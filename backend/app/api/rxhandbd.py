"""
RxHandBD Dataset API Endpoints
Provides access to Zenodo RxHandBD handwritten prescription dataset and OCR word detection.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, Body, HTTPException
from pydantic import BaseModel

from app.core.rxhandbd_loader import rxhandbd_instance
from app.core.token_matcher import TokenMatcher
from app.core.database import query_drug_interactions

router = APIRouter(prefix="/api/v1/rxhandbd", tags=["RxHandBD"])

token_matcher = TokenMatcher()


class DetectionRequest(BaseModel):
    word_tokens: List[str]
    confidence_scores: Optional[List[float]] = None


@router.get("/info")
async def get_dataset_info():
    """Returns metadata and statistics about the Zenodo RxHandBD dataset."""
    rxhandbd_instance.load_dataset()
    return {
        "dataset_name": "RxHandBD (Handwritten Prescription Word Image Dataset)",
        "source": "Zenodo (DOI: 10.5281/zenodo.18478741)",
        "original_repository": "Mendeley Data (10.17632/dsb5r6vskg.1)",
        "author": "Md Masudul Islam",
        "total_images": 5578,
        "unique_vocabulary_count": len(rxhandbd_instance.unique_vocabulary),
        "split_ratio": "80% Training (4,463) / 20% Testing (1,115)",
        "image_resolution": "128x128 pixel JPG",
        "use_case": "Prescription handwriting recognition & clinical DDI verification"
    }


@router.get("/samples")
async def get_sample_words(limit: int = Query(10, ge=1, le=50)):
    """Returns curated handwritten prescription words from RxHandBD for interactive testing."""
    return {
        "dataset": "RxHandBD (Zenodo DOI: 10.5281/zenodo.18478741)",
        "samples": rxhandbd_instance.get_featured_samples(limit=limit)
    }


@router.post("/detect")
async def detect_handwritten_prescription(request: DetectionRequest):
    """
    Matches candidate handwritten OCR tokens against the 1,559 RxHandBD vocabulary
    and maps them to standardized RxNorm active ingredients.
    """
    detected_words = []
    generic_drugs = set()
    uncertainties = []

    confidences = request.confidence_scores or [0.90] * len(request.word_tokens)

    for idx, token in enumerate(request.word_tokens):
        conf = confidences[idx] if idx < len(confidences) else 0.90

        # Match against RxHandBD vocabulary
        rxhand_match = rxhandbd_instance.match_handwritten_token(token)
        matched_term = rxhand_match[0] if rxhand_match else token
        match_conf = rxhand_match[1] if rxhand_match else 0.80

        # Standardize against RxNorm
        rxnorm_match = token_matcher.match_token(matched_term)
        if rxnorm_match:
            gen_name, sim, record = rxnorm_match
            overall_conf = round(conf * match_conf * sim, 3)
            generic_drugs.add(gen_name)
            is_uncertain = overall_conf < 0.80

            detected_words.append({
                "raw_handwritten_input": token,
                "rxhandbd_label": matched_term,
                "generic_name": gen_name,
                "rxcui": record.rxcui,
                "drug_class": record.drug_class,
                "confidence": overall_conf,
                "needs_review": is_uncertain
            })

            if is_uncertain:
                uncertainties.append(f"Handwritten token '{token}' scored {int(overall_conf * 100)}% (<80% threshold).")

    # Deterministic DDI check
    verified_ddis = query_drug_interactions(list(generic_drugs))

    return {
        "status": "success",
        "detected_words": detected_words,
        "generic_drugs": list(generic_drugs),
        "verified_ddis": verified_ddis,
        "uncertainties": uncertainties
    }
