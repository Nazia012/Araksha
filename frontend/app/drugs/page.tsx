'use client';

import { useState } from 'react';

const POPULAR_DRUGS = [
  {
    name: 'Warfarin',
    brand: 'Coumadin, Jantoven',
    class: 'Vitamin K Antagonist Anticoagulant',
    rxcui: '11289',
    risk: 'High Bleeding Risk with NSAIDs & Antiplatelets',
    dosages: '1mg, 2mg, 5mg, 10mg',
  },
  {
    name: 'Aspirin',
    brand: 'Bayer, Ecotrin',
    class: 'NSAID / Antiplatelet',
    rxcui: '1191',
    risk: 'Severe Bleeding when combined with Anticoagulants',
    dosages: '81mg, 325mg',
  },
  {
    name: 'Sildenafil',
    brand: 'Viagra, Revatio',
    class: 'PDE5 Inhibitor Vasodilator',
    rxcui: '36117',
    risk: 'Fatal Hypotension with Nitrates (Strict Contraindication)',
    dosages: '20mg, 50mg, 100mg',
  },
  {
    name: 'Nitroglycerin',
    brand: 'Nitrostat, Nitro-Dur',
    class: 'Nitrate Vasodilator',
    rxcui: '7435',
    risk: 'Synergistic cGMP Hypotension with PDE5 Inhibitors',
    dosages: '0.3mg, 0.4mg SL',
  },
  {
    name: 'Lisinopril',
    brand: 'Prinivil, Zestril',
    class: 'ACE Inhibitor Antihypertensive',
    rxcui: '29046',
    risk: 'Hyperkalemia with Spironolactone & Potassium',
    dosages: '5mg, 10mg, 20mg, 40mg',
  },
  {
    name: 'Spironolactone',
    brand: 'Aldactone',
    class: 'Potassium-Sparing Diuretic',
    rxcui: '9997',
    risk: 'Life-threatening Potassium elevation with ACEIs/ARBs',
    dosages: '25mg, 50mg, 100mg',
  },
  {
    name: 'Simvastatin',
    brand: 'Zocor',
    class: 'HMG-CoA Reductase Inhibitor (Statin)',
    rxcui: '36567',
    risk: 'Severe Rhabdomyolysis with Clarithromycin & Ketoconazole',
    dosages: '10mg, 20mg, 40mg',
  },
  {
    name: 'Clopidogrel',
    brand: 'Plavix',
    class: 'P2Y12 Antiplatelet',
    rxcui: '32968',
    risk: 'Attenuated efficacy with Omeprazole (CYP2C19 blockade)',
    dosages: '75mg, 300mg',
  },
  {
    name: 'Metformin',
    brand: 'Glucophage',
    class: 'Biguanide Antidiabetic',
    rxcui: '6809',
    risk: 'Renal monitoring required; avoid contrast media',
    dosages: '500mg, 850mg, 1000mg',
  },
  {
    name: 'Digoxin',
    brand: 'Lanoxin',
    class: 'Cardiac Glycoside Inotrope',
    rxcui: '3407',
    risk: 'Toxicity with Amiodarone, Clarithromycin & Verapamil',
    dosages: '0.125mg, 0.25mg',
  },
  {
    name: 'Lithium',
    brand: 'Lithobid',
    class: 'Mood Stabilizer',
    rxcui: '6448',
    risk: 'Toxic accumulation with NSAIDs & Thiazide Diuretics',
    dosages: '150mg, 300mg, 600mg',
  },
  {
    name: 'Tramadol',
    brand: 'Ultram',
    class: 'Opioid Analgesic / SNRI',
    rxcui: '10689',
    risk: 'Serotonin Syndrome & Seizure risk with SSRIs (Sertraline)',
    dosages: '50mg, 100mg',
  },
];

export default function DrugsCatalogPage() {
  const [query, setQuery] = useState('');
  const [selectedClass, setSelectedClass] = useState('All');

  const filtered = POPULAR_DRUGS.filter((d) => {
    const matchesQuery =
      d.name.toLowerCase().includes(query.toLowerCase()) ||
      d.brand.toLowerCase().includes(query.toLowerCase()) ||
      d.class.toLowerCase().includes(query.toLowerCase());
    const matchesClass = selectedClass === 'All' || d.class.includes(selectedClass);
    return matchesQuery && matchesClass;
  });

  return (
    <div className="page-container">
      <div className="hero-banner" style={{ marginBottom: '2rem' }}>
        <div className="hero-tag">
          <span>📚 RxNorm Standardized Dictionary</span>
        </div>
        <h1 className="hero-title" style={{ fontSize: '2.2rem' }}>
          Curated Medication & Interaction Catalog
        </h1>
        <p className="hero-desc">
          Browse standardized RxCUI medication records and verified interaction clinical profiles in the deterministic database.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
        <input
          type="text"
          className="search-input"
          style={{ flex: 1, minWidth: '280px' }}
          placeholder="Filter by drug name, brand (e.g. Coumadin, Plavix), or drug class..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select
          value={selectedClass}
          onChange={(e) => setSelectedClass(e.target.value)}
          style={{
            background: '#0F172A',
            color: '#fff',
            border: '1px solid #243454',
            borderRadius: '8px',
            padding: '10px 16px',
            fontSize: '0.85rem',
            cursor: 'pointer',
          }}
        >
          <option value="All">All Drug Classes</option>
          <option value="Anticoagulant">Anticoagulants</option>
          <option value="NSAID">NSAIDs & Antiplatelets</option>
          <option value="Vasodilator">Vasodilators & Nitrates</option>
          <option value="ACE Inhibitor">ACE Inhibitors</option>
          <option value="Diuretic">Diuretics</option>
          <option value="Statin">Statins</option>
        </select>
      </div>

      {/* Drug Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '1.25rem' }}>
        {filtered.map((drug, idx) => (
          <div key={idx} className="card-panel" style={{ padding: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#38BDF8' }}>{drug.name}</h3>
                <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Brands: {drug.brand}</span>
              </div>
              <span
                style={{
                  fontSize: '0.68rem',
                  fontWeight: 700,
                  background: 'rgba(2, 132, 199, 0.15)',
                  border: '1px solid rgba(56, 189, 248, 0.3)',
                  color: '#38BDF8',
                  padding: '3px 8px',
                  borderRadius: '6px',
                }}
              >
                RxCUI: {drug.rxcui}
              </span>
            </div>

            <div style={{ margin: '10px 0', fontSize: '0.82rem', color: '#CBD5E1' }}>
              <strong>Class:</strong> {drug.class}
            </div>

            <div
              style={{
                background: 'rgba(239, 68, 68, 0.1)',
                border: '1px solid rgba(239, 68, 68, 0.25)',
                borderRadius: '8px',
                padding: '8px 12px',
                fontSize: '0.78rem',
                color: '#FCA5A5',
              }}
            >
              ⚠️ <strong>Primary Risk:</strong> {drug.risk}
            </div>

            <div style={{ marginTop: '10px', fontSize: '0.72rem', color: '#64748B' }}>
              Common Dosages: {drug.dosages}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
