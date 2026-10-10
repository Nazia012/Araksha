# Araksha: Prescription & Drug Interaction Inspector using Google Gemma 4

**Araksha** is a modular three-tier clinical application (Next.js Frontend, FastAPI Backend Gateway, and Gemma 4 AI Inference Service) that scans prescriptions, tests handwriting OCR tolerance against doctor datasets (RxHandBD), verifies Drug-Drug Interactions (DDIs) deterministically against medical databases, and uses **Google Gemma 4** with few-shot clinical annotations (n2c2) to produce safe, clear, plain-language patient explanations.

---

## 🏛 Architecture & Component Breakdown

```
[ Frontend: Flutter / React Native ]
│  (HTTP / Multipart: Image + Confidences)
▼
┌────────────────────────────────────────────────────────┐
│            BACKEND API SERVICE (FastAPI)               │
│  - Endpoint: POST /api/v1/prescriptions/process        │
│  - Endpoint: POST /api/v1/prescription/analyze         │
│  - Endpoint: GET  /api/v1/drugs/lookup                 │
│  - Ingestion & OCR Post-processing                     │
│  - Fuzzy Match / Token Matcher (RxNorm Standard)       │
│  - Deterministic DDI Engine (PostgreSQL / SQLite)      │
└────────────────────────┬───────────────────────────────┘
│ Structured Clinical Payload
▼
┌────────────────────────────────────────────────────────┐
│             AI INFERENCE WORKER (Gemma 4)              │
│  - Model: Google Gemma 4 (E2B / E4B / 4B via Ollama /  │
│    vLLM / LiteRT-LM)                                   │
│  - System Prompt: Plain-language translation + Safety  │
│  - Enforces uncertainty scoring & medical disclaimer   │
└────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
prescription-inspector/
├── frontend/                     # Next.js Web Application
│   ├── app/                      # Next.js App Router (React 18 / TS)
│   │   ├── layout.tsx            # Global layout, Google fonts, Navbar
│   │   ├── globals.css           # Vanilla CSS design system & animations
│   │   ├── page.tsx              # Scanner Studio, OCR Chips & Gemma 4 Report
│   │   ├── drugs/page.tsx        # RxNorm Medication Database Catalog
│   │   └── safety/page.tsx       # Safety & Three-Tier Architecture Guide
│   ├── flutter/                  # Flutter Mobile Client (lib/ & pubspec.yaml)
│   ├── react_native/             # React Native (Expo) Client (App.tsx)
│   ├── next.config.js            # API proxy configuration
│   ├── package.json              # Next.js scripts & dependencies
│   └── tsconfig.json             # TypeScript config
├── backend/                      # FastAPI Gateway Application
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py               # FastAPI entrypoint, CORS, lifespan seeding
│   │   ├── api/
│   │   │   ├── prescriptions.py  # OCR processing, DDI engine, Gemma 4 dispatch
│   │   │   └── drugs.py          # RxNorm autocomplete lookup
│   │   ├── core/
│   │   │   ├── database.py       # SQLite / PostgreSQL deterministic query engine
│   │   │   └── token_matcher.py  # Fuzzy Levenshtein token matcher & OCR post-processing
│   │   ├── data/
│   │   │   ├── rxnorm_catalog.py    # Curated RxNorm generic & brand dictionary
│   │   │   └── interactions_seed.py # Top 100 Clinical DDI pairs seed
│   │   └── services/
│   │       └── gemma_service.py  # Connector to Gemma 4 AI service
│   └── tests/
│       ├── test_ddi_pipeline.py  # Pytest for RxNorm, DDI queries, Gemma schema
│       └── test_api_endpoints.py # FastAPI TestClient integration tests
├── ai_service/                   # Gemma 4 Runner (Ollama / vLLM wrapper)
│   ├── prompt_templates.py       # Safety system prompt & clinical payload formatting
│   ├── gemma_client.py           # HTTP client with Ollama & deterministic fallback
│   └── app.py                    # Standalone FastAPI microservice
└── docker-compose.yml            # Local orchestration (Backend, Gemma 4 AI, Postgres)
```

---

## 🩺 RxHandBD Dataset (Zenodo DOI: 10.5281/zenodo.18478741)

The system integrates the **RxHandBD** (Handwritten Prescription Word Image Dataset) by *Md Masudul Islam*:
- **Total Images:** 5,578 cropped handwritten words extracted from medical prescriptions.
- **Vocabulary:** 1,769 unique text entries covering doctor prescription handwriting, pharmaceutical brand names, dosages, and instructions.
- **Handwritten Image Detection:** Enables testing against real doctor handwriting samples (e.g. *Nitrocontive*, *Ciprox*, *Losita*, *Seclo*, *Nexcital*, *Napa*, *Zimax*, *Lasix*).
- **RxNorm Mapping:** Resolves regional and handwritten brand names to standard RxCUI ingredients for deterministic DDI verification.
2. **Role of Google Gemma 4:** Gemma 4 **only** explains interactions provided in the verified database payload. It translates clinical pharmacology into empathetic, plain-language patient summaries.
3. **Medical Safety Constraints:**
   - **Never diagnoses** illnesses or conditions.
   - **Never prescribes** or adjusts medication dosages.
   - **Never suggests stopping** medications abruptly.
   - Includes mandatory **medical disclaimer** and actionable questions for the pharmacist.

