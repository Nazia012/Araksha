"""
Prescription Processing & Analysis API Endpoints
Handles OCR token ingestion, RxNorm normalization, deterministic DDI lookup,
and Gemma 4 AI plain-language generation.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, File, UploadFile, Form, Body, HTTPException
from pydantic import BaseModel, Field

from app.core.token_matcher import TokenMatcher
from app.core.database import query_drug_interactions
from app.services.gemma_service import get_gemma_explanation

router = APIRouter(prefix="/api/v1", tags=["Prescription"])

token_matcher = TokenMatcher()


class TokenInput(BaseModel):
    text: str
    confidence: float = 0.95
    bbox: Optional[List[float]] = None


class PrescriptionProcessRequest(BaseModel):
    raw_text: Optional[str] = None
    tokens: Optional[List[TokenInput]] = None
    manual_drugs: Optional[List[str]] = None
    confidence_cutoff: float = 0.80


class InteractionFlag(BaseModel):
    pair: str
    severity: str
    explanation: str
    action_for_pharmacist: str


class PrescriptionAnalysisResponse(BaseModel):
    status: str
    risk_level: str  # "Severe", "Moderate", "Clear"
    risk_color: str  # "red", "amber", "green"
    detected_medications: List[Dict[str, Any]]
    verified_ddis: List[Dict[str, Any]]
    patient_summary: str
    interaction_flags: List[InteractionFlag]
    uncertainties: List[str]
    pharmacist_checklist: List[str]
    disclaimer: str


def compute_risk_classification(interactions: List[Dict[str, Any]]) -> tuple[str, str]:
    """
    Computes overall risk level and color:
    - Red: Severe DDI
    - Amber: Moderate/Caution DDI
    - Green: Clear (No interactions found)
    """
    if not interactions:
        return "Clear", "green"

    severities = [i.get("severity", "").lower() for i in interactions]
    if any(s == "severe" for s in severities):
        return "Severe", "red"
    if any(s in ("moderate", "caution") for s in severities):
        return "Moderate", "amber"
    return "Clear", "green"


def build_pharmacist_checklist(
    detected_meds: List[Dict[str, Any]],
    verified_interactions: List[Dict[str, Any]],
    uncertainties: List[Any]
) -> List[str]:
    """
    Generates actionable checklist questions for the patient to ask their pharmacist.
    """
    checklist = []
    
    # 1. Uncertainty verification items
    if uncertainties:
        checklist.append("Verify low-confidence or handwritten prescription items with the pharmacy team.")

    # 2. Interaction-specific checklist items
    for item in verified_interactions:
        pair = item.get("pair", "")
        sev = item.get("severity", "")
        checklist.append(f"Discuss {pair} ({sev} interaction risk) and review recommended dosing intervals.")

    # 3. Standard clinical safety checkpoints
    if any(m.get("generic_name") in ["warfarin", "apixaban", "rivaroxaban", "clopidogrel"] for m in detected_meds):
        checklist.append("Confirm target INR or bleeding precautions before taking any over-the-counter NSAIDs.")

    if any(m.get("generic_name") in ["sildenafil", "tadalafil"] for m in detected_meds):
        checklist.append("Confirm emergency nitrate avoidance protocol.")

    if any(m.get("generic_name") in ["lisinopril", "losartan", "spironolactone"] for m in detected_meds):
        checklist.append("Ask whether routine blood potassium and kidney function monitoring is scheduled.")

    if not checklist:
        checklist.append("Confirm all medication dosage timings and food/water intake instructions.")
        checklist.append("Check if any newly started over-the-counter supplements might interfere.")

    return checklist


async def _run_pipeline(
    raw_text: Optional[str] = None,
    tokens: Optional[List[TokenInput]] = None,
    manual_drugs: Optional[List[str]] = None,
    confidence_cutoff: float = 0.80
) -> Dict[str, Any]:
    """
    Internal execution pipeline for OCR post-processing, RxNorm matching,
    deterministic DDI querying, and Gemma 4 AI explanation.
    """
    detected_medications = []
    generic_drugs = set()
    uncertainties_list = []

    # 1. Process structured OCR tokens if provided
    if tokens:
        raw_token_dicts = [t.model_dump() if hasattr(t, "model_dump") else t.dict() for t in tokens]
        ocr_result = token_matcher.process_ocr_tokens(
            raw_token_dicts,
            confidence_cutoff=confidence_cutoff
        )
        detected_medications.extend(ocr_result["detected_medications"])
        generic_drugs.update(ocr_result["generic_drugs"])
        uncertainties_list.extend(ocr_result["uncertainties"])

    # 2. Process raw text if provided
    if raw_text:
        text_result = token_matcher.process_raw_text(raw_text)
        for med in text_result["detected_medications"]:
            if med["generic_name"] not in generic_drugs:
                generic_drugs.add(med["generic_name"])
                detected_medications.append(med)
        uncertainties_list.extend(text_result["uncertainties"])

    # 3. Add any manual user-added/corrected medications
    if manual_drugs:
        for drug_name in manual_drugs:
            clean_name = drug_name.strip().lower()
            match = token_matcher.match_token(clean_name)
            if match:
                gen, conf, record = match
                if gen not in generic_drugs:
                    generic_drugs.add(gen)
                    detected_medications.append({
                        "raw_text": drug_name,
                        "generic_name": gen,
                        "rxcui": record.rxcui,
                        "drug_class": record.drug_class,
                        "brand_names": record.brand_names,
                        "description": record.description,
                        "ocr_confidence": 1.0,
                        "match_confidence": conf,
                        "overall_confidence": conf,
                        "needs_review": False,
                        "bbox": None
                    })
            else:
                # Add as uncertain/unverified drug
                uncertainties_list.append({
                    "token": drug_name,
                    "confidence": 0.50,
                    "reason": f"Manual drug '{drug_name}' could not be matched to standard RxNorm catalog."
                })

    # 4. Deterministic DDI Engine Query against Database
    # RULE: No LLM Hallucination!
    verified_ddis = query_drug_interactions(list(generic_drugs))

    # 5. AI Inference Service: Gemma 4
    gemma_output = await get_gemma_explanation(
        detected_medications=detected_medications,
        verified_interactions=verified_ddis,
        uncertainties=uncertainties_list
    )

    # 6. Risk Level & Pharmacist Checklist
    risk_level, risk_color = compute_risk_classification(verified_ddis)
    checklist = build_pharmacist_checklist(detected_medications, verified_ddis, uncertainties_list)

    return {
        "status": "success",
        "risk_level": risk_level,
        "risk_color": risk_color,
        "detected_medications": detected_medications,
        "verified_ddis": verified_ddis,
        "patient_summary": gemma_output.get("patient_summary", "Review complete."),
        "interaction_flags": gemma_output.get("interaction_flags", []),
        "uncertainties": gemma_output.get("uncertainties", []),
        "pharmacist_checklist": checklist,
        "disclaimer": gemma_output.get(
            "disclaimer",
            "This tool is for informational review and does not replace medical advice."
        )
    }


@router.post("/prescriptions/process")
async def process_prescription(request: PrescriptionProcessRequest) -> Dict[str, Any]:
    """
    Primary processing endpoint accepting JSON tokens, raw text, or manual edits.
    """
    return await _run_pipeline(
        raw_text=request.raw_text,
        tokens=request.tokens,
        manual_drugs=request.manual_drugs,
        confidence_cutoff=request.confidence_cutoff
    )


@router.post("/prescription/analyze")
async def analyze_prescription_alias(
    request: Optional[PrescriptionProcessRequest] = Body(None),
    image: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None),
    confidence_cutoff: float = Form(0.80)
) -> Dict[str, Any]:
    """
    Endpoint accepting either JSON payload or multipart image upload / form data.
    """
    # If JSON payload was passed in body
    if request:
        return await _run_pipeline(
            raw_text=request.raw_text,
            tokens=request.tokens,
            manual_drugs=request.manual_drugs,
            confidence_cutoff=request.confidence_cutoff
        )

    # If multipart upload
    extracted_text = raw_text or ""
    if image:
        # Mock/simulated OCR text extraction from filename or image stream for quick demo
        filename = (image.filename or "").lower()
        if "warfarin" in filename or "aspirin" in filename:
            extracted_text += "\nWarfarin 5mg PO daily\nAspirin 81mg PO daily"
        elif "lisinopril" in filename or "spironolactone" in filename:
            extracted_text += "\nLisinopril 20mg tab\nSpironolactone 25mg daily"
        elif "sildenafil" in filename or "nitro" in filename:
            extracted_text += "\nSildenafil 50mg PRN\nNitroglycerin 0.4mg SL"
        else:
            extracted_text += "\nCoumadin 5mg\nAdvil 400mg"

    return await _run_pipeline(
        raw_text=extracted_text,
        confidence_cutoff=confidence_cutoff
    )


@router.get("/prescriptions/calibrated/dr_sanjay")
async def get_calibrated_dr_sanjay_prescription() -> Dict[str, Any]:
    """
    Returns the calibrated OCR transcription profile for Dr. Sanjay Kumar Singh's prescription
    (MVD Health Plus Multi Speciality Clinic, Guwahati).
    """
    from app.core.prescription_calibrator import DR_SANJAY_PRESCRIPTION_PROFILE
    return {
        "status": "success",
        "profile": DR_SANJAY_PRESCRIPTION_PROFILE
    }

