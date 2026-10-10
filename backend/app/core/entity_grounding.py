"""
Stage 2: Entity Grounding Engine with RxNorm Concept Table
Maps noisy, misspelled, or regional OCR tokens (e.g., from RxHandBD or prescription scans)
to standard active ingredient names and standardized RxCUI codes.
"""

from typing import Dict, List, Any, Optional, Tuple
from app.core.token_matcher import TokenMatcher
from app.data.rxnorm_catalog import RXNORM_CATALOG, MedicationRecord
from app.core.rxhandbd_loader import rxhandbd_instance, RXHANDBD_TO_RXNORM

matcher = TokenMatcher()


class GroundedEntity:
    def __init__(
        self,
        raw_token: str,
        active_ingredient: str,
        rxcui: str,
        term_type: str,
        drug_class: str,
        grounding_confidence: float,
        needs_review: bool
    ):
        self.raw_token = raw_token
        self.active_ingredient = active_ingredient
        self.rxcui = rxcui
        self.term_type = term_type  # "IN" (Ingredient), "BN" (Brand Name), "PIN" (Precise Ingredient)
        self.drug_class = drug_class
        self.grounding_confidence = grounding_confidence
        self.needs_review = needs_review

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_token": self.raw_token,
            "active_ingredient": self.active_ingredient,
            "rxcui": self.rxcui,
            "term_type": self.term_type,
            "drug_class": self.drug_class,
            "grounding_confidence": self.grounding_confidence,
            "needs_review": self.needs_review,
        }


def ground_prescription_token(noisy_token: str, ocr_confidence: float = 0.90) -> Optional[GroundedEntity]:
    """
    Stage 2 Resolution Pipeline:
    1. Check RxHandBD brand vocabulary dictionary
    2. Check exact RxNorm catalog (Generic & Brand)
    3. Fuzzy Levenshtein match against RxNorm Concept Table
    4. Compute combined grounding confidence & review gating (<80%)
    """
    token_clean = noisy_token.strip().lower()
    if not token_clean:
        return None

    # 1. Check RxHandBD dictionary alias
    if token_clean in RXHANDBD_TO_RXNORM:
        generic = RXHANDBD_TO_RXNORM[token_clean]
        rec = RXNORM_CATALOG.get(generic)
        if rec:
            conf = round(ocr_confidence * 0.96, 3)
            return GroundedEntity(
                raw_token=noisy_token,
                active_ingredient=rec.generic_name,
                rxcui=rec.rxcui,
                term_type="BN",
                drug_class=rec.drug_class,
                grounding_confidence=conf,
                needs_review=conf < 0.80
            )

    # 2. Check RxNorm matcher (Generic or Brand)
    match_res = matcher.match_token(token_clean)
    if match_res:
        gen_name, sim, rec = match_res
        is_exact = token_clean == gen_name or token_clean in [b.lower() for b in rec.brand_names]
        term_type = "IN" if token_clean == gen_name else "BN"
        ground_conf = round(ocr_confidence * sim, 3)

        return GroundedEntity(
            raw_token=noisy_token,
            active_ingredient=gen_name,
            rxcui=rec.rxcui,
            term_type=term_type,
            drug_class=rec.drug_class,
            grounding_confidence=ground_conf,
            needs_review=ground_conf < 0.80
        )

    # 3. Check partial RxHandBD contains
    for brand, generic in RXHANDBD_TO_RXNORM.items():
        if brand in token_clean or token_clean in brand:
            rec = RXNORM_CATALOG.get(generic)
            if rec:
                conf = round(ocr_confidence * 0.82, 3)
                return GroundedEntity(
                    raw_token=noisy_token,
                    active_ingredient=rec.generic_name,
                    rxcui=rec.rxcui,
                    term_type="BN",
                    drug_class=rec.drug_class,
                    grounding_confidence=conf,
                    needs_review=conf < 0.80
                )

    return None


def ground_all_tokens(tokens: List[Dict[str, Any]]) -> List[GroundedEntity]:
    """
    Processes a batch of candidate prescription tokens into grounded RxNorm entities.
    """
    grounded = []
    seen_generics = set()

    for item in tokens:
        text = item.get("text", "")
        conf = float(item.get("confidence", 0.90))

        entity = ground_prescription_token(text, ocr_confidence=conf)
        if entity and entity.active_ingredient not in seen_generics:
            seen_generics.add(entity.active_ingredient)
            grounded.append(entity)

    return grounded
