"""
Prescription Calibrator & Real Doctor Handwriting OCR Profile
Calibrated on Dr. Sanjay Kumar Singh (MD, Consultant Psychiatrist)
MVD Health Plus Multi Speciality Clinic, Guwahati, Assam
Patient: Nazia Parbat (20/F) | Date: 22/01/26
"""

from typing import Dict, List, Any

DR_SANJAY_PRESCRIPTION_PROFILE: Dict[str, Any] = {
    "prescription_id": "dr_sanjay_220126",
    "clinic_name": "MVD Health Plus Multi Speciality Clinic",
    "clinic_location": "Guwahati, Assam",
    "physician": {
        "name": "Dr. Sanjay Kumar Singh",
        "qualifications": "MBBS (AMC:20902), MD",
        "speciality": "Consultant Psychiatrist"
    },
    "patient": {
        "name": "Nazia Parbat",
        "age": 20,
        "gender": "Female",
        "date": "22/01/26"
    },
    "image_path": "/prescriptions/dr_sanjay_prescription.jpg",
    "handwritten_items": [
        {
            "line_number": 1,
            "raw_ocr_string": "Tab Aripax 10mg",
            "ocr_confidence": 0.92,
            "cer": 0.08,
            "crop_image": "/prescriptions/crops/line1_aripax.jpg",
            "dosage_schedule": "1 --------- 0 --------- 0 (Morning)",
            "standard_generic": "aripiprazole",
            "rxcui": "214199",
            "drug_class": "Atypical Antipsychotic / Mood Stabilizer",
            "plain_english_indication": "Mood stabilization and antipsychotic therapy",
            "gated_review": False
        },
        {
            "line_number": 2,
            "raw_ocr_string": "Tab Lupizep 25mg",
            "ocr_confidence": 0.88,
            "cer": 0.11,
            "crop_image": "/prescriptions/crops/line2_lupizep.jpg",
            "dosage_schedule": "0 --------- 0 --------- 1 (Night)",
            "standard_generic": "paroxetine",
            "co_ingredient": "clonazepam",
            "rxcui": "32937",
            "drug_class": "SSRI Antidepressant / Potent CYP2D6 Inhibitor",
            "plain_english_indication": "Depression, panic, and anxiety (contains Paroxetine + Clonazepam 0.5mg)",
            "gated_review": False
        },
        {
            "line_number": 3,
            "raw_ocr_string": "Tab Toficalm 50mg",
            "ocr_confidence": 0.90,
            "cer": 0.09,
            "crop_image": "/prescriptions/crops/line3_toficalm.jpg",
            "dosage_schedule": "1/2 --------- 0 --------- 1/2 (Morning & Night)",
            "standard_generic": "tofisopam",
            "rxcui": "10688",
            "drug_class": "2,3-Benzodiazepine Anxiolytic",
            "plain_english_indication": "Daytime anxiety relief without muscle weakness",
            "gated_review": False
        },
        {
            "line_number": 4,
            "raw_ocr_string": "Tab Lonazep MD",
            "ocr_confidence": 0.86,
            "cer": 0.12,
            "crop_image": "/prescriptions/crops/line4_lonazep.jpg",
            "dosage_schedule": "0 --------- 0 --------- 1 (8 PM at bedtime)",
            "standard_generic": "clonazepam",
            "rxcui": "2598",
            "drug_class": "Benzodiazepine Anticonvulsant / Anxiolytic",
            "plain_english_indication": "Nighttime sleep and panic control (Mouth-Dissolving)",
            "gated_review": False
        },
        {
            "line_number": 5,
            "raw_ocr_string": "Syr Carnisure 10ml",
            "ocr_confidence": 0.91,
            "cer": 0.07,
            "crop_image": "/prescriptions/crops/line5_carnisure.jpg",
            "dosage_schedule": "1 1/2 month review protocol",
            "standard_generic": "levocarnitine",
            "rxcui": "6324",
            "drug_class": "Mitochondrial & Cellular Nutrient",
            "plain_english_indication": "Cellular energy and metabolic support syrup",
            "gated_review": False
        }
    ],
    "clinical_risk_alerts": [
        {
            "pair": "Paroxetine + Aripiprazole",
            "severity": "Severe",
            "mechanism": "Paroxetine strongly inhibits CYP2D6 enzyme, causing a 2x-3x increase in Aripiprazole blood levels.",
            "plain_warning": "Paroxetine blocks how your liver breaks down Aripiprazole, which can cause severe restlessness (akathisia), tremors, and cardiac rhythm changes. Clinical guidelines recommend reducing the Aripiprazole dose by 50% when taken with Paroxetine."
        },
        {
            "pair": "Lupizep (Clonazepam) + Lonazep (Clonazepam)",
            "severity": "Severe",
            "mechanism": "Duplicate Benzodiazepine Therapy: Lupizep already contains Clonazepam 0.5mg, and Lonazep MD provides additional Clonazepam at 8 PM.",
            "plain_warning": "Duplicate Sedative Alert: Lupizep already has Clonazepam in it, and Lonazep is also Clonazepam. Taking both can cause heavy daytime sedation, confusion, and risk of falls."
        }
    ]
}
