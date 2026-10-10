"""
RxHandBD Dataset Loader & Handwritten Prescription Recognition Engine
Dataset Source: Zenodo (DOI: 10.5281/zenodo.18478741)
Author: Md Masudul Islam
Contains 5,578 cropped handwritten prescription images and 1,769 unique medical words.
"""

import os
import csv
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger("prescription_inspector.rxhandbd")

DATA_DIR = os.path.dirname(os.path.dirname(__file__))
RXHANDBD_DIR = os.path.join(DATA_DIR, "data", "rxhandbd")

# Mapping RxHandBD physician brand names and terms to RxNorm active ingredients
RXHANDBD_TO_RXNORM = {
    "napa": "acetaminophen",
    "napa one": "acetaminophen",
    "ace": "acetaminophen",
    "ace power": "acetaminophen",
    "paracetamol": "acetaminophen",
    "seclo": "omeprazole",
    "losectil": "omeprazole",
    "omeprazole": "omeprazole",
    "losita": "losartan",
    "angilock": "losartan",
    "osartil": "losartan",
    "losartan": "losartan",
    "nexcital": "escitalopram",
    "escitalopram": "escitalopram",
    "amdocal": "amlodipine",
    "camlosan": "amlodipine",
    "amlodipine": "amlodipine",
    "nitrocontive": "nitroglycerin",
    "nitro-sr": "nitroglycerin",
    "nitroglycerin": "nitroglycerin",
    "ciprox": "ciprofloxacin",
    "ciprocin": "ciprofloxacin",
    "neoflox": "ciprofloxacin",
    "ciprofloxacin": "ciprofloxacin",
    "zimax": "azithromycin",
    "azithromycin": "azithromycin",
    "denvar": "cefixime",
    "monas": "montelukast",
    "monas 10": "montelukast",
    "aldactone": "spironolactone",
    "spironolactone": "spironolactone",
    "lasix": "furosemide",
    "furosemide": "furosemide",
    "warfarin": "warfarin",
    "coumadin": "warfarin",
    "aspirin": "aspirin",
    "ecotrin": "aspirin",
    "sildenafil": "sildenafil",
    "intagra": "sildenafil",
    "lisinopril": "lisinopril",
    "metformin": "metformin",
    "comet": "metformin",
    # Psychiatric Doctor Handwriting Brands (Dr. Sanjay Kumar Singh & Regional Psychiatry)
    "aripax": "aripiprazole",
    "arepax": "aripiprazole",
    "axepox": "aripiprazole",
    "aripra": "aripiprazole",
    "asprito": "aripiprazole",
    "aripiprazole": "aripiprazole",
    "lupizep": "paroxetine",
    "lupizep-25": "paroxetine",
    "lupizep 25": "paroxetine",
    "lupizent": "paroxetine",
    "paroxetine": "paroxetine",
    "lonazep": "clonazepam",
    "lonazep-md": "clonazepam",
    "lonazep md": "clonazepam",
    "clonazepam": "clonazepam",
    "toficalm": "tofisopam",
    "tofcalm": "tofisopam",
    "tofisopam": "tofisopam",
    "carnisure": "levocarnitine",
    "camisure": "levocarnitine",
    "carnitor": "levocarnitine",
    "levocarnitine": "levocarnitine",
}


