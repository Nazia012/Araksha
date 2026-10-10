"""
API Endpoints Integration Tests
Validates FastAPI endpoints directly via TestClient.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Google Gemma 4" in data["ai_engine"]


def test_drug_lookup_autocomplete():
    response = client.get("/api/v1/drugs/lookup?q=viagra")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert data["results"][0]["generic_name"] == "sildenafil"


def test_prescription_process_endpoint_severe_risk():
    payload = {
        "tokens": [
            {"text": "Sildenafil", "confidence": 0.95},
            {"text": "Nitroglycerin", "confidence": 0.92}
        ]
    }
    response = client.post("/api/v1/prescriptions/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["risk_level"] == "Severe"
    assert data["risk_color"] == "red"
    assert len(data["verified_ddis"]) == 1
    assert "Sildenafil + Nitroglycerin" in data["interaction_flags"][0]["pair"]
    assert "pharmacist_checklist" in data
    assert len(data["pharmacist_checklist"]) > 0


def test_prescription_process_endpoint_with_uncertainty():
    payload = {
        "tokens": [
            {"text": "Warfrin", "confidence": 0.72},  # Low confidence (< 80%)
            {"text": "Aspirin", "confidence": 0.95}
        ],
        "confidence_cutoff": 0.80
    }
    response = client.post("/api/v1/prescriptions/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "Severe"
    # Should flag uncertainty for review
    assert len(data["uncertainties"]) >= 1
