"""
Four-Stage Clinical Prescription Pipeline API
Stage 1: OCR Testing (RxHandBD Zenodo)
Stage 2: Entity Grounding (RxNorm Concept Table)
Stage 3: Verification Engine (TWOSIDES / DDI Corpus)
Stage 4: Gemma 4 Few-Shot Prompts (n2c2 Medication Event Annotations)
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.ocr_testing import evaluate_ocr_tolerance, benchmark_rxhandbd_samples
from app.core.entity_grounding import ground_prescription_token, ground_all_tokens
from app.core.twosides_engine import query_twosides_interactions
from app.services.gemma_service import get_gemma_explanation

router = APIRouter(prefix="/api/v1/pipeline", tags=["4-Stage Pipeline"])


class PipelineInput(BaseModel):
    tokens: List[Dict[str, Any]]
    confidence_cutoff: float = 0.80


@router.get("/stages")
async def get_pipeline_stages():
    """
    Returns specifications for the 4-stage pipeline architecture.
    """
    return {
        "pipeline_name": "Modular Prescription & DDI Inspector Pipeline",
        "stages": [
            {
                "stage": 1,
                "name": "OCR Testing",
                "dataset_source": "RxHandBD (Zenodo DOI: 10.5281/zenodo.18478741)",
                "format": "Images (128x128 JPG) + CSV (Train_Label, Test_Labels)",
                "purpose": "Test OCR tolerance on real physician prescription handwriting and gate <80% confidence items"
            },
            {
                "stage": 2,
                "name": "Entity Grounding",
                "dataset_source": "RxNorm Concept Table",
                "format": "SQLite / CSV",
                "purpose": "Map noisy OCR strings and brand aliases to standard active ingredient names and RxCUI codes"
            },
            {
                "stage": 3,
                "name": "Verification Engine",
                "dataset_source": "DDI Corpus / TWOSIDES",
                "format": "SQLite Table (twosides_ddi)",
                "purpose": "Deterministic query of interacting drug pairs without LLM hallucination"
            },
            {
                "stage": 4,
                "name": "Gemma 4 Few-Shot Prompts",
                "dataset_source": "n2c2 Medication Event Annotations",
                "format": "JSON (n2c2_few_shot.json)",
                "purpose": "Few-shot context examples showing how to summarize dosages, routes, and frequencies in plain English"
            }
        ]
    }


@router.get("/stage1/benchmark")
async def run_stage1_benchmark(samples_count: int = 8):
    """Executes Stage 1 benchmark against RxHandBD Zenodo handwriting samples."""
    return {
        "stage": "Stage 1: OCR Testing on RxHandBD",
        "benchmark_results": benchmark_rxhandbd_samples(samples_count=samples_count)
    }


@router.post("/execute")
async def execute_four_stage_pipeline(request: PipelineInput):
    """
    Executes all 4 stages sequentially and returns full stage-by-stage audit output.
    """
    raw_tokens = request.tokens

    # ==========================================
    # STAGE 1: OCR Testing & Tolerance (RxHandBD)
    # ==========================================
    stage_1_results = []
    gated_tokens = []
    uncertainties = []

    for t in raw_tokens:
        text = t.get("text", "")
        conf = float(t.get("confidence", 0.90))

        # Test against RxHandBD tolerance standards
        eval_res = evaluate_ocr_tolerance(text, text, raw_confidence=conf)
        stage_1_results.append(eval_res)

        if eval_res["needs_review"]:
            uncertainties.append(f"Token '{text}' flagged in Stage 1: {eval_res['clinical_flag']}.")

        gated_tokens.append({
            "text": text,
            "confidence": eval_res["adjusted_confidence"]
        })

    # ==========================================
    # STAGE 2: Entity Grounding (RxNorm Concepts)
    # ==========================================
    grounded_entities = ground_all_tokens(gated_tokens)
    generic_names = [e.active_ingredient for e in grounded_entities]
    stage_2_results = [e.to_dict() for e in grounded_entities]

    # ==========================================
    # STAGE 3: Verification Engine (TWOSIDES DDI)
    # ==========================================
    twosides_ddis = query_twosides_interactions(generic_names)

    # Determine risk level
    severities = [d.get("severity", "").lower() for d in twosides_ddis]
    if any(s == "severe" for s in severities):
        risk_level = "Severe"
        risk_color = "red"
    elif any(s in ("moderate", "caution") for s in severities):
        risk_level = "Moderate"
        risk_color = "amber"
    else:
        risk_level = "Clear"
        risk_color = "green"

    # ==========================================
    # STAGE 4: Gemma 4 Few-Shot Translation (n2c2)
    # ==========================================
    detected_meds_payload = [
        {
            "generic_name": e.active_ingredient,
            "rxcui": e.rxcui,
            "drug_class": e.drug_class,
            "overall_confidence": e.grounding_confidence,
            "needs_review": e.needs_review
        }
        for e in grounded_entities
    ]

    gemma_output = await get_gemma_explanation(
        detected_medications=detected_meds_payload,
        verified_interactions=twosides_ddis,
        uncertainties=uncertainties
    )

    # Build checklist
    checklist = []
    for ddi in twosides_ddis:
        checklist.append(
            f"Discuss {ddi.get('pair')} ({ddi.get('severity')} risk - {ddi.get('side_effect')}) with pharmacist."
        )
    if not checklist:
        checklist.append("Confirm all medication dosage timings and food/water intake instructions.")
        checklist.append("Check if any newly started over-the-counter supplements might interfere.")

    return {
        "status": "success",
        "risk_level": risk_level,
        "risk_color": risk_color,
        "stages": {
            "stage_1_ocr_testing": {
                "dataset": "RxHandBD (Zenodo 10.5281/zenodo.18478741)",
                "evaluations": stage_1_results
            },
            "stage_2_entity_grounding": {
                "dataset": "RxNorm Concept Table",
                "grounded_entities": stage_2_results
            },
            "stage_3_verification_engine": {
                "dataset": "DDI Corpus / TWOSIDES (SQLite)",
                "verified_ddis": twosides_ddis
            },
            "stage_4_gemma4_few_shot": {
                "dataset": "n2c2 Medication Event Annotations (JSON)",
                "patient_summary": gemma_output.get("patient_summary", ""),
                "interaction_flags": gemma_output.get("interaction_flags", []),
                "pharmacist_checklist": checklist,
                "disclaimer": gemma_output.get("disclaimer", "")
            }
        }
    }
