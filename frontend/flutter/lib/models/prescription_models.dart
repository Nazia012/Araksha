import 'dart:convert';

class OCRToken {
  String text;
  double confidence;
  List<double>? bbox;
  bool isVerified;

  OCRToken({
    required this.text,
    required this.confidence,
    this.bbox,
    this.isVerified = false,
  });

  bool get isUncertain => confidence < 0.80;

  Map<String, dynamic> toJson() => {
    'text': text,
    'confidence': confidence,
    'bbox': bbox,
  };

  factory OCRToken.fromJson(Map<String, dynamic> json) => OCRToken(
    text: json['text'] ?? '',
    confidence: (json['confidence'] ?? 0.9).toDouble(),
    bbox: json['bbox'] != null ? List<double>.from(json['bbox']) : null,
  );
}

class DetectedMedication {
  final String rawText;
  final String genericName;
  final String rxcui;
  final String drugClass;
  final List<String> brandNames;
  final String description;
  final double overallConfidence;
  final bool needsReview;

  DetectedMedication({
    required this.rawText,
    required this.genericName,
    required this.rxcui,
    required this.drugClass,
    required this.brandNames,
    required this.description,
    required this.overallConfidence,
    required this.needsReview,
  });

  factory DetectedMedication.fromJson(Map<String, dynamic> json) =>
      DetectedMedication(
        rawText: json['raw_text'] ?? '',
        genericName: json['generic_name'] ?? '',
        rxcui: json['rxcui'] ?? '',
        drugClass: json['drug_class'] ?? '',
        brandNames: List<String>.from(json['brand_names'] ?? []),
        description: json['description'] ?? '',
        overallConfidence: (json['overall_confidence'] ?? 1.0).toDouble(),
        needsReview: json['needs_review'] ?? false,
      );
}

class InteractionFlag {
  final String pair;
  final String severity;
  final String explanation;
  final String actionForPharmacist;

  InteractionFlag({
    required this.pair,
    required this.severity,
    required this.explanation,
    required this.actionForPharmacist,
  });

  factory InteractionFlag.fromJson(Map<String, dynamic> json) =>
      InteractionFlag(
        pair: json['pair'] ?? '',
        severity: json['severity'] ?? '',
        explanation: json['explanation'] ?? '',
        actionForPharmacist: json['action_for_pharmacist'] ?? '',
      );
}

class PrescriptionAnalysisReport {
  final String status;
  final String riskLevel; // 'Severe', 'Moderate', 'Clear'
  final String riskColor; // 'red', 'amber', 'green'
  final List<DetectedMedication> detectedMedications;
  final List<Map<String, dynamic>> verifiedDdis;
  final String patientSummary;
  final List<InteractionFlag> interactionFlags;
  final List<String> uncertainties;
  final List<String> pharmacistChecklist;
  final String disclaimer;

  PrescriptionAnalysisReport({
    required this.status,
    required this.riskLevel,
    required this.riskColor,
    required this.detectedMedications,
    required this.verifiedDdis,
    required this.patientSummary,
    required this.interactionFlags,
    required this.uncertainties,
    required this.pharmacistChecklist,
    required this.disclaimer,
  });

  factory PrescriptionAnalysisReport.fromJson(Map<String, dynamic> json) =>
      PrescriptionAnalysisReport(
        status: json['status'] ?? 'success',
        riskLevel: json['risk_level'] ?? 'Clear',
        riskColor: json['risk_color'] ?? 'green',
        detectedMedications: (json['detected_medications'] as List? ?? [])
            .map((m) => DetectedMedication.fromJson(m))
            .toList(),
        verifiedDdis: List<Map<String, dynamic>>.from(json['verified_ddis'] ?? []),
        patientSummary: json['patient_summary'] ?? '',
        interactionFlags: (json['interaction_flags'] as List? ?? [])
            .map((f) => InteractionFlag.fromJson(f))
            .toList(),
        uncertainties: List<String>.from(json['uncertainties'] ?? []),
        pharmacistChecklist:
            List<String>.from(json['pharmacist_checklist'] ?? []),
        disclaimer: json['disclaimer'] ?? '',
      );
}
