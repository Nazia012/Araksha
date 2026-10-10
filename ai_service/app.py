"""
AI Service Microservice Entrypoint (Optional Standalone Mode)
Wraps Gemma 4 inference with REST API.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ai_service.gemma_client import GemmaClient

app = FastAPI(
    title="Gemma 4 Clinical Explainer Microservice",
    description="Translates verified drug interactions into safe, plain-language patient summaries."
)

client = GemmaClient()


class ClinicalInferencePayload(BaseModel):
    detected_medications: List[Dict[str, Any]]
    verified_interactions: List[Dict[str, Any]]
    uncertainties: List[Any] = []


@app.post("/generate")
async def generate_explanation(payload: ClinicalInferencePayload):
    try:
        result = await client.generate_patient_explanation(
            detected_medications=payload.detected_medications,
            verified_interactions=payload.verified_interactions,
            uncertainties=payload.uncertainties
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine": "Google Gemma 4",
        "model": client.model_name
    }
