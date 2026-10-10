"use client";

import React, { useState } from "react";
import {
  FileDown,
  Lock,
  CheckCircle,
  AlertTriangle,
  Loader2,
  FileCheck2,
  ShieldCheck,
  UserCheck,
  ExternalLink,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { AuditResponse } from "@/types/audit";

interface ActionBarProps {
  auditData: AuditResponse;
  onLockPrescription: (signoff: {
    signed_by: string;
    license_id: string;
    notes: string;
  }) => void;
  isLocked: boolean;
}

export function ActionBar({
  auditData,
  onLockPrescription,
  isLocked,
}: ActionBarProps) {
  const [isPdfLoading, setIsPdfLoading] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [clinicianName, setClinicianName] = useState("Dr. Eleanor Vance, PharmD");
  const [licenseId, setLicenseId] = useState("RPH-84910-US");
  const [signoffNotes, setSignoffNotes] = useState(
    "Verified Warfarin dose as 2.5mg with Dr. Vance. Nitroglycerin held during Sildenafil therapy."
  );
  const [confirmedCheck, setConfirmedCheck] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  // Pharmacist Dossier PDF Trigger (ReportLab endpoint)
  const handleDownloadDossier = async () => {
    setIsPdfLoading(true);
    setDownloadSuccess(false);

    try {
      // In production, this calls the backend ReportLab endpoint:
      // const res = await fetch(`/api/reports/dossier?id=${auditData.prescription_id}`);
      // For on-device demonstration, simulate ReportLab PDF generation delay:
      await new Promise((resolve) => setTimeout(resolve, 1400));

      // Create a downloadable dossier blob summary or report
      const reportHtml = `
===========================================================
ARAKSHA-MED: PHARMACIST CLINICAL DOSSIER
Deterministic Drug Interaction & On-Device Audit Report
===========================================================
Prescription ID: ${auditData.prescription_id}
Patient ID (Masked): ${auditData.patient_masked_id}
Generated: ${new Date().toISOString()}
Edge Engine: ${auditData.model_runtime}
Inference Latency: ${auditData.inference_latency_ms} ms

MEDICATIONS EXTRACTED:
${auditData.medications
  .map(
    (m) =>
      `• ${m.name} (${m.active_ingredient}) - ${m.dosage} | ${m.frequency} [Confidence: ${Math.round(
        m.confidence * 100
      )}%] ${m.handwriting_uncertain ? " [FLAGGED: UNCERTAIN HANDWRITING]" : ""}`
  )
  .join("\n")}

CONTRAINDICATIONS & INTERACTIONS DETECTED:
${auditData.interactions
  .map(
    (i) =>
      `[${i.severity.toUpperCase()}] ${i.title}\nMechanism: ${i.mechanism}\nAction: ${
        i.clinical_action
      }\nSource: ${i.citation_source}\n`
  )
  .join("\n")}

STATUS: ${isLocked ? "CONFIRMED & LOCKED BY CLINICIAN" : "PENDING CLINICAL SIGN-OFF"}
${
  auditData.pharmacist_signoff
    ? `Signed By: ${auditData.pharmacist_signoff.signed_by} (${auditData.pharmacist_signoff.license_id})\nTimestamp: ${auditData.pharmacist_signoff.timestamp}`
    : ""
}

DISCLAIMER: ${auditData.patient_summary.clinical_disclaimer}
===========================================================
      `;

      const blob = new Blob([reportHtml], { type: "text/plain;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `Araksha_Pharmacist_Dossier_${auditData.prescription_id}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      setDownloadSuccess(true);
      setTimeout(() => setDownloadSuccess(false), 4000);
    } catch (err) {
      console.error("Failed to generate PDF dossier:", err);
    } finally {
      setIsPdfLoading(false);
    }
  };

  const handleConfirmLock = () => {
    if (!confirmedCheck) return;
    onLockPrescription({
      signed_by: clinicianName,
      license_id: licenseId,
      notes: signoffNotes,
    });
    setIsDialogOpen(false);
  };

  const majorCount = auditData.interactions.filter(
    (i) => i.severity === "major"
  ).length;
  const uncertainCount = auditData.medications.filter(
    (m) => m.handwriting_uncertain
  ).length;

  return (
    <>
      <div className="rounded-2xl border border-border/80 bg-card/80 backdrop-blur-xl p-4 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Left Status info */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          {isLocked ? (
            <div className="flex items-center gap-2 text-emerald-400">
              <div className="h-9 w-9 rounded-full bg-emerald-500/20 flex items-center justify-center border border-emerald-500/40">
                <CheckCircle className="h-5 w-5 text-emerald-400" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-300 block">
                  Prescription Confirmed & Locked
                </span>
                <span className="text-[11px] text-muted-foreground font-mono">
                  Signed: {auditData.pharmacist_signoff?.signed_by || clinicianName}
                </span>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <div className="h-9 w-9 rounded-full bg-amber-500/10 flex items-center justify-center border border-amber-500/30">
                <AlertTriangle className="h-5 w-5 text-amber-400" />
              </div>
              <div>
                <span className="text-xs font-bold text-foreground block">
                  Clinical Review Pending
                </span>
                <span className="text-[11px] text-muted-foreground">
                  {majorCount} major contraindication • {uncertainCount} unclear line
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Right Actions */}
        <div className="flex flex-wrap items-center gap-2.5 w-full sm:w-auto justify-end">
          {/* Download Pharmacist Dossier (PDF / ReportLab) */}
          <Button
            variant="outline"
            size="default"
            onClick={handleDownloadDossier}
            disabled={isPdfLoading}
            className="gap-2 border-border/80 hover:bg-muted/80 text-xs sm:text-sm"
          >
            {isPdfLoading ? (
              <Loader2 className="h-4 w-4 animate-spin text-primary" />
            ) : downloadSuccess ? (
              <CheckCircle className="h-4 w-4 text-emerald-400" />
            ) : (
              <FileDown className="h-4 w-4 text-cyan-400" />
            )}
            <span>
              {isPdfLoading
                ? "Compiling ReportLab Dossier..."
                : downloadSuccess
                ? "Dossier Downloaded"
                : "Download Pharmacist Dossier (PDF)"}
            </span>
          </Button>

          {/* Confirm & Lock Prescription Button */}
          {isLocked ? (
            <Button
              variant="outline"
              size="default"
              disabled
              className="gap-2 border-emerald-500/50 bg-emerald-950/30 text-emerald-300 text-xs sm:text-sm cursor-default"
            >
              <Lock className="h-4 w-4 text-emerald-400" />
              <span>Prescription Locked</span>
            </Button>
          ) : (
            <Button
              variant="default"
              size="default"
              onClick={() => setIsDialogOpen(true)}
              className="gap-2 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-500 hover:to-teal-500 text-white shadow-lg shadow-cyan-950/30 text-xs sm:text-sm"
            >
              <FileCheck2 className="h-4 w-4" />
              <span>Confirm & Lock Prescription</span>
            </Button>
          )}
        </div>
      </div>

      {/* Clinician Sign-off Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <div className="flex items-center gap-2 text-primary">
              <ShieldCheck className="h-5 w-5 text-cyan-400" />
              <DialogTitle>Clinician Sign-off & Audit Lock</DialogTitle>
            </div>
            <DialogDescription>
              Confirming will seal this prescription review record with an immutable on-device audit hash.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-3 text-xs">
            {majorCount > 0 && (
              <div className="rounded-lg border border-red-500/50 bg-red-950/20 p-3 text-red-200">
                <p className="font-bold flex items-center gap-1.5 mb-1">
                  <AlertTriangle className="h-4 w-4 text-red-400" />
                  Active Major Contraindication Detected!
                </p>
                <p className="text-[11px] opacity-90 leading-relaxed">
                  Sildenafil and Nitroglycerin co-administration is strictly contraindicated. Please confirm that you have counseled the patient or adjusted dispensing accordingly.
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="text-muted-foreground font-medium">Pharmacist / Clinician Name</label>
                <input
                  type="text"
                  value={clinicianName}
                  onChange={(e) => setClinicianName(e.target.value)}
                  className="w-full h-8 rounded-md border border-input bg-background/50 px-2.5 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>

              <div className="space-y-1">
                <label className="text-muted-foreground font-medium">License / NPI Number</label>
                <input
                  type="text"
                  value={licenseId}
                  onChange={(e) => setLicenseId(e.target.value)}
                  className="w-full h-8 rounded-md border border-input bg-background/50 px-2.5 text-xs text-foreground font-mono focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-muted-foreground font-medium">Verification & Override Notes</label>
              <textarea
                value={signoffNotes}
                onChange={(e) => setSignoffNotes(e.target.value)}
                rows={3}
                className="w-full rounded-md border border-input bg-background/50 p-2.5 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary resize-none"
              />
            </div>

            <div className="rounded-lg border border-border/60 bg-muted/30 p-3">
              <label className="flex items-start gap-2.5 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={confirmedCheck}
                  onChange={(e) => setConfirmedCheck(e.target.checked)}
                  className="mt-0.5 rounded border-border text-primary focus:ring-primary"
                />
                <span className="text-[11px] text-muted-foreground leading-snug">
                  I certify as a licensed healthcare professional that I have evaluated the flagged handwriting uncertainties, drug interactions, and counseling instructions before dispensing.
                </span>
              </label>
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button
              variant="default"
              size="sm"
              disabled={!confirmedCheck}
              onClick={handleConfirmLock}
              className="gap-1.5 bg-cyan-600 hover:bg-cyan-500 text-white"
            >
              <Lock className="h-3.5 w-3.5" />
              Confirm & Lock Audit
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
