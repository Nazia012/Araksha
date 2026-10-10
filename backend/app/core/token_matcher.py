"""
OCR Post-Processing & Fuzzy Token Matcher (RxNorm Standard)
Matches raw or noisy OCR text/tokens against the curated RxNorm dictionary.
Flags tokens with confidence < 80% or ambiguous matches.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from app.data.rxnorm_catalog import RXNORM_CATALOG, MedicationRecord


def levenshtein_similarity(s1: str, s2: str) -> float:
    """
    Computes normalized similarity between 0.0 and 1.0 using Levenshtein distance.
    """
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # deletion
                dp[i][j - 1] + 1,       # insertion
                dp[i - 1][j - 1] + cost # substitution
            )

    dist = dp[len1][len2]
    max_len = max(len1, len2)
    return max(0.0, 1.0 - (dist / max_len))


def clean_prescription_text(text: str) -> List[str]:
    """
    Removes prescription metadata, medical abbreviations (Sig, PO, BID, QID, PRN),
    dosages (mg, mcg, ml), and returns candidate medication word tokens and phrases.
    """
    if not text:
        return []

    # Clean punctuation and non-alphanumeric noise
    cleaned = re.sub(r"[#*_\(\)\[\]\{\};:\'\"\\\/]", " ", text)
    
    # Common medical stop words and directions to filter out
    stop_words = {
        "rx", "sig", "tab", "tabs", "capsule", "capsules", "po", "bid", "tid", "qid",
        "prn", "daily", "once", "twice", "every", "hours", "hrs", "take", "with",
        "food", "water", "bedtime", "morning", "night", "dispense", "refill", "refills",
        "dr", "doctor", "patient", "name", "date", "qty", "quantity", "mg", "mcg",
        "ml", "tablets", "cap", "oral", "use", "as", "directed", "for", "pain"
    }

    lines = cleaned.splitlines()
    candidate_tokens: List[str] = []

    for line in lines:
        words = re.findall(r"[A-Za-z\-]{3,}", line)
        for w in words:
            w_clean = w.lower().strip("-")
            if len(w_clean) >= 3 and w_clean not in stop_words:
                candidate_tokens.append(w_clean)

        # Also consider two-word combinations (e.g. "potassium chloride", "calcium carbonate")
        for i in range(len(words) - 1):
            phrase = f"{words[i].lower().strip()} {words[i+1].lower().strip()}"
            candidate_tokens.append(phrase)

    return list(dict.fromkeys(candidate_tokens))


class TokenMatcher:
    def __init__(self, catalog: Optional[Dict[str, MedicationRecord]] = None):
        self.catalog = catalog or RXNORM_CATALOG
        # Index all generic names, brand names, and aliases
        self.name_to_generic: Dict[str, str] = {}
        for gen_name, record in self.catalog.items():
            self.name_to_generic[gen_name.lower()] = gen_name
            for brand in record.brand_names:
                self.name_to_generic[brand.lower()] = gen_name

    def match_token(self, token: str, threshold: float = 0.78) -> Optional[Tuple[str, float, MedicationRecord]]:
        """
        Matches a token or phrase against known RxNorm generic and brand names.
        Intelligently strips dosages (10mg, 500mg), medical form prefixes (Tab, Syr, Cap),
        and extracts candidate active ingredients from compound or parenthetical notations.
        Returns (standardized_generic_name, match_confidence, MedicationRecord) or None.
        """
        token_clean = token.lower().strip()
        if not token_clean:
            return None

        # 1. Direct exact match check on whole string
        if token_clean in self.name_to_generic:
            gen_name = self.name_to_generic[token_clean]
            return gen_name, 1.0, self.catalog[gen_name]

        # 2. Extract candidate words/phrases if token contains medical forms or dosage numbers
        medical_stop = {
            "tab", "tabs", "tablet", "tablets", "syr", "syrup", "cap", "capsule",
            "capsules", "inj", "injection", "rx", "dr", "md", "mg", "mcg", "g",
            "ml", "daily", "od", "bd", "bid", "tid", "qid", "prn", "po", "at",
            "night", "morning", "bedtime", "oral", "drops"
        }

        # Words with punctuation stripped
        words = [w.strip().lower() for w in re.findall(r"[A-Za-z\-]{3,}", token_clean)]
        filtered_words = [w for w in words if w not in medical_stop]

        # Check exact match on individual filtered words (e.g. "Aripax" in "Tab Aripax 10mg")
        for word in filtered_words:
            if word in self.name_to_generic:
                gen_name = self.name_to_generic[word]
                return gen_name, 1.0, self.catalog[gen_name]

        # Check exact match on two-word phrases (e.g. "potassium chloride")
        for i in range(len(filtered_words) - 1):
            phrase = f"{filtered_words[i]} {filtered_words[i+1]}"
            if phrase in self.name_to_generic:
                gen_name = self.name_to_generic[phrase]
                return gen_name, 1.0, self.catalog[gen_name]

        # 3. Fuzzy match across candidates (filtered words first, then full token)
        candidates_to_try = filtered_words + [token_clean]
        best_generic: Optional[str] = None
        best_score: float = 0.0

        for cand in candidates_to_try:
            for candidate_name, gen_name in self.name_to_generic.items():
                sim = levenshtein_similarity(cand, candidate_name)
                # Boost score if candidate starts with token or candidate_name
                if candidate_name.startswith(cand) or cand.startswith(candidate_name):
                    sim = max(sim, min(1.0, sim + 0.1))

                if sim > best_score:
                    best_score = sim
                    best_generic = gen_name

        if best_score >= threshold and best_generic:
            return best_generic, round(best_score, 3), self.catalog[best_generic]

        return None

    def process_ocr_tokens(
        self,
        raw_tokens: List[Dict[str, Any]],
        confidence_cutoff: float = 0.80
    ) -> Dict[str, Any]:
        """
        Processes a list of OCR token objects:
        Each item: {"text": "Warfrin", "confidence": 0.75, "bbox": [x1, y1, x2, y2]}
        Identifies candidate drugs, flags low-confidence tokens (<80%),
        and standardizes generic RxNorm names.
        """
        detected_medications: List[Dict[str, Any]] = []
        uncertainties: List[Dict[str, Any]] = []
        matched_generics = set()

        for token_item in raw_tokens:
            token_text = token_item.get("text", "")
            ocr_conf = float(token_item.get("confidence", 0.90))
            bbox = token_item.get("bbox", [])

            match_result = self.match_token(token_text)
            if match_result:
                gen_name, match_conf, med_record = match_result
                # Overall confidence combines OCR confidence and string similarity
                overall_conf = round(ocr_conf * match_conf, 3)

                is_uncertain = overall_conf < confidence_cutoff

                med_entry = {
                    "raw_text": token_text,
                    "generic_name": gen_name,
                    "rxcui": med_record.rxcui,
                    "drug_class": med_record.drug_class,
                    "brand_names": med_record.brand_names,
                    "description": med_record.description,
                    "ocr_confidence": ocr_conf,
                    "match_confidence": match_conf,
                    "overall_confidence": overall_conf,
                    "needs_review": is_uncertain,
                    "bbox": bbox
                }

                if gen_name not in matched_generics:
                    matched_generics.add(gen_name)
                    detected_medications.append(med_entry)

                if is_uncertain:
                    uncertainties.append({
                        "token": token_text,
                        "suggested_match": gen_name,
                        "confidence": overall_conf,
                        "reason": f"OCR or match confidence ({int(overall_conf * 100)}%) is below review threshold (80%)."
                    })
            else:
                # If token looked like a potential drug name but didn't match cleanly
                if len(token_text) >= 4 and not token_text.isdigit():
                    if ocr_conf < confidence_cutoff:
                        uncertainties.append({
                            "token": token_text,
                            "suggested_match": None,
                            "confidence": ocr_conf,
                            "reason": f"Unrecognized medical token with low OCR confidence ({int(ocr_conf * 100)}%)."
                        })

        return {
            "detected_medications": detected_medications,
            "generic_drugs": list(matched_generics),
            "uncertainties": uncertainties
        }

    def process_raw_text(
        self,
        raw_text: str,
        default_confidence: float = 0.95
    ) -> Dict[str, Any]:
        """
        Processes a block of plain prescription text (e.g. from OCR or user input).
        """
        candidate_words = clean_prescription_text(raw_text)
        token_items = [
            {"text": word, "confidence": default_confidence}
            for word in candidate_words
        ]
        return self.process_ocr_tokens(token_items)
