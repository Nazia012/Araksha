"""
Test Suite: Real Doctor Prescription Calibration (Dr. Sanjay Kumar Singh, MD Psychiatrist)
Tests OCR handwriting resolution, RxNorm entity grounding, and deterministic DDI safety check.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.core.entity_grounding import ground_prescription_token
from app.core.twosides_engine import query_twosides_interactions
from app.core.prescription_calibrator import DR_SANJAY_PRESCRIPTION_PROFILE

client = TestClient(app)


def test_prescription_profile_structure():
    """Verify Dr. Sanjay Kumar Singh prescription profile metadata."""
    assert DR_SANJAY_PRESCRIPTION_PROFILE["physician"]["name"] == "Dr. Sanjay Kumar Singh"
    assert DR_SANJAY_PRESCRIPTION_PROFILE["patient"]["name"] == "Nazia Parbat"
    assert len(DR_SANJAY_PRESCRIPTION_PROFILE["handwritten_items"]) == 5


def test_handwriting_entity_grounding_dr_sanjay():
    """Verify that all 5 handwritten tokens ground accurately to RxNorm generic active ingredients."""
    items = DR_SANJAY_PRESCRIPTION_PROFILE["handwritten_items"]

    # Line 1: Tab Aripax 10mg -> aripiprazole
    e1 = ground_prescription_token("Tab Aripax 10mg", ocr_confidence=0.92)
    assert e1 is not None
    assert e1.active_ingredient == "aripiprazole"

    # Line 2: Tab Lupizep 25mg -> paroxetine
    e2 = ground_prescription_token("Tab Lupizep 25mg", ocr_confidence=0.88)
    assert e2 is not None
    assert e2.active_ingredient == "paroxetine"

    # Line 3: Tab Toficalm 50mg -> tofisopam
    e3 = ground_prescription_token("Tab Toficalm 50mg", ocr_confidence=0.90)
    assert e3 is not None
    assert e3.active_ingredient == "tofisopam"

    # Line 4: Tab Lonazep MD -> clonazepam
    e4 = ground_prescription_token("Tab Lonazep MD", ocr_confidence=0.86)
    assert e4 is not None
    assert e4.active_ingredient == "clonazepam"

    # Line 5: Syr Carnisure 10ml -> levocarnitine
    e5 = ground_prescription_token("Syr Carnisure 10ml", ocr_confidence=0.91)
    assert e5 is not None
    assert e5.active_ingredient == "levocarnitine"


def test_ddi_verification_dr_sanjay():
    """Verify deterministic detection of severe CYP2D6 interaction between paroxetine and aripiprazole."""
    meds = ["aripiprazole", "paroxetine", "clonazepam", "tofisopam", "levocarnitine"]
    interactions = query_twosides_interactions(meds)

    # Must detect paroxetine + aripiprazole as Severe
    pair_names = [i["pair"].lower() for i in interactions]
    severities = [i["severity"] for i in interactions]

    assert any("paroxetine" in p and "aripiprazole" in p for p in pair_names)
    assert "Severe" in severities


def test_api_calibrated_dr_sanjay_endpoint():
    """Verify API endpoint returns calibrated prescription profile."""
    res = client.get("/api/v1/prescriptions/calibrated/dr_sanjay")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["profile"]["prescription_id"] == "dr_sanjay_220126"
