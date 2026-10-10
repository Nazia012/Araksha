"""
Automated Integration & Unit Tests for Prescription & DDI Pipeline
Validates RxNorm matching, deterministic DDI database queries, and Gemma 4 payload formatting.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.database import init_db, query_drug_interactions, search_rxnorm_medications
from app.core.token_matcher import TokenMatcher
from ai_service.gemma_client import GemmaClient


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Initializes and seeds the database before tests run."""
    init_db(seed_if_empty=True)


def test_rxnorm_catalog_and_search():
    """Validates autocomplete and RxNorm search for brand and generic names."""
    results = search_rxnorm_medications("coumadin")
    assert len(results) > 0
    assert results[0]["generic_name"] == "warfarin"

    lipitor_results = search_rxnorm_medications("lipitor")
    assert len(lipitor_results) > 0
    assert lipitor_results[0]["generic_name"] == "atorvastatin"


def test_token_matcher_exact_and_fuzzy():
    """Validates OCR token matching and normalization to RxNorm standards."""
    matcher = TokenMatcher()

    # Exact generic
    match = matcher.match_token("warfarin")
    assert match is not None
    assert match[0] == "warfarin"
    assert match[1] == 1.0

    # Brand name to generic mapping
    match_brand = matcher.match_token("advil")
    assert match_brand is not None
    assert match_brand[0] == "ibuprofen"

    # Fuzzy noisy OCR typo ("Warfrin" -> "warfarin")
    fuzzy_match = matcher.match_token("Warfrin")
    assert fuzzy_match is not None
    assert fuzzy_match[0] == "warfarin"
    assert fuzzy_match[1] >= 0.85

    # Low confidence token processing
    ocr_tokens = [
        {"text": "Warfrin", "confidence": 0.70},  # < 80% confidence
        {"text": "Advil", "confidence": 0.95}
    ]
    processed = matcher.process_ocr_tokens(ocr_tokens, confidence_cutoff=0.80)
    assert len(processed["detected_medications"]) == 2
    assert "warfarin" in processed["generic_drugs"]
    assert "ibuprofen" in processed["generic_drugs"]
    assert len(processed["uncertainties"]) >= 1


def test_deterministic_ddi_engine_severe_interaction():
    """
    CRITICAL: Validates deterministic SQL query:
    SELECT drug_a, drug_b, severity, mechanism, recommendation 
    FROM drug_interactions 
    WHERE (drug_a IN (:drugs) AND drug_b IN (:drugs)) 
       OR (drug_b IN (:drugs) AND drug_a IN (:drugs));
    """
    # 1. Warfarin + Aspirin (Severe Bleeding)
    ddis = query_drug_interactions(["warfarin", "aspirin"])
    assert len(ddis) == 1
    assert ddis[0]["severity"] == "Severe"
    assert "bleeding" in ddis[0]["mechanism"].lower() or "coagulation" in ddis[0]["mechanism"].lower()

    # 2. Sildenafil + Nitroglycerin (Severe Hypotension)
    sildenafil_ddis = query_drug_interactions(["sildenafil", "nitroglycerin"])
    assert len(sildenafil_ddis) == 1
    assert sildenafil_ddis[0]["severity"] == "Severe"
    assert "hypotension" in sildenafil_ddis[0]["mechanism"].lower() or "vasodilation" in sildenafil_ddis[0]["mechanism"].lower()

    # 3. Lisinopril + Spironolactone (Severe Hyperkalemia)
    raas_ddis = query_drug_interactions(["lisinopril", "spironolactone"])
    assert len(raas_ddis) == 1
    assert raas_ddis[0]["severity"] == "Severe"

    # 4. Independent un-interacting drugs should return 0 DDIs
    clear_ddis = query_drug_interactions(["metformin", "acetaminophen"])
    assert len(clear_ddis) == 0


def test_gemma_client_schema_and_plain_language():
    """Validates that Gemma 4 output strictly satisfies the user's required schema."""
    import asyncio
    client = GemmaClient()
    detected_meds = [
        {"generic_name": "warfarin", "rxcui": "11289", "drug_class": "Anticoagulant", "overall_confidence": 0.95},
        {"generic_name": "aspirin", "rxcui": "1191", "drug_class": "Antiplatelet", "overall_confidence": 0.95}
    ]
    interactions = [
        {
            "pair": "Warfarin + Aspirin",
            "severity": "Severe",
            "mechanism": "Synergistic inhibition of coagulation factors and platelet aggregation, increasing bleeding risk.",
            "recommendation": "Avoid concurrent use unless strictly indicated."
        }
    ]
    uncertainties = ["Warfrin (OCR confidence 70%)"]

    response = asyncio.run(client.generate_patient_explanation(detected_meds, interactions, uncertainties))

    # Check schema keys
    assert "patient_summary" in response
    assert "interaction_flags" in response
    assert "uncertainties" in response
    assert "disclaimer" in response

    # Check contents
    assert len(response["interaction_flags"]) == 1
    flag = response["interaction_flags"][0]
    assert flag["pair"] == "Warfarin + Aspirin"
    assert flag["severity"] == "Severe"
    assert "action_for_pharmacist" in flag
    assert len(flag["action_for_pharmacist"]) > 0
    assert "medical advice" in response["disclaimer"].lower()
