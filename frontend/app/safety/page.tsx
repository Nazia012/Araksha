export default function SafetyArchitecturePage() {
  return (
    <div className="page-container" style={{ maxWidth: '980px' }}>
      <div className="hero-banner" style={{ marginBottom: '2.5rem' }}>
        <div className="hero-tag">
          <span>🛡️ Clinical Guardrails & Architecture</span>
        </div>
        <h1 className="hero-title" style={{ fontSize: '2.3rem' }}>
          Deterministic Safety Engine & Gemma 4
        </h1>
        <p className="hero-desc">
          How our modular architecture guarantees clinical accuracy by decoupling database verification from language model generation.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {/* Principle 1 */}
        <div className="card-panel">
          <h2 style={{ fontSize: '1.25rem', color: '#38BDF8', marginBottom: '8px' }}>
            1. Zero LLM Hallucination Guarantee
          </h2>
          <p style={{ color: '#CBD5E1', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Large Language Models are prone to hallucinating interactions or omitting lethal contraindications.
            In this system, <strong>no interaction reaches Google Gemma 4 unless it is deterministically matched</strong> in
            our curated medical database (PostgreSQL / SQLite).
          </p>
          <div
            style={{
              background: '#0B1120',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #243454',
              marginTop: '12px',
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: '0.78rem',
              color: '#38BDF8',
            }}
          >
            SELECT drug_a, drug_b, severity, mechanism, recommendation<br />
            FROM drug_interactions<br />
            WHERE ((drug_a IN (:drugs) AND drug_b IN (:drugs))<br />
            &nbsp;&nbsp;&nbsp;OR (drug_b IN (:drugs) AND drug_a IN (:drugs)))<br />
            &nbsp;&nbsp;AND drug_a != drug_b;
          </div>
        </div>

        {/* Principle 2 */}
        <div className="card-panel">
          <h2 style={{ fontSize: '1.25rem', color: '#38BDF8', marginBottom: '8px' }}>
            2. Google Gemma 4 Plain-Language Translation
          </h2>
          <p style={{ color: '#CBD5E1', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Google Gemma 4 acts strictly as an empathetic clinical translator. Its task is to translate complex pharmacology
            (e.g., <em>CYP3A4 enzymatic inhibition</em>, <em>QTc interval prolongation</em>, <em>P-glycoprotein efflux transport</em>)
            into plain, calming, actionable patient language that anyone can understand.
          </p>
          <ul style={{ paddingLeft: '20px', color: '#94A3B8', fontSize: '0.85rem', marginTop: '10px', lineHeight: 1.7 }}>
            <li><strong>Constraint:</strong> Never diagnoses illnesses or conditions.</li>
            <li><strong>Constraint:</strong> Never prescribes medication or alters doses.</li>
            <li><strong>Constraint:</strong> Never suggests abruptly stopping medication.</li>
            <li><strong>Mandatory:</strong> Formulates a specific question for the patient to bring directly to their pharmacist.</li>
          </ul>
        </div>

        {/* Principle 3 */}
        <div className="card-panel">
          <h2 style={{ fontSize: '1.25rem', color: '#38BDF8', marginBottom: '8px' }}>
            3. On-Device OCR Confidence Gating (&lt; 80%)
          </h2>
          <p style={{ color: '#CBD5E1', fontSize: '0.9rem', lineHeight: 1.6 }}>
            Handwritten prescriptions can lead to OCR transcription mistakes. Our ingestion engine combines string distance
            and OCR recognition confidence. Any detected token scoring below <strong>80% confidence</strong> is flagged
            in amber and requires manual user confirmation before clinical review.
          </p>
        </div>

        {/* Architecture Diagram */}
        <div className="card-panel">
          <h2 style={{ fontSize: '1.25rem', color: '#38BDF8', marginBottom: '12px' }}>
            4. Modular Three-Tier Topology
          </h2>
          <div
            style={{
              background: '#0B1120',
              padding: '16px',
              borderRadius: '8px',
              border: '1px solid #243454',
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: '0.75rem',
              color: '#CBD5E1',
              lineHeight: 1.6,
            }}
          >
            [ Next.js Web Client / Flutter / React Native ]<br />
            &nbsp;&nbsp;│ (HTTP POST: Tokens + OCR Confidence)<br />
            &nbsp;&nbsp;▼<br />
            [ FastAPI Gateway on port 8000 ]<br />
            &nbsp;&nbsp;├─ Levenshtein &amp; RxNorm Standardizer<br />
            &nbsp;&nbsp;└─ Deterministic SQL Query Engine (SQLite / PostgreSQL)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│ (Verified Clinical Payload)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▼<br />
            [ Gemma 4 AI Inference Worker (Ollama / vLLM / LiteRT) ]<br />
            &nbsp;&nbsp;└─ Plain-Language Patient Summary + Pharmacist Checklist
          </div>
        </div>
      </div>
    </div>
  );
}