class RxHandBDDataset:
    def __init__(self, data_dir: str = RXHANDBD_DIR):
        self.data_dir = data_dir
        self.labels_map: Dict[str, str] = {}  # image_file -> label
        self.word_to_images: Dict[str, List[str]] = {}
        self.unique_vocabulary: List[str] = []
        self.is_loaded = False

    def load_dataset(self):
        """Loads Test_Labels.csv and Train_Label.csv from the extracted RxHandBD dataset."""
        label_files = [
            os.path.join(self.data_dir, "Test_Labels.csv"),
            os.path.join(self.data_dir, "Train_Label.csv"),
        ]

        found = False
        for fpath in label_files:
            if os.path.exists(fpath):
                found = True
                self._parse_csv(fpath)

        if not found or len(self.labels_map) == 0:
            logger.warning(f"No CSVs found in {self.data_dir}, using fallback RxHandBD map.")
            for brand, generic in RXHANDBD_TO_RXNORM.items():
                self.labels_map[f"{brand}.jpg"] = brand.capitalize()
                self.word_to_images.setdefault(brand.lower(), []).append(f"{brand}.jpg")

        self.unique_vocabulary = sorted(list(self.word_to_images.keys()))
        self.is_loaded = True
        logger.info(f"RxHandBD initialized: {len(self.labels_map)} images, {len(self.unique_vocabulary)} unique words.")

    def _parse_csv(self, fpath: str):
        try:
            with open(fpath, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        img_name = row[0].strip()
                        label = row[1].strip()
                        if label and label != "???":
                            self.labels_map[img_name] = label
                            self.word_to_images.setdefault(label.lower(), []).append(img_name)
        except Exception as e:
            logger.error(f"Error parsing RxHandBD CSV {fpath}: {e}")

    def get_featured_samples(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns representative actual handwritten prescription word images from RxHandBD."""
        featured = [
            {
                "image": "/rxhandbd/P1556.jpg",
                "label": "Nitrocontive",
                "mapped_generic": "nitroglycerin",
                "drug_class": "Nitrate Vasodilator",
                "risk_context": "Severe life-threatening hypotension if combined with Sildenafil / PDE5 inhibitors",
                "confidence": 0.88,
            },
            {
                "image": "/rxhandbd/P3234.jpg",
                "label": "Ciprox",
                "mapped_generic": "ciprofloxacin",
                "drug_class": "Fluoroquinolone Antibiotic",
                "risk_context": "Inhibits CYP1A2 / CYP3A4, sharp INR spike with Warfarin and Theophylline toxicity",
                "confidence": 0.84,
            },
            {
                "image": "/rxhandbd/P0004.jpg",
                "label": "Losita",
                "mapped_generic": "losartan",
                "drug_class": "Angiotensin II Receptor Blocker (ARB)",
                "risk_context": "Hyperkalemia with Spironolactone & Lithium toxicity risk",
                "confidence": 0.94,
            },
            {
                "image": "/rxhandbd/P0916.jpg",
                "label": "Seclo",
                "mapped_generic": "omeprazole",
                "drug_class": "Proton Pump Inhibitor (PPI)",
                "risk_context": "Inhibits CYP2C19 activation of Clopidogrel (Plavix)",
                "confidence": 0.95,
            },
            {
                "image": "/rxhandbd/P0001.jpg",
                "label": "Nexcital",
                "mapped_generic": "escitalopram",
                "drug_class": "Selective Serotonin Reuptake Inhibitor (SSRI)",
                "risk_context": "Serotonin syndrome with Tramadol / MAOIs; additive QTc prolongation with Amiodarone",
                "confidence": 0.92,
            },
            {
                "image": "/rxhandbd/P1105.jpg",
                "label": "Napa",
                "mapped_generic": "acetaminophen",
                "drug_class": "Analgesic / Antipyretic",
                "risk_context": "Generally safe; high cumulative doses (>2g/day) enhance Warfarin anticoagulation",
                "confidence": 0.96,
            },
            {
                "image": "/rxhandbd/P1106.jpg",
                "label": "Zimax",
                "mapped_generic": "azithromycin",
                "drug_class": "Macrolide Antibiotic",
                "risk_context": "QTc prolongation precautions with antiarrhythmics",
                "confidence": 0.89,
            },
            {
                "image": "/rxhandbd/P3851.jpg",
                "label": "Lasix",
                "mapped_generic": "furosemide",
                "drug_class": "Loop Diuretic",
                "risk_context": "Hypokalemia, nephrotoxicity with Aminoglycosides",
                "confidence": 0.91,
            },
            {
                "image": "/rxhandbd/P0359.jpg",
                "label": "Monas",
                "mapped_generic": "montelukast",
                "drug_class": "Leukotriene Receptor Antagonist",
                "risk_context": "Asthma and allergic rhinitis maintenance",
                "confidence": 0.93,
            },
            {
                "image": "/rxhandbd/P0280.jpg",
                "label": "Denvar",
                "mapped_generic": "cefixime",
                "drug_class": "Cephalosporin Antibiotic",
                "risk_context": "Third-generation cephalosporin antibacterial",
                "confidence": 0.87,
            },
        ]
        return featured[:limit]

    def resolve_rxhandbd_word(self, word: str) -> Optional[str]:
        """Maps an RxHandBD handwritten label to its standard RxNorm generic active ingredient."""
        w_clean = word.lower().strip()
        if w_clean in RXHANDBD_TO_RXNORM:
            return RXHANDBD_TO_RXNORM[w_clean]

        for brand, generic in RXHANDBD_TO_RXNORM.items():
            if brand in w_clean or w_clean in brand:
                return generic

        return None

    def match_handwritten_token(self, detected_text: str) -> Optional[Tuple[str, float]]:
        """
        Matches a raw or noisy handwritten token against RxHandBD vocabulary.
        Returns (resolved_label, confidence_score)
        """
        text_lower = detected_text.lower().strip()

        # Check known brand/generic map
        resolved = self.resolve_rxhandbd_word(text_lower)
        if resolved:
            return resolved.capitalize(), 0.95

        if text_lower in self.word_to_images:
            return text_lower.capitalize(), 1.0

        # Fuzzy matching
        from app.core.token_matcher import levenshtein_similarity
        best_match = None
        best_score = 0.0

        for vocab_word in list(self.word_to_images.keys())[:300]:
            sim = levenshtein_similarity(text_lower, vocab_word)
            if sim > best_score:
                best_score = sim
                best_match = vocab_word

        if best_score >= 0.75 and best_match:
            return best_match.capitalize(), round(best_score, 3)

        return None


# Global instance
rxhandbd_instance = RxHandBDDataset()
rxhandbd_instance.load_dataset()
