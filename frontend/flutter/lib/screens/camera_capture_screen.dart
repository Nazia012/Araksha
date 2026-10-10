import 'package:flutter/material.dart';
import '../models/prescription_models.dart';
import 'ocr_review_chips_screen.dart';

class CameraCaptureScreen extends StatefulWidget {
  const CameraCaptureScreen({Key? key}) : super(key: key);

  @override
  State<CameraCaptureScreen> createState() => _CameraCaptureScreenState();
}

class _CameraCaptureScreenState extends State<CameraCaptureScreen> {
  bool _isProcessing = false;

  // Sample prescription test presets to simulate instant document capture
  final List<Map<String, dynamic>> _samplePrescriptions = [
    {
      'title': 'High Risk Hemorrhage Case',
      'desc': 'Warfarin (Blood thinner) + Aspirin (Pain/Cardio)',
      'tokens': [
        OCRToken(text: 'Warfrin 5mg', confidence: 0.72), // Low confidence <80%
        OCRToken(text: 'Aspirin 81mg', confidence: 0.94),
        OCRToken(text: 'Sig: 1 tab daily', confidence: 0.98),
      ],
    },
    {
      'title': 'Fatal Vasodilator Interaction',
      'desc': 'Sildenafil (Viagra) + Nitroglycerin (Angina)',
      'tokens': [
        OCRToken(text: 'Sildenafil 50mg', confidence: 0.95),
        OCRToken(text: 'Nitroglycerin 0.4mg SL', confidence: 0.88),
      ],
    },
    {
      'title': 'Hyperkalemia RAAS Risk',
      'desc': 'Lisinopril + Spironolactone',
      'tokens': [
        OCRToken(text: 'Lisinopril 20mg', confidence: 0.91),
        OCRToken(text: 'Spironolactne 25mg', confidence: 0.76), // Typo & <80%
      ],
    },
    {
      'title': 'Safe / No Known Interaction',
      'desc': 'Metformin (Diabetes) + Acetaminophen (Tylenol)',
      'tokens': [
        OCRToken(text: 'Metformin 500mg', confidence: 0.96),
        OCRToken(text: 'Acetaminophen 650mg', confidence: 0.92),
      ],
    },
  ];

