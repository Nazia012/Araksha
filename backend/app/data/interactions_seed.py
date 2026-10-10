"""
Top 100 Verified Drug-Drug Interaction (DDI) Seed Data
Compiled from RxNorm, openFDA, and National Library of Medicine (NLM) clinical references.
"""

from typing import List, Dict

INTERACTIONS_SEED: List[Dict[str, str]] = [
    # 1 - 10: Anticoagulants & Antiplatelets High Risk
    {
        "drug_a": "warfarin",
        "drug_b": "aspirin",
        "severity": "Severe",
        "mechanism": "Synergistic inhibition of coagulation factors and platelet aggregation, significantly degrading gastric mucosal defense.",
        "recommendation": "Avoid concurrent use unless strictly indicated (e.g. mechanical heart valves). Monitor INR closely and assess for occult bleeding.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "warfarin",
        "drug_b": "ibuprofen",
        "severity": "Severe",
        "mechanism": "NSAID causes gastric erosion and inhibits platelet COX-1 while displacing warfarin from plasma albumin, escalating hemorrhagic risk.",
        "recommendation": "Avoid combination. Substitute with acetaminophen for mild pain with short duration.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "warfarin",
        "drug_b": "clopidogrel",
        "severity": "Severe",
        "mechanism": "Dual antiplatelet and antithrombotic therapy results in marked potentiation of major systemic hemorrhage.",
        "recommendation": "Use minimal effective duration with gastroprotection (e.g., PPI). Frequent hemoglobin and hematocrit surveillance required.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "warfarin",
        "drug_b": "fluconazole",
        "severity": "Severe",
        "mechanism": "Potent inhibition of CYP2C9 enzyme reduces S-warfarin clearance, causing severe hypoprothrombinemia and INR spikes.",
        "recommendation": "Empirically reduce warfarin dose by 25-50% during fluconazole therapy and test INR at day 3 and day 7.",
        "evidence_level": "Well-documented / Pharmacokinetic"
    },
    {
        "drug_a": "warfarin",
        "drug_b": "ciprofloxacin",
        "severity": "Severe",
        "mechanism": "Inhibition of CYP1A2 and alteration of gut flora producing vitamin K causes supratherapeutic anticoagulation.",
        "recommendation": "Monitor INR within 48 to 72 hours of antimicrobial initiation. Adjust warfarin dosage as indicated.",
        "evidence_level": "Well-documented / Case Studies"
    },
    {
        "drug_a": "warfarin",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Inhibition of CYP2C9 and CYP3A4 substantially delays warfarin clearance, often doubling circulating levels.",
        "recommendation": "Proactively reduce warfarin maintenance dose by 30% to 50% upon initiating amiodarone.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "warfarin",
        "drug_b": "acetaminophen",
        "severity": "Moderate",
        "mechanism": "Toxic metabolite NAPQI inhibits vitamin K-dependent clotting factors at prolonged dosages exceeding 2g/day.",
        "recommendation": "Limit acetaminophen to under 2000mg/day. Monitor INR if taking regularly for more than 4 consecutive days.",
        "evidence_level": "Probable Clinical Evidence"
    },
    {
        "drug_a": "apixaban",
        "drug_b": "aspirin",
        "severity": "Severe",
        "mechanism": "Concurrent factor Xa inhibition and irreversible platelet COX-1 inhibition exponentially elevate fatal bleeding episodes.",
        "recommendation": "Avoid concomitant therapy unless clinically mandated following acute coronary syndrome or stent placement.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "rivaroxaban",
        "drug_b": "ibuprofen",
        "severity": "Severe",
        "mechanism": "Dual interference with primary and secondary hemostasis increases major gastrointestinal bleeding incidence.",
        "recommendation": "Contraindicated for routine analgesia. Select alternative non-ulcerogenic non-NSAID therapies.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "dabigatran",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Strong P-glycoprotein (P-gp) inhibition elevates dabigatran systemic absorption and peak concentrations.",
        "recommendation": "Reduce dabigatran dosage in renal impairment or select an alternate macrolide (e.g. azithromycin).",
        "evidence_level": "Well-documented / Pharmacokinetic"
    },

    # 11 - 20: Cardiovascular & RAAS / Electrolyte Interactions
    {
        "drug_a": "lisinopril",
        "drug_b": "spironolactone",
        "severity": "Severe",
        "mechanism": "Combined suppression of aldosterone secretion and renal potassium retention triggers life-threatening hyperkalemia.",
        "recommendation": "Check baseline serum potassium and creatinine within 1 week of combination. Educate patient on signs of cardiac arrhythmia.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "lisinopril",
        "drug_b": "potassium chloride",
        "severity": "Severe",
        "mechanism": "ACE inhibitor reduces urinary potassium excretion while exogenous potassium supplements rapidly elevate serum levels.",
        "recommendation": "Contraindicated unless hypokalemia is refractory and documented with continuous serial lab monitoring.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "lisinopril",
        "drug_b": "losartan",
        "severity": "Severe",
        "mechanism": "Dual RAAS blockade (ACE inhibitor + ARB) provides no additive benefit but spikes risk of syncope, hyperkalemia, and renal failure.",
        "recommendation": "Do not combine ACE inhibitors with ARBs. Discontinue one agent and titrate monotherapy.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "lisinopril",
        "drug_b": "ibuprofen",
        "severity": "Moderate",
        "mechanism": "NSAID inhibits renal prostaglandins causing afferent arteriolar vasoconstriction, blunting ACEI antihypertensive action and inducing acute kidney injury.",
        "recommendation": "Avoid chronic NSAIDs. Monitor blood pressure and renal panel if brief co-administration occurs.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "losartan",
        "drug_b": "spironolactone",
        "severity": "Severe",
        "mechanism": "Synergistic potassium retention downstream of angiotensin II blockade and aldosterone antagonism.",
        "recommendation": "Frequent electrolyte panel monitoring. Stop potassium supplements and avoid high-potassium salt substitutes.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "sildenafil",
        "drug_b": "nitroglycerin",
        "severity": "Severe",
        "mechanism": "Synergistic PDE5 inhibition and nitric oxide cGMP pathway activation cause profound, refractory systemic vasodilation and fatal hypotension.",
        "recommendation": "Strict absolute contraindication. Do not administer nitrates within 24 hours of sildenafil (48 hours for tadalafil).",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "tadalafil",
        "drug_b": "nitroglycerin",
        "severity": "Severe",
        "mechanism": "Sustained cGMP-mediated vascular smooth muscle relaxation produces irreversible cardiovascular collapse.",
        "recommendation": "Absolute contraindication. Minimum 48-hour washout required before any nitrate therapy.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "sildenafil",
        "drug_b": "isosorbide mononitrate",
        "severity": "Severe",
        "mechanism": "Combined cGMP amplification induces severe postural hypotension, myocardial infarction, and syncope.",
        "recommendation": "Concurrent use strictly contraindicated. Explore non-PDE5 alternatives for erectile dysfunction.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "tadalafil",
        "drug_b": "isosorbide mononitrate",
        "severity": "Severe",
        "mechanism": "Potent prolonged drop in systemic vascular resistance resulting in coronary hypoperfusion.",
        "recommendation": "Strictly contraindicated under all clinical circumstances.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "digoxin",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Amiodarone inhibits P-glycoprotein-mediated renal clearance, increasing serum digoxin concentrations by 70% to 100%.",
        "recommendation": "Immediately reduce digoxin dose by 50% upon starting amiodarone and monitor digoxin levels and ECG.",
        "evidence_level": "Established Clinical Trial"
    },

    # 21 - 30: Digoxin, Antiarrhythmics, Statins
    {
        "drug_a": "digoxin",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Elimination of gut flora (Eubacterium lentum) that metabolize digoxin plus P-gp transport inhibition spikes digoxin toxicity.",
        "recommendation": "Monitor for yellow/halo visual disturbances, bradycardia, and nausea. Lower digoxin dose and monitor serum levels.",
        "evidence_level": "Well-documented / Pharmacokinetic"
    },
    {
        "drug_a": "digoxin",
        "drug_b": "verapamil",
        "severity": "Severe",
        "mechanism": "Inhibition of tubular secretion and additive depression of AV node conduction can induce high-grade heart block.",
        "recommendation": "Reduce digoxin dosage by 25-50% and monitor heart rate and PR interval on ECG.",
        "evidence_level": "Well-documented / Pharmacokinetic"
    },
    {
        "drug_a": "digoxin",
        "drug_b": "diltiazem",
        "severity": "Moderate",
        "mechanism": "Additive negative dromotropic effects on the atrioventricular node and reduced digoxin clearance.",
        "recommendation": "Monitor resting heart rate. Watch for symptomatic bradycardia and syncope.",
        "evidence_level": "Probable Clinical Evidence"
    },
    {
        "drug_a": "clopidogrel",
        "drug_b": "omeprazole",
        "severity": "Moderate",
        "mechanism": "Omeprazole competitively inhibits CYP2C19, preventing bioactivation of clopidogrel into its active thiol metabolite.",
        "recommendation": "Consider substituting with pantoprazole or H2-receptor antagonists which exhibit negligible CYP2C19 inhibition.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "clopidogrel",
        "drug_b": "esomeprazole",
        "severity": "Moderate",
        "mechanism": "CYP2C19 inhibition attenuates antiplatelet efficacy of clopidogrel, elevating risk of recurrent ischemic stroke or MI.",
        "recommendation": "Switch gastroprotection to pantoprazole or famotidine.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "simvastatin",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Potent CYP3A4 inhibition elevates simvastatin AUC by up to 10-fold, inducing severe rhabdomyolysis and acute renal failure.",
        "recommendation": "Avoid combination. Temporarily withhold simvastatin during macrolide therapy or use azithromycin.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "atorvastatin",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "CYP3A4 inhibition increases atorvastatin exposure 3- to 4-fold, heightening risk of acute muscle breakdown.",
        "recommendation": "Limit atorvastatin dose to 20mg daily or suspend during the antibiotic course.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "simvastatin",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Amiodarone inhibits CYP3A4 metabolism of simvastatin, leading to cumulative statin toxicity and myopathy.",
        "recommendation": "Do not exceed simvastatin 20mg daily when co-prescribed with amiodarone.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "simvastatin",
        "drug_b": "amlodipine",
        "severity": "Moderate",
        "mechanism": "Amlodipine increases systemic simvastatin levels via weak CYP3A4 inhibition and P-gp modulation.",
        "recommendation": "Do not exceed simvastatin 20mg daily when taken concomitantly with amlodipine.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "atorvastatin",
        "drug_b": "gemfibrozil",
        "severity": "Severe",
        "mechanism": "Gemfibrozil inhibits statin glucuronidation (UGT1A1/1A3) and OATP1B1 hepatic uptake transporter, causing dramatic serum accumulation.",
        "recommendation": "Avoid concurrent use. Fenofibrate is preferred if fibrate-statin co-therapy is deemed essential.",
        "evidence_level": "FDA Warning"
    },

    # 31 - 40: Central Nervous System / Serotonin Syndrome / Psych
    {
        "drug_a": "sertraline",
        "drug_b": "tramadol",
        "severity": "Severe",
        "mechanism": "Dual serotonergic stimulation plus lowering of seizure threshold elevates risk of Serotonin Syndrome and convulsions.",
        "recommendation": "Monitor for hyperreflexia, clonus, tremors, and hyperthermia. Consider non-serotonergic analgesics.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "fluoxetine",
        "drug_b": "tramadol",
        "severity": "Severe",
        "mechanism": "Fluoxetine inhibits CYP2D6 conversion of tramadol while causing additive serotonin reuptake inhibition, provoking toxic serotonin crisis.",
        "recommendation": "Avoid combination. Titrate alternative multimodal non-serotonergic pain control.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "fluoxetine",
        "drug_b": "phenelzine",
        "severity": "Severe",
        "mechanism": "Concurrent MAO inhibition and SSRI administration prevents breakdown of serotonin, causing fatal hyperpyrexic Serotonin Syndrome.",
        "recommendation": "Absolute contraindication. Minimum 5-week washout required after fluoxetine before initiating any MAOI.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "sertraline",
        "drug_b": "phenelzine",
        "severity": "Severe",
        "mechanism": "Excess synaptic cleft serotonin accumulation leading to delirium, autonomic instability, and neuromuscular rigidity.",
        "recommendation": "Strict contraindication. Require at least a 14-day washout period between agents.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "citalopram",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Additive prolongation of cardiac myocyte repolarization (QTc interval), escalating risk of Torsades de Pointes and ventricular fibrillation.",
        "recommendation": "Avoid combination or limit citalopram to 20mg max with continuous baseline and periodic 12-lead ECG monitoring.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "escitalopram",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Synergistic cardiac hERG potassium channel blockade predisposing to lethal ventricular tachydysrhythmias.",
        "recommendation": "Perform baseline QTc measurement. Discontinue if QTc exceeds 500 ms.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "citalopram",
        "drug_b": "haloperidol",
        "severity": "Severe",
        "mechanism": "Dual potassium channel inhibition exacerbates cardiac repolarization delay and polymorphic ventricular tachycardia.",
        "recommendation": "Avoid concurrent use when possible. Perform routine electrolyte checks and ECG.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "sertraline",
        "drug_b": "linezolid",
        "severity": "Severe",
        "mechanism": "Linezolid possesses reversible, non-selective MAO-A inhibitory properties, precipitating acute serotonin toxicity.",
        "recommendation": "Unless urgent antibacterial therapy is required without alternatives, pause sertraline and monitor closely.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "lithium",
        "drug_b": "ibuprofen",
        "severity": "Severe",
        "mechanism": "NSAIDs decrease renal prostaglandin synthesis, lowering renal lithium clearance and elevating serum lithium to toxic thresholds.",
        "recommendation": "Avoid NSAID use in patients on lithium. Check lithium levels within 48 to 72 hours if co-prescribed.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "lithium",
        "drug_b": "hydrochlorothiazide",
        "severity": "Severe",
        "mechanism": "Thiazide diuretics cause proximal tubule sodium depletion, which reflexively triggers compensatory toxic lithium reabsorption.",
        "recommendation": "Reduce lithium dosage by up to 50% upon initiating thiazides; monitor serum lithium levels weekly.",
        "evidence_level": "Established Clinical Trial"
    },

    # 41 - 50: Methotrexate, Gout, Anticonvulsants, Antibiotics
    {
        "drug_a": "methotrexate",
        "drug_b": "ibuprofen",
        "severity": "Severe",
        "mechanism": "NSAIDs inhibit renal organic anion transporters (OAT1/OAT3) responsible for MTX elimination, resulting in severe pancytopenia and stomatitis.",
        "recommendation": "Avoid NSAIDs, especially with intermediate-to-high dose methotrexate regimens.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "methotrexate",
        "drug_b": "naproxen",
        "severity": "Severe",
        "mechanism": "Impaired glomerular filtration and competitive tubular secretion lead to lethal bone marrow suppression.",
        "recommendation": "Avoid combination. For arthritic inflammation, consult rheumatology for alternative biologic/DMARD therapies.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "allopurinol",
        "drug_b": "azathioprine",
        "severity": "Severe",
        "mechanism": "Allopurinol blocks xanthine oxidase, the primary metabolic inactivation pathway for 6-mercaptopurine/azathioprine, causing severe aplastic anemia.",
        "recommendation": "Mandatory 67% to 75% dose reduction of azathioprine with weekly complete blood counts.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "allopurinol",
        "drug_b": "mercaptopurine",
        "severity": "Severe",
        "mechanism": "Xanthine oxidase inhibition creates toxic accumulation of mercaptopurine with profound life-threatening myelosuppression.",
        "recommendation": "Reduce 6-MP dosage to 25-33% of standard dose and monitor hematologic parameters closely.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "theophylline",
        "drug_b": "ciprofloxacin",
        "severity": "Severe",
        "mechanism": "Ciprofloxacin inhibits hepatic CYP1A2, increasing theophylline systemic concentrations by up to 100-300%, triggering seizures.",
        "recommendation": "Reduce theophylline dose by 50% and track plasma theophylline concentrations regularly.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "carbamazepine",
        "drug_b": "fluconazole",
        "severity": "Severe",
        "mechanism": "Inhibition of CYP3A4 by fluconazole impairs carbamazepine breakdown, resulting in ataxia, nystagmus, and diplopia.",
        "recommendation": "Monitor carbamazepine serum concentrations and reduce dose if symptoms of neurotoxicity appear.",
        "evidence_level": "Well-documented / Pharmacokinetic"
    },
    {
        "drug_a": "carbamazepine",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Potent CYP3A4 inhibition abruptly halts carbamazepine metabolism, causing severe neurotoxicity and lethargy within 24-48 hours.",
        "recommendation": "Do not co-prescribe. Substitute clarithromycin with an alternate antibiotic class.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "phenytoin",
        "drug_b": "fluconazole",
        "severity": "Severe",
        "mechanism": "Fluconazole inhibits CYP2C9 and CYP2C19, sharply reducing saturable phenytoin clearance and driving toxic CNS levels.",
        "recommendation": "Check phenytoin plasma concentration; anticipate need for dose reduction.",
        "evidence_level": "Well-documented / Pharmacokinetic"
    },
    {
        "drug_a": "phenytoin",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "CYP2C9 inhibition decreases phenytoin metabolism, elevating risk of encephalopathy, ataxia, and gingival hyperplasia.",
        "recommendation": "Monitor free and total phenytoin levels; decrease phenytoin dosage proactively.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "levothyroxine",
        "drug_b": "calcium carbonate",
        "severity": "Moderate",
        "mechanism": "Calcium ions bind to levothyroxine in an acidic milieu, forming insoluble chelates that impair gastrointestinal absorption.",
        "recommendation": "Separate administration by at least 4 hours. Test TSH levels 6 to 8 weeks after starting co-therapy.",
        "evidence_level": "Established Clinical Trial"
    },

    # 51 - 60: Mineral binding, Sedatives & Opioids
    {
        "drug_a": "levothyroxine",
        "drug_b": "ferrous sulfate",
        "severity": "Moderate",
        "mechanism": "Insoluble ferric-thyroxine complex forms in the stomach, substantially reducing thyroid hormone bioavailability.",
        "recommendation": "Administer levothyroxine at least 4 hours before or after oral iron supplements.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "oxycodone",
        "drug_b": "alprazolam",
        "severity": "Severe",
        "mechanism": "Additive central nervous system and respiratory depression mediated through mu-opioid and GABA-A receptors, leading to coma and death.",
        "recommendation": "Avoid concurrent prescribing of opioids and benzodiazepines whenever possible. Co-prescribe naloxone.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "oxycodone",
        "drug_b": "diazepam",
        "severity": "Severe",
        "mechanism": "Synergistic sedation, profound hypoventilation, respiratory arrest, and cardiovascular collapse.",
        "recommendation": "Prescribe lowest effective dosages for shortest durations; furnish emergency naloxone rescue kits.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "oxycodone",
        "drug_b": "lorazepam",
        "severity": "Severe",
        "mechanism": "Profound respiratory depression and sedation from simultaneous central GABA-ergic and opioidergic enhancement.",
        "recommendation": "Limit combined therapy to specialized palliative settings with intensive respiration monitoring.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "hydrocodone",
        "drug_b": "alprazolam",
        "severity": "Severe",
        "mechanism": "Concurrent sedative effects precipitate severe hypoxemia, airway obstruction, and fatal respiratory depression.",
        "recommendation": "Avoid combination. Re-evaluate alternative non-sedating anxiolytic and non-opioid analgesic therapies.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "fentanyl",
        "drug_b": "alprazolam",
        "severity": "Severe",
        "mechanism": "Extremely high risk of fatal hypoventilation and coma due to high opioid potency paired with central GABA activation.",
        "recommendation": "Strictly avoid unless patient is intubated in an ICU / monitored anesthesia care unit.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "fentanyl",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Clarithromycin inhibits CYP3A4, substantially prolonging fentanyl clearance and precipitating opioid overdose toxicity.",
        "recommendation": "Carefully monitor for respiratory depression and sedated state; consider dosage reduction of fentanyl.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "gabapentin",
        "drug_b": "oxycodone",
        "severity": "Severe",
        "mechanism": "Additive central nervous system depressant action elevates risk of fatal respiratory depression even at therapeutic doses.",
        "recommendation": "Start with lowest possible doses; educate family and caregivers on recognizing signs of opioid toxidrome.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "pregabalin",
        "drug_b": "oxycodone",
        "severity": "Severe",
        "mechanism": "Dual neurological depression enhances somnolence, dizziness, respiratory insufficiency, and accidental falls.",
        "recommendation": "Exercise extreme caution; monitor respiratory function and advise against driving or machinery operation.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "gabapentin",
        "drug_b": "tramadol",
        "severity": "Moderate",
        "mechanism": "Synergistic sedation and psychomotor slowing; elevated risk of balance impairment and falls.",
        "recommendation": "Titrate cautiously in elderly populations. Instruct patient to avoid alcohol.",
        "evidence_level": "Probable Clinical Evidence"
    },

    # 61 - 70: Steroids, NSAIDs, Antidiabetics
    {
        "drug_a": "prednisone",
        "drug_b": "ibuprofen",
        "severity": "Severe",
        "mechanism": "Dual suppression of gastric prostaglandins and mucosal renewal causes up to 4- to 10-fold increase in peptic ulceration and GI bleeding.",
        "recommendation": "Avoid concurrent use. If mandatory, prescribe gastroprotective proton pump inhibitor (e.g. pantoprazole).",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "prednisone",
        "drug_b": "naproxen",
        "severity": "Severe",
        "mechanism": "Cumulative ulcerogenic action on stomach and duodenal mucosa leads to silent perforations and hematemesis.",
        "recommendation": "Avoid combination; monitor for black tarry stools, abdominal pain, or unexpected anemia.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "prednisone",
        "drug_b": "aspirin",
        "severity": "Severe",
        "mechanism": "Combined inhibition of gastric cytoprotective mucus coupled with antiplatelet effects escalates severe upper GI hemorrhage.",
        "recommendation": "Avoid combination or add definitive proton pump inhibitor gastroprotection.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "metformin",
        "drug_b": "hydrochlorothiazide",
        "severity": "Moderate",
        "mechanism": "Thiazides impair glucose tolerance, raising blood sugar while altering renal perfusion and metformin elimination.",
        "recommendation": "Monitor blood glucose closely and adjust metformin dosing as necessary.",
        "evidence_level": "Probable Clinical Evidence"
    },
    {
        "drug_a": "spironolactone",
        "drug_b": "potassium chloride",
        "severity": "Severe",
        "mechanism": "Potassium-sparing diuretic paired with exogenous potassium leads to acute fatal hyperkalemia and cardiac arrest.",
        "recommendation": "Contraindicated in routine clinical management unless severe documented potassium wasting is ongoing.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "diltiazem",
        "drug_b": "simvastatin",
        "severity": "Moderate",
        "mechanism": "Moderate CYP3A4 inhibition by diltiazem increases simvastatin peak concentration and AUC by several fold.",
        "recommendation": "Do not exceed simvastatin 10mg daily when taken with diltiazem.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "verapamil",
        "drug_b": "simvastatin",
        "severity": "Severe",
        "mechanism": "Verapamil inhibits CYP3A4 and P-gp, elevating simvastatin exposure and predisposing to severe myopathy.",
        "recommendation": "Limit simvastatin to maximum 10mg daily or switch to pravastatin/rosuvastatin.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "verapamil",
        "drug_b": "atorvastatin",
        "severity": "Moderate",
        "mechanism": "Inhibition of hepatic CYP3A4 elevates plasma atorvastatin levels and incidence of muscle pain.",
        "recommendation": "Monitor for unexplained muscle aches or weakness; maintain conservative atorvastatin dosing.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "amiodarone",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Concurrent administration yields marked additive QTc prolongation and CYP3A4 inhibition, risking polymorphic ventricular tachycardia.",
        "recommendation": "Contraindicated. Choose non-macrolide antibiotic alternatives for bacterial infections.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "haloperidol",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Clarithromycin inhibits CYP3A4 clearance of haloperidol and compounds cardiac QTc interval prolongation.",
        "recommendation": "Avoid combination due to heightened risk of fatal cardiac dysrhythmias.",
        "evidence_level": "FDA Warning"
    },

    # 71 - 80: Antifungals, Antibiotics, NSAID combinations
    {
        "drug_a": "ketoconazole",
        "drug_b": "simvastatin",
        "severity": "Severe",
        "mechanism": "Near-total shutdown of CYP3A4 metabolism causes massive 20-fold spike in simvastatin concentration, causing acute rhabdomyolysis.",
        "recommendation": "Absolute contraindication. Withhold statin completely for the entire antifungal duration.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "ketoconazole",
        "drug_b": "atorvastatin",
        "severity": "Severe",
        "mechanism": "Marked increase in circulating atorvastatin levels from CYP3A4 blockage triggers severe skeletal muscle toxicity.",
        "recommendation": "Avoid co-administration. If antifungal is essential, hold atorvastatin until course completion.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "fluconazole",
        "drug_b": "atorvastatin",
        "severity": "Moderate",
        "mechanism": "Moderate CYP3A4 inhibition increases statin exposure, elevating risk of elevated transaminases and myalgias.",
        "recommendation": "Monitor liver function tests and advise patient to report myalgia immediately.",
        "evidence_level": "Probable Clinical Evidence"
    },
    {
        "drug_a": "aspirin",
        "drug_b": "ibuprofen",
        "severity": "Moderate",
        "mechanism": "Ibuprofen competitively impedes aspirin from binding permanently to platelet COX-1, attenuating aspirin cardioprotective antiplatelet effect.",
        "recommendation": "Take immediate-release aspirin at least 30 to 120 minutes prior to ibuprofen ingestion.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "aspirin",
        "drug_b": "naproxen",
        "severity": "Moderate",
        "mechanism": "Naproxen interferes with the irreversible antiplatelet inhibition of low-dose cardioprotective aspirin while increasing GI bleed risk.",
        "recommendation": "Separate dosing times appropriately; assess cardiovascular vs gastrointestinal risk benefit.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "apixaban",
        "drug_b": "clarithromycin",
        "severity": "Moderate",
        "mechanism": "Dual inhibition of CYP3A4 and P-glycoprotein increases systemic apixaban exposure, increasing bleed rates.",
        "recommendation": "Consider apixaban dose reduction in patients with renal impairment receiving strong dual inhibitors.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "rivaroxaban",
        "drug_b": "clarithromycin",
        "severity": "Severe",
        "mechanism": "Potent P-gp and CYP3A4 inhibition significantly elevates rivaroxaban plasma levels and systemic bleeding events.",
        "recommendation": "Avoid concurrent therapy unless benefit outweighs hazard; monitor for hemorrhage.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "dabigatran",
        "drug_b": "verapamil",
        "severity": "Moderate",
        "mechanism": "P-glycoprotein transport inhibition by verapamil increases dabigatran bioavailability.",
        "recommendation": "Administer dabigatran at least 2 hours before verapamil when co-prescribed.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "clopidogrel",
        "drug_b": "fluconazole",
        "severity": "Moderate",
        "mechanism": "Inhibition of CYP2C19 diminishes biotransformation of clopidogrel to its active antiplatelet compound.",
        "recommendation": "Use alternate antifungal therapy (e.g. nystatin or micafungin) where possible.",
        "evidence_level": "Pharmacokinetic Trial"
    },
    {
        "drug_a": "spironolactone",
        "drug_b": "ibuprofen",
        "severity": "Moderate",
        "mechanism": "NSAID-induced prostaglandin inhibition decreases natriuretic and antihypertensive efficacy of spironolactone while increasing hyperkalemia risk.",
        "recommendation": "Monitor blood pressure and serum potassium regularly.",
        "evidence_level": "Well-documented"
    },

    # 81 - 90: Diuretics, Lithium, Antidepressants, Opioids
    {
        "drug_a": "hydrochlorothiazide",
        "drug_b": "ibuprofen",
        "severity": "Moderate",
        "mechanism": "Prostaglandin synthesis inhibition counteracts the diuretic, natriuretic, and blood pressure-lowering response to hydrochlorothiazide.",
        "recommendation": "Monitor blood pressure closely; watch for peripheral fluid retention.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "lithium",
        "drug_b": "lisinopril",
        "severity": "Severe",
        "mechanism": "ACE inhibitor-induced renal vasodilation reduces glomerular filtration rate and sodium excretion, causing toxic lithium retention.",
        "recommendation": "Check serum lithium level within 3-5 days of initiating lisinopril; adjust lithium dosage down.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "lithium",
        "drug_b": "losartan",
        "severity": "Severe",
        "mechanism": "Angiotensin II receptor blockade decreases renal clearance of lithium, elevating risk of neurotoxicity and renal damage.",
        "recommendation": "Frequent lithium monitoring; instruct patient on tremors, slurred speech, and ataxia.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "theophylline",
        "drug_b": "clarithromycin",
        "severity": "Moderate",
        "mechanism": "Macrolide inhibition of hepatic CYP3A4 elevates theophylline concentrations by 20-40%.",
        "recommendation": "Check theophylline serum level; adjust dosage to stay within the 5-15 mcg/mL target range.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "tramadol",
        "drug_b": "alprazolam",
        "severity": "Severe",
        "mechanism": "Combined opioid-like CNS depression and benzodiazepine action increases risk of severe sedation and respiratory depression.",
        "recommendation": "Restrict combination; counsel patients on profound sedation and motor impairment.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "tramadol",
        "drug_b": "citalopram",
        "severity": "Severe",
        "mechanism": "Additive serotonergic tone and reduced seizure threshold predisposing to seizures and Serotonin Syndrome.",
        "recommendation": "Monitor for agitation, tachycardia, hyperthermia, and tremor. Avoid in patients with history of seizures.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "tramadol",
        "drug_b": "escitalopram",
        "severity": "Severe",
        "mechanism": "Enhanced synaptic serotonin levels from combined reuptake inhibition and tramadol-mediated release.",
        "recommendation": "Exercise vigilance for signs of serotonin toxicity. Seek safer analgesic alternatives.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "carbamazepine",
        "drug_b": "warfarin",
        "severity": "Severe",
        "mechanism": "Carbamazepine powerfully induces CYP2C9 and CYP3A4, dramatically accelerating warfarin metabolism and dropping INR levels.",
        "recommendation": "Double-check INR frequently; anticipates substantial warfarin dose increases to maintain therapeutic anticoagulation.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "phenytoin",
        "drug_b": "warfarin",
        "severity": "Severe",
        "mechanism": "Biphasic interaction: initial protein binding displacement causes transient INR spike, followed by enzyme induction lowering INR.",
        "recommendation": "Frequent serial INR and free phenytoin measurements are essential.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "carbamazepine",
        "drug_b": "apixaban",
        "severity": "Severe",
        "mechanism": "Strong induction of CYP3A4 and P-gp drastically decreases plasma apixaban concentrations by over 50%, risking thrombotic stroke.",
        "recommendation": "Avoid combination. Direct oral anticoagulants should not be co-administered with strong P-gp/CYP inducers.",
        "evidence_level": "FDA Black Box Warning"
    },

    # 91 - 100: Miscellaneous High-Impact Combinations
    {
        "drug_a": "carbamazepine",
        "drug_b": "rivaroxaban",
        "severity": "Severe",
        "mechanism": "Potent metabolic induction reduces rivaroxaban AUC by ~50%, compromising protection against pulmonary embolism and stroke.",
        "recommendation": "Avoid combination. Switch to an alternative anticoagulant or non-inducing anticonvulsant.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "carbamazepine",
        "drug_b": "tramadol",
        "severity": "Moderate",
        "mechanism": "Enzyme induction lowers tramadol analgesic efficacy while lowering seizure threshold synergistically.",
        "recommendation": "Consider non-opioid or alternative analgesics; avoid tramadol in patients on antiepileptics.",
        "evidence_level": "Probable Clinical Evidence"
    },
    {
        "drug_a": "ciprofloxacin",
        "drug_b": "prednisone",
        "severity": "Severe",
        "mechanism": "Synergistic degradation of tenocyte extracellular matrix drastically escalates risk of severe tendon rupture (especially Achilles tendon).",
        "recommendation": "Avoid combination, especially in elderly or athletic patients. Discontinue immediately if pain, swelling, or tenderness develops.",
        "evidence_level": "FDA Black Box Warning"
    },
    {
        "drug_a": "ciprofloxacin",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Additive blockade of myocardial potassium rectifying channels creates marked QTc prolongation and Torsades de Pointes risk.",
        "recommendation": "Avoid combination; evaluate alternative non-quinolone antibacterial regimens.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "methotrexate",
        "drug_b": "aspirin",
        "severity": "Severe",
        "mechanism": "Salicylates displace methotrexate from plasma albumin and diminish renal excretion, elevating MTX toxicity.",
        "recommendation": "Avoid combining high or intermediate dose methotrexate with aspirin.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "allopurinol",
        "drug_b": "warfarin",
        "severity": "Moderate",
        "mechanism": "Allopurinol may inhibit hepatic microsomal enzymes that metabolize warfarin, potentiating the hypoprothrombinemic effect.",
        "recommendation": "Monitor INR upon beginning or discontinuing allopurinol therapy.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "metformin",
        "drug_b": "cimetidine",
        "severity": "Moderate",
        "mechanism": "Competition for renal organic cation transport (OCT2) increases circulating metformin concentrations, raising lactic acidosis risk.",
        "recommendation": "Substitute cimetidine with famotidine or a proton pump inhibitor.",
        "evidence_level": "Established Clinical Trial"
    },
    {
        "drug_a": "digoxin",
        "drug_b": "spironolactone",
        "severity": "Moderate",
        "mechanism": "Spironolactone decreases renal and non-renal clearance of digoxin while falsely elevating some digoxin immunoassays.",
        "recommendation": "Monitor clinical symptoms and obtain verified digoxin assay after steady state is reached.",
        "evidence_level": "Well-documented"
    },
    {
        "drug_a": "diltiazem",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Profound synergistic suppression of sinus node automaticity and AV nodal conduction causing sinus arrest and severe bradycardia.",
        "recommendation": "Use combination only under telemetry monitoring with pacemaker availability.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "verapamil",
        "drug_b": "amiodarone",
        "severity": "Severe",
        "mechanism": "Concurrent calcium channel and multivalent antiarrhythmic blockade causes synergistic cardiac depression, AV block, and hypotension.",
        "recommendation": "Avoid simultaneous use unless specialized electrophysiologist supervision is in place.",
        "evidence_level": "FDA Warning"
    },
    {
        "drug_a": "paroxetine",
        "drug_b": "aripiprazole",
        "severity": "Severe",
        "mechanism": "Paroxetine is a potent CYP2D6 inhibitor that blocks liver metabolism of aripiprazole, leading to a 2- to 3-fold elevation in aripiprazole serum levels and heightened toxicity.",
        "recommendation": "Reduce aripiprazole dose by 50% when co-administered with paroxetine. Monitor closely for akathisia (severe motor restlessness), tremors, parkinsonism, and QTc prolongation.",
        "evidence_level": "FDA Black Box Label / Pharmacokinetic Study"
    },
    {
        "drug_a": "paroxetine",
        "drug_b": "clonazepam",
        "severity": "Moderate",
        "mechanism": "Additive central nervous system depression and psychomotor slowing. Lupizep contains both paroxetine and clonazepam; co-prescribing additional clonazepam leads to duplicate benzodiazepine exposure.",
        "recommendation": "Verify whether duplicate benzodiazepine therapy (Lupizep containing clonazepam + separate Lonazep) was intentional. Assess patient for excessive daytime drowsiness, falls, and respiratory depression.",
        "evidence_level": "Clinical Pharmacovigilance / Alert"
    },
    {
        "drug_a": "clonazepam",
        "drug_b": "tofisopam",
        "severity": "Moderate",
        "mechanism": "Dual benzodiazepine receptor modulation. Clonazepam acts on central GABA-A classical sites, while tofisopam acts as a 2,3-benzodiazepine, compounding central sedation and dizziness.",
        "recommendation": "Advise patient to take doses at separated times and exercise caution when driving or walking on stairs.",
        "evidence_level": "Pharmacological Mechanism Study"
    }
]
