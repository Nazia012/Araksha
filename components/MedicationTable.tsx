"use client";

import React from "react";
import {
  AlertTriangle,
  CheckCircle2,
  HelpCircle,
  Pill,
  ShieldAlert,
  Sparkles,
  Edit2,
  Check,
} from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ExtractedMedication } from "@/types/audit";
import { cn } from "@/lib/utils";

interface MedicationTableProps {
  medications: ExtractedMedication[];
  selectedMedId: string | null;
  onSelectMed: (id: string | null) => void;
  onVerifyMedication?: (id: string, correctedDosage?: string) => void;
}

export function MedicationTable({
  medications,
  selectedMedId,
  onSelectMed,
  onVerifyMedication,
}: MedicationTableProps) {
  const [editingId, setEditingId] = React.useState<string | null>(null);
  const [editedDosage, setEditedDosage] = React.useState<string>("");

  const handleStartEdit = (med: ExtractedMedication) => {
    setEditingId(med.id);
    setEditedDosage(med.dosage);
  };

  const handleSaveEdit = (id: string) => {
    if (onVerifyMedication) {
      onVerifyMedication(id, editedDosage);
    }
    setEditingId(null);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Pill className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-semibold tracking-tight text-foreground">
            Extracted Medications ({medications.length})
          </h3>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-emerald-500 inline-block" />
            High Confidence
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2 w-2 rounded-full bg-amber-500 inline-block" />
            Needs Review
          </span>
        </div>
      </div>

      {/* Main Table Container */}
      <div className="rounded-xl border border-border/70 bg-card/40 backdrop-blur-md overflow-hidden shadow-sm">
        <Table>
          <TableHeader>
            <TableRow className="border-border/60 hover:bg-transparent">
              <TableHead className="w-[180px]">Drug Name</TableHead>
              <TableHead className="w-[140px]">Active Ingredient</TableHead>
              <TableHead className="w-[130px]">Dosage</TableHead>
              <TableHead className="min-w-[180px]">Frequency & Sig</TableHead>
              <TableHead className="w-[120px] text-right">Confidence</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {medications.map((med) => {
              const isSelected = selectedMedId === med.id;
              const isUncertain = med.handwriting_uncertain;
              const confidencePercent = Math.round(med.confidence * 100);

              return (
                <React.Fragment key={med.id}>
                  <TableRow
                    onClick={() => onSelectMed(isSelected ? null : med.id)}
                    className={cn(
                      "cursor-pointer transition-colors duration-150",
                      isSelected
                        ? "bg-primary/10 border-l-4 border-l-primary"
                        : "hover:bg-muted/50",
                      isUncertain && "bg-amber-950/10 border-l-4 border-l-amber-500/80"
                    )}
                  >
                    {/* Drug Name Column */}
                    <TableCell className="font-medium">
                      <div className="flex flex-col gap-0.5">
                        <div className="flex items-center gap-1.5">
                          <span className="text-foreground font-semibold text-sm">
                            {med.name}
                          </span>
                        </div>
                        {med.route && (
                          <span className="text-[10px] text-muted-foreground">
                            Route: {med.route}
                          </span>
                        )}
                      </div>
                    </TableCell>

                    {/* Active Ingredient */}
                    <TableCell>
                      <span className="text-xs text-muted-foreground font-mono bg-muted/40 px-2 py-0.5 rounded-md border border-border/40">
                        {med.active_ingredient}
                      </span>
                    </TableCell>

                    {/* Dosage */}
                    <TableCell>
                      {editingId === med.id ? (
                        <div
                          className="flex items-center gap-1.5"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <input
                            type="text"
                            value={editedDosage}
                            onChange={(e) => setEditedDosage(e.target.value)}
                            className="h-7 w-24 rounded border border-amber-500 bg-background px-2 text-xs font-mono text-foreground focus:outline-none focus:ring-1 focus:ring-amber-500"
                            autoFocus
                          />
                          <Button
                            size="icon"
                            variant="amber"
                            className="h-6 w-6"
                            onClick={() => handleSaveEdit(med.id)}
                            title="Confirm Dosage"
                          >
                            <Check className="h-3 w-3" />
                          </Button>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1.5">
                          <span
                            className={cn(
                              "font-mono text-xs font-semibold px-2 py-0.5 rounded",
                              isUncertain
                                ? "text-amber-300 bg-amber-950/40 border border-amber-500/50"
                                : "text-foreground bg-muted/40 border border-border/40"
                            )}
                          >
                            {med.dosage}
                          </span>
                          {isUncertain && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleStartEdit(med);
                              }}
                              className="text-amber-400 hover:text-amber-300 transition-colors p-1"
                              title="Edit/Verify Dosage"
                            >
                              <Edit2 className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                      )}
                    </TableCell>

                    {/* Frequency */}
                    <TableCell className="text-xs text-muted-foreground">
                      {med.frequency}
                    </TableCell>

                    {/* Confidence Pill */}
                    <TableCell className="text-right">
                      {confidencePercent >= 85 ? (
                        <Badge
                          variant="success"
                          className="font-mono text-[11px] gap-1"
                        >
                          <CheckCircle2 className="h-3 w-3" />
                          {confidencePercent}%
                        </Badge>
                      ) : (
                        <Badge
                          variant="warning"
                          className="font-mono text-[11px] gap-1"
                        >
                          <AlertTriangle className="h-3 w-3" />
                          {confidencePercent}%
                        </Badge>
                      )}
                    </TableCell>
                  </TableRow>

                  {/* Handwriting Uncertainty Warning Banner */}
                  {isUncertain && (
                    <TableRow className="bg-amber-950/20 hover:bg-amber-950/25 border-b border-amber-500/30">
                      <TableCell colSpan={5} className="py-2.5 px-4">
                        <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-amber-500/50 bg-amber-500/10 p-2.5 shadow-sm">
                          <div className="flex items-center gap-2">
                            <div className="rounded-full bg-amber-500/20 p-1 text-amber-400">
                              <AlertTriangle className="h-4 w-4" />
                            </div>
                            <div>
                              <Badge
                                variant="warning"
                                className="border-amber-500/60 font-semibold tracking-wide uppercase text-[10px]"
                              >
                                Doctor handwriting unclear — verify before dispensing
                              </Badge>
                              <p className="mt-1 text-xs text-amber-200/90 font-sans">
                                {med.uncertainty_reason ||
                                  "OCR detected low stroke confidence on dosage numerals. Cross-reference clinical indication with physician."}
                              </p>
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            <Button
                              size="sm"
                              variant="outline"
                              className="h-7 text-xs border-amber-500/50 text-amber-300 hover:bg-amber-500/20"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleStartEdit(med);
                              }}
                            >
                              Clarify Dosage
                            </Button>
                            <Button
                              size="sm"
                              variant="amber"
                              className="h-7 text-xs"
                              onClick={(e) => {
                                e.stopPropagation();
                                onVerifyMedication?.(med.id);
                              }}
                            >
                              Mark Verified
                            </Button>
                          </div>
                        </div>
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              );
            })}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
