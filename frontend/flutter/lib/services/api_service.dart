import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/prescription_models.dart';

class ApiService {
  // Configurable base URL: 10.0.2.2 for Android emulator, localhost for iOS simulator/web
  static const String defaultBaseUrl = 'http://127.0.0.1:8000';
  final String baseUrl;

  ApiService({this.baseUrl = defaultBaseUrl});

  /// Sends extracted tokens and/or manual medications to backend for deterministic DDI & Gemma 4 review
  Future<PrescriptionAnalysisReport> processPrescription({
    List<OCRToken>? tokens,
    String? rawText,
    List<String>? manualDrugs,
    double confidenceCutoff = 0.80,
  }) async {
    final uri = Uri.parse('$baseUrl/api/v1/prescriptions/process');
    final payload = {
      'tokens': tokens?.map((t) => t.toJson()).toList(),
      'raw_text': rawText,
      'manual_drugs': manualDrugs,
      'confidence_cutoff': confidenceCutoff,
    };

    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return PrescriptionAnalysisReport.fromJson(data);
    } else {
      throw Exception('Failed to analyze prescription: ${response.statusCode} ${response.body}');
    }
  }

  /// Autocomplete lookup against RxNorm database
  Future<List<Map<String, dynamic>>> lookupDrugs(String query) async {
    if (query.trim().isEmpty) return [];
    final uri = Uri.parse('$baseUrl/api/v1/drugs/lookup?q=${Uri.encodeComponent(query)}');
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<Map<String, dynamic>>.from(data['results'] ?? []);
    } else {
      throw Exception('Drug lookup failed: ${response.statusCode}');
    }
  }
}
