"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { PrescriptionViewer } from "@/components/PrescriptionViewer";
import { MedicationTable } from "@/components/MedicationTable";
import { InteractionAlerts } from "@/components/InteractionAlerts";
import { PatientSummary } from "@/components/PatientSummary";
import { ActionBar } from "@/components/ActionBar";
import { SAMPLE_AUDIT_RESPONSE } from "@/data/sampleAudit";
import { AuditResponse } from "@/types/audit";
import {
  FileText,
  ShieldAlert,
  Sparkles,
  RefreshCw,
  SlidersHorizontal,
  CheckCircle2,
  Info,
} from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  const [auditData, setAuditData] = useState<AuditResponse>(SAMPLE_AUDIT_RESPONSE);
  const [selectedMedId, setSelectedMedId] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [activeTab, setActiveTab] = useState<string>("all");

  // Handle uploading custom prescription image
  const handleCustomImageUpload = (file: File) => {
    setIsScanning(true);
    // Simulate on-device OCR inference pipeline (1.2 seconds)
    setTimeout(() => {
      setIsScanning(false);
    }, 1200);
  };

  // Handle clinician verifying an ambiguous handwriting line
  const handleVerifyMedication = (id: string, correctedDosage?: string) => {
    setAuditData((prev) => ({
      ...prev,
      medications: prev.medications.map((m) => {
        if (m.id === id) {
          return {
            ...m,
            dosage: correctedDosage || "2.5 mg (Clarified with MD)",
            handwriting_uncertain: false,
            confidence: 0.99,
            uncertainty_reason: undefined,
          };
        }
        return m;
      }),
    }));
  };

  // Handle Clinician Confirm & Lock sign-off
  const handleLockPrescription = (signoff: {
    signed_by: string;
    license_id: string;
    notes: string;
  }) => {
    setAuditData((prev) => ({
      ...prev,
      status: "confirmed_and_locked",
      pharmacist_signoff: {
        ...signoff,
        timestamp: new Date().toISOString(),
      },
    }));
  };

  // Handle resetting back to initial demonstration state
  const handleResetDemo = () => {
    setAuditData(SAMPLE_AUDIT_RESPONSE);
    setSelectedMedId(null);
  };

  return (
    <div className="flex min-h-screen flex-col bg-background selection:bg-cyan-500/20">
      {/* Top Navigation & Privacy Header */}
      <Header
        prescriptionId={auditData.prescription_id}
        patientMaskedId={auditData.patient_masked_id}
        edgeMode={auditData.edge_mode}
        latencyMs={auditData.inference_latency_ms}
      />

      {/* Main Workspace Layout */}
      <main className="flex-1 container mx-auto px-4 py-6 sm:px-6 space-y-6">
        {/* Prescription Metadata / Sub-header */}
        <div className="flex flex-wrap items-center justify-between gap-3 bg-card/40 border border-border/50 rounded-xl px-4 py-2.5 text-xs text-muted-foreground backdrop-blur-md">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-foreground">
              Inspection Dossier:
            </span>
            <span className="font-mono bg-muted/60 px-2 py-0.5 rounded text-primary">
              {auditData.prescription_id}
            </span>
            <span className="hidden sm:inline text-border">•</span>
            <span className="hidden sm:inline">
              Model: <strong className="text-foreground">{auditData.model_runtime}</strong>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="ghost"
              onClick={handleResetDemo}
              className="h-7 text-xs text-muted-foreground hover:text-foreground gap-1"
            >
              <RefreshCw className="h-3 w-3" />
              <span>Reset Demo State</span>
            </Button>
          </div>
        </div>

        {/* 1. Split-View Inspection Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Side: Prescription Image Viewer (5 cols on lg) */}
          <div className="lg:col-span-5 sticky lg:top-20 space-y-3">
            <PrescriptionViewer
              medications={auditData.medications}
              selectedMedId={selectedMedId}
              onSelectMed={setSelectedMedId}
              onCustomImageUpload={handleCustomImageUpload}
              isScanning={isScanning}
            />

            {/* Quick Helper card */}
            <div className="rounded-xl border border-border/50 bg-card/30 p-3 text-xs text-muted-foreground flex items-start gap-2.5">
              <Info className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
              <p className="leading-relaxed">
                Click any line in the digital slip or table to highlight and cross-examine extracted tokens with OCR coordinates.
              </p>
            </div>
          </div>

          {/* Right Side: Interactive Audit Dashboard (7 cols on lg) */}
          <div className="lg:col-span-7 space-y-6">
            {/* View Selector Tabs */}
            <Tabs defaultValue="all" value={activeTab} onValueChange={setActiveTab}>
              <div className="flex items-center justify-between gap-2 border-b border-border/60 pb-2">
                <TabsList className="bg-muted/40">
                  <TabsTrigger value="all" className="gap-1.5 text-xs">
                    <SlidersHorizontal className="h-3.5 w-3.5" />
                    <span>Complete Dossier</span>
                  </TabsTrigger>
                  <TabsTrigger value="medications" className="gap-1.5 text-xs">
                    <FileText className="h-3.5 w-3.5" />
                    <span>Medications ({auditData.medications.length})</span>
                  </TabsTrigger>
                  <TabsTrigger value="interactions" className="gap-1.5 text-xs">
                    <ShieldAlert className="h-3.5 w-3.5" />
                    <span>Interactions ({auditData.interactions.length})</span>
                  </TabsTrigger>
                  <TabsTrigger value="patient" className="gap-1.5 text-xs">
                    <Sparkles className="h-3.5 w-3.5" />
                    <span>Gemma Patient Guide</span>
                  </TabsTrigger>
                </TabsList>
              </div>

              {/* Complete Dossier View (All in coherent clinical order) */}
              <TabsContent value="all" className="space-y-6 mt-4">
                {/* 4. Deterministic Interaction Alert Cards (Top priority for safety) */}
                <InteractionAlerts
                  interactions={auditData.interactions}
                />

                {/* 3. Clinical Uncertainty & Flagging UI */}
                <MedicationTable
                  medications={auditData.medications}
                  selectedMedId={selectedMedId}
                  onSelectMed={setSelectedMedId}
                  onVerifyMedication={handleVerifyMedication}
                />

                {/* 5. Gemma Plain-Language Translation Card */}
                <PatientSummary summary={auditData.patient_summary} />
              </TabsContent>

              {/* Individual Tab Views */}
              <TabsContent value="medications" className="space-y-4 mt-4">
                <MedicationTable
                  medications={auditData.medications}
                  selectedMedId={selectedMedId}
                  onSelectMed={setSelectedMedId}
                  onVerifyMedication={handleVerifyMedication}
                />
              </TabsContent>

              <TabsContent value="interactions" className="space-y-4 mt-4">
                <InteractionAlerts
                  interactions={auditData.interactions}
                />
              </TabsContent>

              <TabsContent value="patient" className="space-y-4 mt-4">
                <PatientSummary summary={auditData.patient_summary} />
              </TabsContent>
            </Tabs>
          </div>
        </div>

        {/* 6. Action Bar at the bottom */}
        <div className="pt-4">
          <ActionBar
            auditData={auditData}
            onLockPrescription={handleLockPrescription}
            isLocked={auditData.status === "confirmed_and_locked"}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/20 py-4 mt-12 text-center text-xs text-muted-foreground">
        <div className="container mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-foreground">Araksha-Med Edge Core</span>
            <span>•</span>
            <span>Zero-Cloud PII Vault</span>
          </div>
          <div>
            Built with Next.js 14, TypeScript, Tailwind CSS & Gemma AI
          </div>
        </div>
      </footer>
    </div>
  );
}
