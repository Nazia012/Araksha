import 'package:flutter/material.dart';
import '../models/prescription_models.dart';
import '../services/api_service.dart';
import 'interaction_report_screen.dart';

class OCRReviewChipsScreen extends StatefulWidget {
  final List<OCRToken> initialTokens;

  const OCRReviewChipsScreen({Key? key, required this.initialTokens}) : super(key: key);

  @override
  State<OCRReviewChipsScreen> createState() => _OCRReviewChipsScreenState();
}

class _OCRReviewChipsScreenState extends State<OCRReviewChipsScreen> {
  late List<OCRToken> _tokens;
  final ApiService _apiService = ApiService();
  bool _isLoading = false;
  String _errorMessage = '';

  final TextEditingController _addDrugController = TextEditingController();
  List<Map<String, dynamic>> _searchResults = [];
  bool _isSearching = false;

  @override
  void initState() {
    super.initState();
    _tokens = List.from(widget.initialTokens);
  }

  void _onEditToken(int index) {
    final token = _tokens[index];
    final controller = TextEditingController(text: token.text);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text('Edit Detected Token', style: TextStyle(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Original OCR Confidence: ${(token.confidence * 100).toInt()}%',
              style: TextStyle(
                color: token.isUncertain ? const Color(0xFFF59E0B) : const Color(0xFF10B981),
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: controller,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                filled: true,
                fillColor: const Color(0xFF0F172A),
                hintText: 'Enter corrected medication name',
                hintStyle: const TextStyle(color: Color(0xFF64748B)),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel', style: TextStyle(color: Color(0xFF94A3B8))),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0284C7)),
            onPressed: () {
              if (controller.text.trim().isNotEmpty) {
                setState(() {
                  _tokens[index].text = controller.text.trim();
                  _tokens[index].confidence = 1.0; // User confirmed
                  _tokens[index].isVerified = true;
                });
              }
              Navigator.pop(context);
            },
            child: const Text('Confirm', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  void _onRemoveToken(int index) {
    setState(() {
      _tokens.removeAt(index);
    });
  }

  Future<void> _searchRxNorm(String query) async {
    if (query.trim().isEmpty) {
      setState(() => _searchResults = []);
      return;
    }
    setState(() => _isSearching = true);
    try {
      final results = await _apiService.lookupDrugs(query);
      setState(() {
        _searchResults = results;
        _isSearching = false;
      });
    } catch (e) {
      setState(() => _isSearching = false);
    }
  }

  void _addMedicationFromSearch(Map<String, dynamic> med) {
    setState(() {
      _tokens.add(
        OCRToken(
          text: med['generic_name'],
          confidence: 1.0,
          isVerified: true,
        ),
      );
      _addDrugController.clear();
      _searchResults = [];
    });
  }

  Future<void> _submitForDDIAnalysis() async {
    if (_tokens.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please keep or add at least one medication to analyze.')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = '';
    });

    try {
      final report = await _apiService.processPrescription(
        tokens: _tokens,
        confidenceCutoff: 0.80,
      );

      setState(() => _isLoading = false);

      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => InteractionReportScreen(report: report),
        ),
      );
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final lowConfidenceCount = _tokens.where((t) => t.isUncertain && !t.isVerified).length;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: const Text('Review OCR Tokens', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Uncertainty Notice Banner if low confidence tokens present
                    if (lowConfidenceCount > 0)
                      Container(
                        padding: const EdgeInsets.all(12),
                        margin: const EdgeInsets.only(bottom: 16),
                        decoration: BoxDecoration(
                          color: const Color(0xFFF59E0B).withOpacity(0.12),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: const Color(0xFFF59E0B)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.warning_amber_rounded, color: Color(0xFFF59E0B), size: 24),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    '$lowConfidenceCount Token(s) Below 80% Confidence',
                                    style: const TextStyle(color: Color(0xFFF59E0B), fontWeight: FontWeight.bold, fontSize: 13),
                                  ),
                                  const SizedBox(height: 2),
                                  const Text(
                                    'Handwritten or noisy tokens are highlighted in amber. Tap chip to correct before verifying interactions.',
                                    style: TextStyle(color: Color(0xFFCBD5E1), fontSize: 11),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),

                    const Text(
                      'Detected Medication Tokens',
                      style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Tap any chip to correct OCR errors or remove false positives.',
                      style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
                    ),
                    const SizedBox(height: 14),

                    // OCR Review Chips
                    Wrap(
                      spacing: 8,
                      runSpacing: 10,
                      children: List.generate(_tokens.length, (index) {
                        final token = _tokens[index];
                        final isUncertain = token.isUncertain && !token.isVerified;

                        return GestureDetector(
                          onTap: () => _onEditToken(index),
                          child: Chip(
                            backgroundColor: isUncertain
                                ? const Color(0xFFF59E0B).withOpacity(0.18)
                                : const Color(0xFF1E293B),
                            side: BorderSide(
                              color: isUncertain ? const Color(0xFFF59E0B) : const Color(0xFF334155),
                              width: isUncertain ? 1.5 : 1,
                            ),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                            avatar: CircleAvatar(
                              backgroundColor: isUncertain ? const Color(0xFFF59E0B) : const Color(0xFF0284C7),
                              child: Icon(
                                isUncertain ? Icons.error_outline : Icons.check,
                                color: Colors.white,
                                size: 14,
                              ),
                            ),
                            label: Text(
                              '${token.text} (${(token.confidence * 100).toInt()}%)',
                              style: TextStyle(
                                color: isUncertain ? const Color(0xFFFDE68A) : Colors.white,
                                fontWeight: FontWeight.w600,
                                fontSize: 12,
                              ),
                            ),
                            deleteIcon: const Icon(Icons.close, size: 16, color: Color(0xFF94A3B8)),
                            onDeleted: () => _onRemoveToken(index),
                          ),
                        );
                      }),
                    ),

                    const SizedBox(height: 24),
                    const Divider(color: Color(0xFF334155)),
                    const SizedBox(height: 12),

                    // Add Medication / RxNorm Autocomplete Lookup
                    const Text(
                      'Add or Search Medication (RxNorm)',
                      style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    TextField(
                      controller: _addDrugController,
                      style: const TextStyle(color: Colors.white),
                      onChanged: _searchRxNorm,
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: const Color(0xFF1E293B),
                        hintText: 'Type brand or generic (e.g., Coumadin, Zestril, Advil)...',
                        hintStyle: const TextStyle(color: Color(0xFF64748B), fontSize: 13),
                        prefixIcon: const Icon(Icons.search, color: Color(0xFF38BDF8)),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(color: Color(0xFF334155)),
                        ),
                      ),
                    ),

                    // Autocomplete Search Results
                    if (_isSearching)
                      const Padding(
                        padding: EdgeInsets.all(12),
                        child: Center(child: CircularProgressIndicator(strokeWidth: 2)),
                      )
                    else if (_searchResults.isNotEmpty)
                      Container(
                        margin: const EdgeInsets.only(top: 8),
                        decoration: BoxDecoration(
                          color: const Color(0xFF1E293B),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: const Color(0xFF334155)),
                        ),
                        child: ListView.separated(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: _searchResults.length,
                          separatorBuilder: (context, _) => const Divider(color: Color(0xFF334155), height: 1),
                          itemBuilder: (context, index) {
                            final item = _searchResults[index];
                            return ListTile(
                              dense: true,
                              title: Text(
                                item['generic_name'].toString().toUpperCase(),
                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                              ),
                              subtitle: Text(
                                '${item['drug_class']} • RxCUI: ${item['rxcui']}',
                                style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11),
                              ),
                              trailing: const Icon(Icons.add_circle_outline, color: Color(0xFF38BDF8)),
                              onTap: () => _addMedicationFromSearch(item),
                            );
                          },
                        ),
                      ),

                    if (_errorMessage.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(top: 16),
                        child: Text(_errorMessage, style: const TextStyle(color: Colors.redAccent, fontSize: 12)),
                      ),
                  ],
                ),
              ),
            ),

            // Submit Button
            Padding(
              padding: const EdgeInsets.all(16),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0284C7),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  ),
                  icon: _isLoading
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                        )
                      : const Icon(Icons.shield_outlined, color: Colors.white),
                  label: Text(
                    _isLoading ? 'Verifying DDIs with Gemma 4...' : 'Verify DDIs & Generate Report',
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                  onPressed: _isLoading ? null : _submitForDDIAnalysis,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