  void _onCaptureDocument(List<OCRToken> tokens) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => OCRReviewChipsScreen(initialTokens: tokens),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: const Color(0xFF38BDF8).withOpacity(0.15),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.medication, color: Color(0xFF38BDF8), size: 22),
            ),
            const SizedBox(width: 10),
            const Text(
              'Prescription Inspector',
              style: TextStyle(fontWeight: FontWeight.w700, fontSize: 18, color: Colors.white),
            ),
          ],
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Camera viewfinder simulation with document crop guides
            Expanded(
              flex: 5,
              child: Container(
                margin: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: const Color(0xFF334155), width: 1.5),
                ),
                child: Stack(
                  children: [
                    // Mock Document inside frame
                    Center(
                      child: Container(
                        width: MediaQuery.of(context).size.width * 0.78,
                        height: MediaQuery.of(context).size.height * 0.38,
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: const Color(0xFF0F172A).withOpacity(0.85),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: const Color(0xFF38BDF8).withOpacity(0.7),
                            width: 2,
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  children: const [
                                    Icon(Icons.local_hospital, color: Color(0xFF38BDF8), size: 18),
                                    SizedBox(width: 6),
                                    Text(
                                      'Rx MEDICAL CLINIC',
                                      style: TextStyle(
                                        color: Colors.white70,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 12,
                                        letterSpacing: 1.1,
                                      ),
                                    ),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: Colors.green.withOpacity(0.2),
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: const Text('READY', style: TextStyle(color: Colors.greenAccent, fontSize: 10, fontWeight: FontWeight.bold)),
                                ),
                              ],
                            ),
                            const Divider(color: Color(0xFF334155), height: 24),
                            // Simulated Prescription Text lines
                            _buildDocLine('Patient: Jane Doe', 'DOB: 1980-04-12'),
                            const SizedBox(height: 12),
                            _buildBoundingBoxSnippet('Rx 1: Warfarin 5mg PO Daily', 0.72),
                            const SizedBox(height: 8),
                            _buildBoundingBoxSnippet('Rx 2: Aspirin 81mg PO Daily', 0.94),
                            const Spacer(),
                            const Center(
                              child: Text(
                                'Align prescription paper within frame',
                                style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                    // Crop Guide Corner Markers
                    _buildCornerMarker(Alignment.topLeft),
                    _buildCornerMarker(Alignment.topRight),
                    _buildCornerMarker(Alignment.bottomLeft),
                    _buildCornerMarker(Alignment.bottomRight),

                    // ML Kit OCR Status Pill
                    Positioned(
                      top: 16,
                      left: 0,
                      right: 0,
                      child: Center(
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                          decoration: BoxDecoration(
                            color: const Color(0xFF0F172A).withOpacity(0.9),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: const Color(0xFF38BDF8).withOpacity(0.4)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: const [
                              Icon(Icons.document_scanner, color: Color(0xFF38BDF8), size: 16),
                              SizedBox(width: 8),
                              Text(
                                'Google ML Kit OCR Ready (Confidence Filter < 80%)',
                                style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w500),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Prescription Presets for Instant One-Tap Testing
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: const [
                  Icon(Icons.flash_on, color: Color(0xFFF59E0B), size: 16),
                  SizedBox(width: 6),
                  Text(
                    'Instant Clinical Presets',
                    style: TextStyle(color: Color(0xFFCBD5E1), fontSize: 13, fontWeight: FontWeight.w600),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 72,
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                scrollDirection: Axis.horizontal,
                itemCount: _samplePrescriptions.length,
                itemBuilder: (context, index) {
                  final preset = _samplePrescriptions[index];
                  return GestureDetector(
                    onTap: () => _onCaptureDocument(preset['tokens']),
                    child: Container(
                      width: 220,
                      margin: const EdgeInsets.only(right: 12),
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: const Color(0xFF1E293B),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: const Color(0xFF334155)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            preset['title'],
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 3),
                          Text(
                            preset['desc'],
                            style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),

            const SizedBox(height: 12),

            // Capture & Gallery Action Buttons
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        side: const Border.all(color: Color(0xFF38BDF8)),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.photo_library, color: Color(0xFF38BDF8)),
                      label: const Text('Pick Image', style: TextStyle(color: Color(0xFF38BDF8), fontWeight: FontWeight.bold)),
                      onPressed: () {
                        // Open preset 1 as simulated photo scan
                        _onCaptureDocument(_samplePrescriptions[0]['tokens']);
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 2,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF0284C7),
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.camera_alt, color: Colors.white),
                      label: const Text('Capture & Scan OCR', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      onPressed: () {
                        _onCaptureDocument(_samplePrescriptions[0]['tokens']);
                      },
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDocLine(String left, String right) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(left, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
        Text(right, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
      ],
    );
  }

  Widget _buildBoundingBoxSnippet(String text, double conf) {
    final bool isLow = conf < 0.80;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: isLow ? const Color(0xFFF59E0B).withOpacity(0.12) : const Color(0xFF10B981).withOpacity(0.12),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(
          color: isLow ? const Color(0xFFF59E0B) : const Color(0xFF10B981),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(text, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600)),
          Text(
            '${(conf * 100).toInt()}% conf',
            style: TextStyle(
              color: isLow ? const Color(0xFFF59E0B) : const Color(0xFF34D399),
              fontSize: 10,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCornerMarker(Alignment alignment) {
    return Align(
      alignment: alignment,
      child: Container(
        margin: const EdgeInsets.all(24),
        width: 24,
        height: 24,
        decoration: BoxDecoration(
          border: Border(
            top: alignment == Alignment.topLeft || alignment == Alignment.topRight ? const BorderSide(color: Color(0xFF38BDF8), width: 3) : BorderSide.none,
            bottom: alignment == Alignment.bottomLeft || alignment == Alignment.bottomRight ? const BorderSide(color: Color(0xFF38BDF8), width: 3) : BorderSide.none,
            left: alignment == Alignment.topLeft || alignment == Alignment.bottomLeft ? const BorderSide(color: Color(0xFF38BDF8), width: 3) : BorderSide.none,
            right: alignment == Alignment.topRight || alignment == Alignment.bottomRight ? const BorderSide(color: Color(0xFF38BDF8), width: 3) : BorderSide.none,
          ),
        ),
      ),
    );
  }
}
