export type InteractionSeverity = "major" | "moderate" | "minor";

export interface BoundingBox {
  x: number;      // percentage 0-100
  y: number;      // percentage 0-100
  width: number;  // percentage 0-100
  height: number; // percentage 0-100
}

export interface ExtractedMedication {
  id: string;
  name: string;
  active_ingredient: string;
  dosage: string;
  frequency: string;
  confidence: number; // 0.0 - 1.0
  handwriting_uncertain: boolean;
  uncertainty_reason?: string;
  bounding_box?: BoundingBox;
  line_number?: number;
  route?: string;
  duration?: string;
}

export interface InteractionAlert {
  id: string;
  severity: InteractionSeverity;
  drugs_involved: [string, string];
  title: string;
  description: string;
  mechanism: string; // Biological mechanism
  citation_source: string; // e.g. "Verified against DrugBank / FDA guidelines"
  clinical_action: string;
  management_recommendation?: string;
}

export interface ScheduleItem {
  med: string;
  dose: string;
  instructions: string;
  with_food?: boolean;
}

export interface PatientSummary {
  headline: string;
  instructions: string;
  schedule: {
    morning: ScheduleItem[];
    afternoon: ScheduleItem[];
    night: ScheduleItem[];
    as_needed?: ScheduleItem[];
  };
  dietary_notes?: string[];
  clinical_disclaimer: string;
}

export interface PharmacistSignoff {
  signed_by: string;
  license_id: string;
  timestamp: string;
  notes?: string;
}

export interface AuditResponse {
  prescription_id: string;
  patient_masked_id: string;
  timestamp: string;
  edge_mode: boolean;
  pii_masked: boolean;
  model_runtime: string; // e.g. "Gemma-2B On-Device (WebGPU/NPU)"
  inference_latency_ms: number;
  overall_confidence: number;
  doctor_notes?: string;
  medications: ExtractedMedication[];
  interactions: InteractionAlert[];
  patient_summary: PatientSummary;
  status: "pending_review" | "confirmed_and_locked";
  pharmacist_signoff?: PharmacistSignoff;
  prescription_image_url?: string;
}
