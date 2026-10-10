"""
Automated Integration Tests for the 4-Stage Clinical Pipeline
Stage 1: OCR Testing (RxHandBD)
Stage 2: Entity Grounding (RxNorm Concepts)
Stage 3: Verification Engine (TWOSIDES DDI)
Stage 4: Gemma 4 Few-Shot Translation (n2c2)
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.ocr_testing import evaluate_ocr_tolerance, benchmark_rxhandbd_samples
from app.core.entity_grounding import ground_prescription_token
from app.core.twosides_engine import query_twosides_interactions
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_stage1_ocr_tolerance_rxhandbd():
    """Validates Stage 1: OCR tolerance and Character Error Rate on RxHandBD."""
    # Test high tolerance match
    res_clean = evaluate_ocr_tolerance("Napa", "Napa", raw_confidence=0.95)
    assert res_clean["tolerance_passed"] is True
    assert res_clean["cer"] == 0.0

    # Test noisy OCR transcription (<80% gating)
    res_noisy = evaluate_ocr_tolerance("Warfrin", "Warfarin", raw_confidence=0.75)
    assert res_noisy["adjusted_confidence"] < 0.80
    assert "Requires Pharmacist Verification" in res_noisy["clinical_flag"]


def test_stage2_entity_grounding_rxnorm():
    """Validates Stage 2: Entity Grounding from noisy brand strings to RxNorm CUI."""
    # Napa (RxHandBD brand) -> acetaminophen
    entity = ground_prescription_token("Napa")
    assert entity is not None
    assert entity.active_ingredient == "acetaminophen"
    assert entity.rxcui == "161"

    # Nitrocontive (RxHandBD brand) -> nitroglycerin
    nitro_entity = ground_prescription_token("Nitrocontive")
    assert nitro_entity is not None
    assert nitro_entity.active_ingredient == "nitroglycerin"
    assert nitro_entity.rxcui == "7435"


def test_stage3_twosides_verification_engine():
    """Validates Stage 3: Deterministic query against TWOSIDES DDI corpus."""
    ddis = query_twosides_interactions(["warfarin", "aspirin"])
    assert len(ddis) >= 1
    assert ddis[0]["severity"] == "Severe"
    assert "Hemorrhage" in ddis[0]["side_effect"] or "Bleeding" in ddis[0]["side_effect"]

    # Sildenafil + Nitroglycerin
    nitro_ddis = query_twosides_interactions(["sildenafil", "nitroglycerin"])
    assert len(nitro_ddis) >= 1
    assert nitro_ddis[0]["severity"] == "Severe"
    assert "Hypotension" in nitro_ddis[0]["side_effect"]


def test_stage4_four_stage_pipeline_execution():
    """Validates the full 4-stage pipeline execution via REST endpoint."""
    payload = {
        "tokens": [
            {"text": "Nitrocontive", "confidence": 0.88},
            {"text": "Sildenafil", "confidence": 0.95}
        ]
    }
    response = client.post("/api/v1/pipeline/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["risk_level"] == "Severe"

    # Check all 4 stages in response
    stages = data["stages"]
    assert "stage_1_ocr_testing" in stages
    assert "stage_2_entity_grounding" in stages
    assert "stage_3_verification_engine" in stages
    assert "stage_4_gemma4_few_shot" in stages

    # Check Stage 4 Gemma 4 output
    stage_4 = stages["stage_4_gemma4_few_shot"]
    assert "patient_summary" in stage_4
    assert len(stage_4["interaction_flags"]) >= 1
    assert "pharmacist_checklist" in stage_4
