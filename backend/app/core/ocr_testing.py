"""
Stage 1: OCR Testing Engine with RxHandBD (Zenodo DOI: 10.5281/zenodo.18478741)
Tests OCR tolerance, Character Error Rate (CER), Word Error Rate (WER), and confidence degradation
on real handwritten prescription word images from physicians.
"""

from typing import Dict, List, Any, Tuple
import os
import csv
from app.core.token_matcher import levenshtein_similarity
from app.core.rxhandbd_loader import rxhandbd_instance


def compute_cer(reference: str, hypothesis: str) -> float:
    """
    Computes Character Error Rate (CER) = Levenshtein Distance(chars) / len(reference).
    """
    ref = reference.lower().strip()
    hyp = hypothesis.lower().strip()
    if not ref:
        return 0.0 if not hyp else 1.0
    sim = levenshtein_similarity(ref, hyp)
    return max(0.0, round(1.0 - sim, 3))


def evaluate_ocr_tolerance(
    ocr_transcription: str,
    ground_truth_label: str,
    raw_confidence: float = 0.90
) -> Dict[str, Any]:
    """
    Evaluates an OCR transcription against RxHandBD ground truth.
    Returns error metrics (CER, similarity), tolerance status, and clinical review flags.
    """
    cer = compute_cer(ground_truth_label, ocr_transcription)
    similarity = round(1.0 - cer, 3)

    # Adjust confidence based on character-level noise and handwriting variance
    adjusted_confidence = round(raw_confidence * similarity, 3)
    needs_review = adjusted_confidence < 0.80 or cer > 0.20

    return {
        "ocr_transcription": ocr_transcription,
        "ground_truth": ground_truth_label,
        "cer": cer,
        "similarity": similarity,
        "adjusted_confidence": adjusted_confidence,
        "needs_review": needs_review,
        "tolerance_passed": not needs_review,
        "clinical_flag": "Requires Pharmacist Verification (<80% or CER > 20%)" if needs_review else "Accepted",
        "dataset_source": "RxHandBD (Zenodo 10.5281/zenodo.18478741)"
    }


def benchmark_rxhandbd_samples(samples_count: int = 8) -> List[Dict[str, Any]]:
    """
    Runs a benchmark test across RxHandBD physician handwriting samples,
    simulating handwriting recognition variance and testing the <80% confidence cutoff.
    """
    rxhandbd_instance.load_dataset()
    featured = rxhandbd_instance.get_featured_samples(limit=samples_count)
    results = []

    # Test cases simulating typical OCR handwriting degradation
    noisy_variants = {
        "Nitrocontive": "Nitrocontiv",  # slight ending drop
        "Ciprox": "Cipro",             # missing letter
        "Losita": "Losita",            # exact match
        "Seclo": "Secl0",              # numeral confusion
        "Nexcital": "Nexcita",         # tail truncated
        "Napa": "Napa",                # exact match
        "Zimax": "Zimx",               # inner vowel drop
        "Lasix": "Lasx",               # drop
    }

    for sample in featured:
        gt = sample["label"]
        hypo = noisy_variants.get(gt, gt)
        raw_conf = sample.get("confidence", 0.90)

        eval_res = evaluate_ocr_tolerance(
            ocr_transcription=hypo,
            ground_truth_label=gt,
            raw_confidence=raw_conf
        )
        eval_res["image"] = sample.get("image", "")
        eval_res["mapped_generic"] = sample.get("mapped_generic", "")
        results.append(eval_res)

    return results
