"""
Service connecting FastAPI backend to the Gemma 4 AI Inference Worker.
"""

import os
import sys

# Ensure ai_service is accessible in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from ai_service.gemma_client import GemmaClient

# Instantiate singleton client
gemma_client = GemmaClient(
    base_url=os.environ.get("GEMMA_API_URL", "http://ai_service:11434"),
    model_name=os.environ.get("GEMMA_MODEL", "gemma4:4b")
)


async def get_gemma_explanation(
    detected_medications: list,
    verified_interactions: list,
    uncertainties: list
) -> dict:
    """
    Invokes Gemma 4 with clinical payload and returns formatted patient explanations.
    """
    return await gemma_client.generate_patient_explanation(
        detected_medications=detected_medications,
        verified_interactions=verified_interactions,
        uncertainties=uncertainties
    )
