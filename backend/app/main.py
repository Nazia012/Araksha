"""
Main FastAPI Application Entrypoint
Prescription & Drug Interaction Inspector Backend Gateway
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api.prescriptions import router as prescriptions_router
from app.api.drugs import router as drugs_router
from app.api.rxhandbd import router as rxhandbd_router
from app.api.pipeline import router as pipeline_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("prescription_inspector.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB tables and seed data
    logger.info("Initializing prescription database and seeding RxNorm / DDI tables...")
    try:
        init_db(seed_if_empty=True)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title="Prescription & Drug Interaction Inspector API",
    version="1.0.0",
    description=(
        "Modular Full-Stack Prescription & Drug Interaction Inspector using Google Gemma 4. "
        "Deterministically verifies Drug-Drug Interactions against medical databases "
        "and translates findings into safe, plain-language patient explanations."
    ),
    lifespan=lifespan
)

# Enable permissive CORS for mobile clients, web views, and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(prescriptions_router)
app.include_router(drugs_router)
app.include_router(rxhandbd_router)
app.include_router(pipeline_router)


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Prescription & Drug Interaction Inspector",
        "ai_engine": "Google Gemma 4 (via Ollama / vLLM / LiteRT)",
        "version": "1.0.0"
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Prescription & Drug Interaction Inspector Gateway is active.",
        "documentation": "/docs",
        "endpoints": [
            "POST /api/v1/prescriptions/process",
            "POST /api/v1/prescription/analyze",
            "GET /api/v1/drugs/lookup"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
