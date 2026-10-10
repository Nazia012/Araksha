"""
Gemma 4 Client & Inference Runner
Connects to Ollama / vLLM / LiteRT-LM inference containers running Google Gemma 4.
Includes robust JSON schema validation, retry logic, and safety fallback synthesizer.
"""

import os
import json
import re
import logging
from typing import Dict, Any, List, Optional
import httpx
from ai_service.prompt_templates import GEMMA4_SYSTEM_PROMPT, build_gemma4_user_payload

logger = logging.getLogger("prescription_inspector.gemma_client")

# Environment configurations
DEFAULT_OLLAMA_URL = os.environ.get("GEMMA_API_URL", "http://ai_service:11434")
DEFAULT_MODEL = os.environ.get("GEMMA_MODEL", "gemma4:4b")
INFERENCE_TIMEOUT = float(os.environ.get("GEMMA_TIMEOUT", "45.0"))


class GemmaClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout: float = INFERENCE_TIMEOUT
    ):
        self.base_url = (base_url or DEFAULT_OLLAMA_URL).rstrip("/")
        self.model_name = model_name or DEFAULT_MODEL
        self.timeout = timeout

    async def generate_patient_explanation(
        self,
        detected_medications: List[Dict[str, Any]],
        verified_interactions: List[Dict[str, Any]],
        uncertainties: List[Any]
    ) -> Dict[str, Any]:
        """
        Sends payload to Gemma 4 via Ollama or vLLM endpoint, or falls back safely
        to deterministic plain-language translation if the LLM container is offline.
        """
        prompt = build_gemma4_user_payload(detected_medications, verified_interactions, uncertainties)
        
        # 1. Attempt communication with Gemma 4 endpoint
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Ollama generate endpoint format
                ollama_payload = {
                    "model": self.model_name,
                    "prompt": f"{GEMMA4_SYSTEM_PROMPT}\n\n{prompt}",
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.2,
                        "top_p": 0.9,
                    }
                }

                logger.info(f"Dispatching clinical payload to Gemma 4 at {self.base_url}/api/generate...")
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=ollama_payload
                )

                if response.status_code == 200:
                    data = response.json()
                    raw_text = data.get("response", "")
                    parsed = self._extract_json(raw_text)
                    if parsed and self._validate_schema(parsed):
                        return parsed
                else:
                    # Also try standard OpenAI/vLLM /v1/chat/completions endpoint
                    chat_payload = {
                        "model": self.model_name,
                        "messages": [
                            {"role": "system", "content": GEMMA4_SYSTEM_PROMPT},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.2,
                        "response_format": {"type": "json_object"}
                    }
                    chat_res = await client.post(
                        f"{self.base_url}/v1/chat/completions",
                        json=chat_payload
                    )
                    if chat_res.status_code == 200:
                        chat_data = chat_res.json()
                        raw_text = chat_data["choices"][0]["message"]["content"]
                        parsed = self._extract_json(raw_text)
                        if parsed and self._validate_schema(parsed):
                            return parsed

        except Exception as e:
            logger.warning(f"Gemma 4 endpoint unreachable ({self.base_url}): {e}. Using deterministic safety synthesis engine.")

        # 2. Resilient Deterministic Fallback Synthesis
        return self._synthesize_safe_response(detected_medications, verified_interactions, uncertainties)

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Safely extracts JSON from model response even if surrounded by markdown."""
        if not text:
            return None
        text_clean = text.strip()
        # Remove markdown code fences if present
        json_match = re.search(r"\{.*\}", text_clean, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        try:
            return json.loads(text_clean)
        except json.JSONDecodeError:
            return None

    def _validate_schema(self, data: Dict[str, Any]) -> bool:
        """Validates that response satisfies the required output schema."""
        required_keys = ["patient_summary", "interaction_flags", "uncertainties", "disclaimer"]
        return all(key in data for key in required_keys)

    def _synthesize_safe_response(
        self,
        detected_medications: List[Dict[str, Any]],
        verified_interactions: List[Dict[str, Any]],
        uncertainties: List[Any]
    ) -> Dict[str, Any]:
        """
        Deterministic, empathetic clinical explainer generator that strictly
        mirrors Gemma 4's expected behavior when running locally or during cold start.
        """
        med_names = [m.get("generic_name", "").title() for m in detected_medications if m.get("generic_name")]
        med_count = len(med_names)

        if med_count == 0:
            summary = "No recognized medications were identified on this prescription."
        elif len(verified_interactions) == 0:
            summary = (
                f"We identified {med_count} medication{'s' if med_count > 1 else ''} "
                f"({', '.join(med_names)}). No verified dangerous interactions were detected "
                "between these medicines in standard clinical databases. Always follow your doctor's dosing instructions."
            )
        else:
            summary = (
                f"This prescription contains {med_count} medications ({', '.join(med_names)}) "
                f"with {len(verified_interactions)} verified interaction concern{'s' if len(verified_interactions) > 1 else ''}. "
                "These medications require coordinated timing or dosage supervision by your healthcare team to ensure safety."
            )

        interaction_flags = []
        for ddi in verified_interactions:
            pair = ddi.get("pair", "")
            severity = ddi.get("severity", "Moderate")
            mech = ddi.get("mechanism", "")
            rec = ddi.get("recommendation", "")

            # Translate mechanism into empathetic plain language
            if "bleeding" in mech.lower() or "hemorrhag" in mech.lower():
                plain_exp = (
                    f"Taking {pair} together can increase your risk of bleeding or bruising, "
                    "as both medicines impact blood clotting or stomach lining."
                )
                action = f"Ask your pharmacist: 'Are there safer pain relief options that do not increase my bleeding risk while on this medication?'"
            elif "hypotension" in mech.lower() or "blood pressure" in mech.lower():
                plain_exp = (
                    f"Combining {pair} can cause a rapid, excessive drop in your blood pressure, "
                    "which could cause severe dizziness, fainting, or stress on your heart."
                )
                action = f"Ask your pharmacist: 'How much time must I wait between taking these medicines to prevent dizzy spells or blood pressure drops?'"
            elif "potassium" in mech.lower() or "hyperkalemia" in mech.lower():
                plain_exp = (
                    f"Both medicines in {pair} cause your body to hold onto potassium, which can build up "
                    "to unsafe levels and affect your heart rhythm."
                )
                action = f"Ask your pharmacist: 'Will I need a blood test to check my potassium levels while taking these medications together?'"
            elif "serotonin" in mech.lower():
                plain_exp = (
                    f"Both {pair} elevate serotonin levels in the body. When combined, this can lead to "
                    "serotonin syndrome, causing tremors, agitation, or fever."
                )
                action = f"Ask your pharmacist: 'What early signs of serotonin reaction should I watch out for?'"
            elif "metabolism" in mech.lower() or "clearance" in mech.lower() or "cyp" in mech.lower():
                plain_exp = (
                    f"One of the medicines slows down how quickly your liver clears the other, "
                    "causing the medicine to build up in your body and increase side effects."
                )
                action = f"Ask your pharmacist: 'Does my dosage of either medicine need to be adjusted or spaced apart?'"
            else:
                plain_exp = (
                    f"These two medications can interact in your body. {mech} "
                    "Clinical guidelines recommend monitoring to keep you safe."
                )
                action = f"Ask your pharmacist: 'How can I safely schedule these medications to avoid unwanted interactions?'"

            interaction_flags.append({
                "pair": pair,
                "severity": severity,
                "explanation": plain_exp,
                "action_for_pharmacist": action
            })

        # Process uncertainties list
        uncertainty_tokens = []
        for u in uncertainties:
            if isinstance(u, dict):
                token = u.get("token", "")
                conf = u.get("confidence", 0.0)
                reason = u.get("reason", "Needs verification")
                uncertainty_tokens.append(f"'{token}' (confidence {int(conf * 100)}%): {reason}")
            else:
                uncertainty_tokens.append(str(u))

        return {
            "patient_summary": summary,
            "interaction_flags": interaction_flags,
            "uncertainties": uncertainty_tokens,
            "disclaimer": "This tool is for informational review and does not replace medical advice."
        }
