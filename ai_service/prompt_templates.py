"""
Gemma 4 System Prompt & Guardrail Templates
Enforces plain-language translation, empathy, uncertainty handling, and strict medical safety.
"""

GEMMA4_SYSTEM_PROMPT = """You are a specialized Clinical Communication Assistant powered by Google Gemma 4.
Your purpose is to translate verified pharmacological drug interaction findings into clear, empathetic, plain-language explanations for patients and caregivers.

CRITICAL MEDICAL SAFETY CONSTRAINTS:
1. NEVER DIAGNOSE illnesses or conditions.
2. NEVER PRESCRIBE medication or suggest dosage changes.
3. NEVER SUGGEST STOPPING any medication abruptly, as stopping prescribed medications without physician guidance can be life-threatening.
4. ONLY EXPLAIN INTERACTIONS that are explicitly provided in the input payload. Do not invent or hallucinate unverified interactions.
5. Translate complex biochemical jargon (e.g., 'CYP3A4 inhibition', 'QTc prolongation', 'P-gp efflux') into relatable, easy-to-understand concepts (e.g., 'slows down how the body clears the medicine', 'can affect heart rhythm').
6. Formulate precise, actionable questions the patient can bring directly to their licensed pharmacist or doctor.
7. Always maintain a calm, caring, and constructive tone.

OUTPUT FORMAT:
You MUST output ONLY a valid, raw JSON object matching this exact schema:
{
  "patient_summary": "Plain-language overview of prescribed drugs",
  "interaction_flags": [
    {
      "pair": "Drug A + Drug B",
      "severity": "Severe / Moderate / Mild",
      "explanation": "Simple, empathetic explanation of why they interact",
      "action_for_pharmacist": "Specific question the patient should ask their pharmacist"
    }
  ],
  "uncertainties": ["Flagged words or tokens that need manual verification by the pharmacist or patient"],
  "disclaimer": "This tool is for informational review and does not replace professional medical advice, diagnosis, or treatment. Always consult your prescribing doctor or pharmacist before making any changes."
}
"""


def load_n2c2_few_shot_examples() -> str:
    """Loads standardized n2c2 medication event few-shot demonstration examples."""
    import os
    import json
    json_path = os.path.join(os.path.dirname(__file__), "n2c2_few_shot.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                formatted = []
                for idx, ex in enumerate(data, 1):
                    formatted.append(
                        f"--- EXAMPLE {idx} (n2c2 Medication Event Ground Truth) ---\n"
                        f"Clinical Context: {ex.get('clinical_note')}\n"
                        f"TWOSIDES Verified DDI: {ex.get('twosides_verified_ddi', {}).get('pair')} "
                        f"({ex.get('twosides_verified_ddi', {}).get('severity')} - {ex.get('twosides_verified_ddi', {}).get('side_effect')})\n"
                        f"Gemma 4 Plain English Translation: {ex.get('gemma4_plain_english_summary')}\n"
                        f"Pharmacist Question: {ex.get('pharmacist_action')}\n"
                    )
                return "\n".join(formatted)
        except Exception:
            pass
    return ""


def build_gemma4_user_payload(
    detected_medications: list,
    verified_interactions: list,
    uncertainties: list
) -> str:
    """
    Constructs the structured clinical payload for Gemma 4 including n2c2 few-shot examples.
    """
    import json

    few_shot_context = load_n2c2_few_shot_examples()

    payload = {
        "context": "Stage 4: Gemma 4 Plain-Language Translation (n2c2-Guided)",
        "detected_medications": [
            {
                "name": med.get("generic_name", ""),
                "rxcui": med.get("rxcui", ""),
                "class": med.get("drug_class", ""),
                "confidence": med.get("overall_confidence", 1.0)
            }
            for med in detected_medications
        ],
        "twosides_verified_ddis": [
            {
                "pair": ddi.get("pair", ""),
                "severity": ddi.get("severity", ""),
                "side_effect": ddi.get("side_effect", "Clinical Interaction"),
                "clinical_mechanism": ddi.get("mechanism", ""),
                "clinical_recommendation": ddi.get("recommendation", "")
            }
            for ddi in verified_interactions
        ],
        "ocr_uncertainties_or_low_confidence": [
            u.get("token") if isinstance(u, dict) else str(u)
            for u in uncertainties
        ]
    }

    prompt_body = ""
    if few_shot_context:
        prompt_body += (
            "FEW-SHOT CONTEXT (From n2c2 Medication Event Annotations & TWOSIDES Database):\n"
            f"{few_shot_context}\n\n"
        )

    prompt_body += (
        "CURRENT PRESCRIPTION TO ANALYZE:\n"
        f"```json\n{json.dumps(payload, indent=2)}\n```\n\n"
        "Generate the plain-language patient summary, interaction flags with actionable pharmacist questions, "
        "uncertainties list, and safety disclaimer according to the system instructions. Output JSON ONLY."
    )

    return prompt_body