---

## 🚀 Quickstart Guide

### Option 1: Running with Docker Compose (Full Stack)

To run the Backend, PostgreSQL database, and Gemma 4 AI worker locally:

```bash
cd prescription-inspector
docker compose up --build
```

- **Backend API:** `http://localhost:8000`
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **Ollama Gemma 4 Service:** `http://localhost:11434`

To pull and run Gemma 4 in Ollama:
```bash
docker exec -it prescription_gemma_ai ollama run gemma4:4b
```

---

### Option 2: Running Locally with Python

1. **Install dependencies:**
   ```bash
   cd prescription-inspector/backend
   pip install -r requirements.txt
   ```

2. **Run automated test suite:**
   ```bash
   cd prescription-inspector
   pytest backend/tests/ -v
   ```

3. **Start the FastAPI backend:**
   ```bash
   cd prescription-inspector/backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Run the Next.js Frontend Website:**
   ```bash
   cd prescription-inspector/frontend
   npm run dev
   ```
   Open `http://localhost:3000` in your web browser.

---

## 📱 Mobile Client Screen Flow

1. **Screen 1: Camera Capture & Document Crop Guides**
   - Viewfinder with corner guides and document crop framing.
   - Real-time OCR bounding box overlay with confidence indicators.
   - One-tap clinical test presets:
     - *Warfarin + Aspirin (Severe Bleed Risk)*
     - *Sildenafil + Nitroglycerin (Fatal Vasodilator Risk)*
     - *Lisinopril + Spironolactone (Hyperkalemia RAAS Risk)*
     - *Metformin + Acetaminophen (Clear / Safe)*

2. **Screen 2: Review Detected Drugs & Confidence Chips**
   - Color-coded tokens: confidence < 80% flagged in **amber** with review prompt.
   - Tap-to-edit modal for correcting OCR handwriting errors.
   - Real-time RxNorm autocomplete search against `GET /api/v1/drugs/lookup`.

3. **Screen 3: Clinical Interaction Report**
   - **Color-coded Risk Alert:**
     - 🔴 **Red:** Severe DDI
     - 🟡 **Amber:** Moderate / Caution DDI
     - 🟢 **Green:** Clear
   - **Gemma 4 Plain-Language Summary:** Empathetic explanation of how the medicines interact.
   - **Verified Interaction Cards:** Clinical mechanism and direct question to ask the pharmacist.
   - **Expandable "Ask Your Pharmacist" Checklist:** Interactive checkable items.
   - **Medical Disclaimer Banner.**

---

## 📡 API Reference

### `POST /api/v1/prescriptions/process`
Processes raw OCR tokens or plain text and produces verified DDIs and Gemma 4 explanation.

**Request Body:**
```json
{
  "tokens": [
    { "text": "Warfrin 5mg", "confidence": 0.72 },
    { "text": "Aspirin 81mg", "confidence": 0.95 }
  ],
  "confidence_cutoff": 0.80
}
```

**Response:**
```json
{
  "status": "success",
  "risk_level": "Severe",
  "risk_color": "red",
  "detected_medications": [
    {
      "generic_name": "warfarin",
      "rxcui": "11289",
      "drug_class": "Vitamin K Antagonist Anticoagulant",
      "overall_confidence": 0.656,
      "needs_review": true
    },
    {
      "generic_name": "aspirin",
      "rxcui": "1191",
      "drug_class": "NSAID / Antiplatelet",
      "overall_confidence": 0.95,
      "needs_review": false
    }
  ],
  "verified_ddis": [
    {
      "pair": "Warfarin + Aspirin",
      "severity": "Severe",
      "mechanism": "Synergistic inhibition of coagulation factors and platelet aggregation...",
      "recommendation": "Avoid concurrent use unless strictly indicated.",
      "evidence_level": "FDA Black Box Warning"
    }
  ],
  "patient_summary": "This prescription contains 2 medications (Warfarin, Aspirin) with 1 verified interaction concern...",
  "interaction_flags": [
    {
      "pair": "Warfarin + Aspirin",
      "severity": "Severe",
      "explanation": "These two medications can interact in your body...",
      "action_for_pharmacist": "Ask your pharmacist: 'How can I safely schedule these medications to avoid unwanted interactions?'"
    }
  ],
  "uncertainties": [
    "'Warfrin' (confidence 65%): OCR or match confidence (65%) is below review threshold (80%)."
  ],
  "pharmacist_checklist": [
    "Verify low-confidence or handwritten prescription items with the pharmacy team.",
    "Discuss Warfarin + Aspirin (Severe interaction risk) and review recommended dosing intervals."
  ],
  "disclaimer": "This tool is for informational review and does not replace medical advice."
}
```

### `GET /api/v1/drugs/lookup?q=coumadin`
Returns autocomplete results with standardized generic name, RxCUI, brand names, and drug class.
>>>>>>> e3b9304 (Initial commit: Araksha - Prescription & Drug Interaction Inspector using Google Gemma 4)
