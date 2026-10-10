import 'package:flutter/material.dart';
import '../models/prescription_models.dart';

class InteractionReportScreen extends StatefulWidget {
  final PrescriptionAnalysisReport report;

  const InteractionReportScreen({Key? key, required this.report}) : super(key: key);

  @override
  State<InteractionReportScreen> createState() => _InteractionReportScreenState();
}

class _InteractionReportScreenState extends State<InteractionReportScreen> {
  late Set<int> _checkedChecklistItems;
  bool _isChecklistExpanded = true;

  @override
  void initState() {
    super.initState();
    _checkedChecklistItems = {};
  }

  Color _getRiskColor() {
    switch (widget.report.riskColor.toLowerCase()) {
      case 'red':
        return const Color(0xFFEF4444); // Severe
      case 'amber':
        return const Color(0xFFF59E0B); // Moderate / Caution
      case 'green':
      default:
        return const Color(0xFF10B981); // Clear
    }
  }

  IconData _getRiskIcon() {
    switch (widget.report.riskColor.toLowerCase()) {
      case 'red':
        return Icons.dangerous_outlined;
      case 'amber':
        return Icons.warning_amber_rounded;
      case 'green':
      default:
        return Icons.check_circle_outline;
    }
  }

  @override
  Widget build(BuildContext context) {
    final riskColor = _getRiskColor();
    final riskIcon = _getRiskIcon();

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: const Text('Interaction Report', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 1. Color-Coded Risk Alert Banner
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: riskColor.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: riskColor, width: 1.5),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: riskColor.withOpacity(0.2),
                        shape: BoxShape.circle,
                      ),
                      child: Icon(riskIcon, color: riskColor, size: 30),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'RISK LEVEL: ${widget.report.riskLevel.toUpperCase()}',
                            style: TextStyle(
                              color: riskColor,
                              fontWeight: FontWeight.w900,
                              fontSize: 15,
                              letterSpacing: 0.5,
                            ),
                          ),
                          const SizedBox(height: 3),
                          Text(
                            widget.report.verifiedDdis.isEmpty
                                ? 'No critical drug-drug interactions detected.'
                                : '${widget.report.verifiedDdis.length} interaction pair(s) deterministically identified.',
                            style: const TextStyle(color: Colors.white70, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // 2. Google Gemma 4 Plain-Language Patient Summary
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: const Color(0xFF334155)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.auto_awesome, color: Color(0xFF38BDF8), size: 18),
                        SizedBox(width: 8),
                        Text(
                          'Plain-Language Patient Summary',
                          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      widget.report.patientSummary,
                      style: const TextStyle(color: Color(0xFFE2E8F0), fontSize: 13, height: 1.5),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // 3. Detected Medications List
              const Text(
                'Identified RxNorm Medications',
                style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: widget.report.detectedMedications.map((med) {
                  return Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: const Color(0xFF334155)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          med.genericName.toUpperCase(),
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                        ),
                        Text(
                          '${med.drugClass} (RxCUI: ${med.rxcui})',
                          style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),

              const SizedBox(height: 20),

              // 4. Verified Interaction Detail Cards
              if (widget.report.interactionFlags.isNotEmpty) ...[
                const Text(
                  'Verified Drug Interactions',
                  style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                ...widget.report.interactionFlags.map((flag) {
                  final isSevere = flag.severity.toLowerCase() == 'severe';
                  final badgeColor = isSevere ? const Color(0xFFEF4444) : const Color(0xFFF59E0B);

                  return Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: badgeColor.withOpacity(0.5)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Text(
                                flag.pair,
                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: badgeColor.withOpacity(0.18),
                                borderRadius: BorderRadius.circular(6),
                                border: Border.all(color: badgeColor),
                              ),
                              child: Text(
                                flag.severity.toUpperCase(),
                                style: TextStyle(color: badgeColor, fontSize: 11, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Text(
                          flag.explanation,
                          style: const TextStyle(color: Color(0xFFCBD5E1), fontSize: 12.5, height: 1.4),
                        ),
                        const SizedBox(height: 12),
                        // Action for Pharmacist
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: const Color(0xFF0F172A),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: const Color(0xFF38BDF8).withOpacity(0.3)),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Icon(Icons.help_outline, color: Color(0xFF38BDF8), size: 16),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  flag.actionForPharmacist,
                                  style: const TextStyle(color: Color(0xFF38BDF8), fontSize: 11.5, fontWeight: FontWeight.w500),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ],

              // 5. Expandable "Ask Your Pharmacist" Checklist
              Container(
                margin: const EdgeInsets.only(top: 8, bottom: 20),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: const Color(0xFF334155)),
                ),
                child: Theme(
                  data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
                  child: ExpansionTile(
                    initiallyExpanded: true,
                    leading: const Icon(Icons.checklist, color: Color(0xFF10B981)),
                    title: const Text(
                      'Ask Your Pharmacist Checklist',
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                    ),
                    subtitle: Text(
                      '${_checkedChecklistItems.length} of ${widget.report.pharmacistChecklist.length} reviewed',
                      style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11),
                    ),
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        child: Column(
                          children: List.generate(widget.report.pharmacistChecklist.length, (index) {
                            final item = widget.report.pharmacistChecklist[index];
                            final isChecked = _checkedChecklistItems.contains(index);

                            return CheckboxListTile(
                              dense: true,
                              activeColor: const Color(0xFF10B981),
                              contentPadding: EdgeInsets.zero,
                              title: Text(
                                item,
                                style: TextStyle(
                                  color: isChecked ? const Color(0xFF64748B) : const Color(0xFFE2E8F0),
                                  fontSize: 12.5,
                                  decoration: isChecked ? TextDecoration.lineThrough : null,
                                ),
                              ),
                              value: isChecked,
                              onChanged: (val) {
                                setState(() {
                                  if (val == true) {
                                    _checkedChecklistItems.add(index);
                                  } else {
                                    _checkedChecklistItems.remove(index);
                                  }
                                });
                              },
                            );
                          }),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              // 6. Flagged Uncertainties if any
              if (widget.report.uncertainties.isNotEmpty) ...[
                Container(
                  padding: const EdgeInsets.all(14),
                  margin: const EdgeInsets.only(bottom: 20),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF59E0B).withOpacity(0.08),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFF59E0B).withOpacity(0.4)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: const [
                          Icon(Icons.flag_outlined, color: Color(0xFFF59E0B), size: 16),
                          SizedBox(width: 6),
                          Text(
                            'Flagged Tokens for Manual Pharmacy Check',
                            style: TextStyle(color: Color(0xFFF59E0B), fontWeight: FontWeight.bold, fontSize: 13),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      ...widget.report.uncertainties.map((u) => Padding(
                            padding: const EdgeInsets.only(bottom: 4),
                            child: Text('• $u', style: const TextStyle(color: Color(0xFFCBD5E1), fontSize: 11.5)),
                          )),
                    ],
                  ),
                ),
              ],

              // 7. Clinical Disclaimer Banner
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFF334155)),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.info_outline, color: Color(0xFF64748B), size: 18),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        widget.report.disclaimer,
                        style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontStyle: FontStyle.italic),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 30),
            ],
          ),
        ),
      ),
    );
  }
}
