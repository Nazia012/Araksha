"""
RxHandBD Dataset & Detection Integration Tests
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.rxhandbd_loader import rxhandbd_instance
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_rxhandbd_dataset_loading():
    """Validates that RxHandBD dataset loads vocabulary and samples from Zenodo."""
    rxhandbd_instance.load_dataset()
    assert rxhandbd_instance.is_loaded
    assert len(rxhandbd_instance.unique_vocabulary) > 50

    samples = rxhandbd_instance.get_featured_samples(limit=5)
    assert len(samples) == 5
    assert "image" in samples[0]
    assert "label" in samples[0]
    assert "mapped_generic" in samples[0]


def test_rxhandbd_brand_to_rxnorm_mapping():
    """Validates that Bangladeshi and regional doctor prescription brands map to standard RxNorm."""
    assert rxhandbd_instance.resolve_rxhandbd_word("Napa") == "acetaminophen"
    assert rxhandbd_instance.resolve_rxhandbd_word("Seclo") == "omeprazole"
    assert rxhandbd_instance.resolve_rxhandbd_word("Losita") == "losartan"
    assert rxhandbd_instance.resolve_rxhandbd_word("Nitrocontive") == "nitroglycerin"
    assert rxhandbd_instance.resolve_rxhandbd_word("Ciprox") == "ciprofloxacin"


def test_rxhandbd_api_samples_endpoint():
    """Tests the GET /api/v1/rxhandbd/samples endpoint."""
    response = client.get("/api/v1/rxhandbd/samples?limit=6")
    assert response.status_code == 200
    data = response.json()
    assert "samples" in data
    assert len(data["samples"]) == 6
    assert data["samples"][0]["mapped_generic"] == "nitroglycerin"


def test_rxhandbd_detection_and_ddi_endpoint():
    """Tests POST /api/v1/rxhandbd/detect with a severe interaction pair."""
    # Test handwritten Nitrocontive + Sildenafil (Severe hypotension)
    payload = {
        "word_tokens": ["Nitrocontive", "Sildenafil"],
        "confidence_scores": [0.88, 0.95]
    }
    response = client.post("/api/v1/rxhandbd/detect", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "nitroglycerin" in data["generic_drugs"]
    assert "sildenafil" in data["generic_drugs"]
    assert len(data["verified_ddis"]) == 1
    assert data["verified_ddis"][0]["severity"] == "Severe"
