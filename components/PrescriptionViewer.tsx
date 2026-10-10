"use client";

import React, { useState, useRef } from "react";
import {
  ZoomIn,
  ZoomOut,
  Maximize2,
  RotateCcw,
  Upload,
  AlertTriangle,
  Eye,
  EyeOff,
  Sparkles,
  FileText,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ExtractedMedication } from "@/types/audit";
import { cn } from "@/lib/utils";

interface PrescriptionViewerProps {
  medications: ExtractedMedication[];
  selectedMedId: string | null;
  onSelectMed: (id: string | null) => void;
  onCustomImageUpload?: (file: File) => void;
  isScanning?: boolean;
}

export function PrescriptionViewer({
  medications,
  selectedMedId,
  onSelectMed,
  onCustomImageUpload,
  isScanning = false,
}: PrescriptionViewerProps) {
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [showOverlays, setShowOverlays] = useState(true);
  const [highlightUncertainOnly, setHighlightUncertainOnly] = useState(false);
  const [customImage, setCustomImage] = useState<string | null>(null);
  const [isDropActive, setIsDropActive] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 0.25, 3.0));
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 0.25, 0.6));
  const handleReset = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return; // only left click
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPan({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => setIsDragging(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setCustomImage(url);
      onCustomImageUpload?.(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDropActive(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file);
      setCustomImage(url);
      onCustomImageUpload?.(file);
    }
  };

  const uncertainMedsCount = medications.filter(
    (m) => m.handwriting_uncertain
  ).length;

  return (
    <div className="flex h-full flex-col rounded-2xl border border-border/70 bg-card/60 backdrop-blur-xl shadow-xl overflow-hidden">
      {/* Top Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border/60 bg-muted/40 px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-foreground">
            <FileText className="h-4 w-4 text-primary" />
            <span>Prescription Slip</span>
          </div>

          <Badge variant="outline" className="text-[11px] font-mono bg-background/50">
            {Math.round(zoom * 100)}%
          </Badge>

          {uncertainMedsCount > 0 && (
            <Badge
              variant="warning"
              className="text-[10px] gap-1 cursor-pointer hover:bg-amber-500/25 transition-colors"
              onClick={() => setHighlightUncertainOnly((prev) => !prev)}
            >
              <AlertTriangle className="h-3 w-3" />
              <span>{uncertainMedsCount} Unclear Line</span>
            </Badge>
          )}
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1.5">
          <Button
            size="sm"
            variant="outline"
            className={cn(
              "h-8 px-2.5 text-xs gap-1.5",
              showOverlays ? "border-primary/50 text-primary bg-primary/10" : ""
            )}
            onClick={() => setShowOverlays((prev) => !prev)}
            title="Toggle OCR Line Highlights"
          >
            {showOverlays ? <Eye className="h-3.5 w-3.5" /> : <EyeOff className="h-3.5 w-3.5" />}
            <span className="hidden sm:inline">Highlights</span>
          </Button>

          <div className="h-4 w-px bg-border/60 mx-1" />

          <Button
            size="icon"
            variant="ghost"
            className="h-8 w-8"
            onClick={handleZoomOut}
            title="Zoom Out"
            disabled={zoom <= 0.6}
          >
            <ZoomOut className="h-4 w-4" />
          </Button>

          <Button
            size="icon"
            variant="ghost"
            className="h-8 w-8"
            onClick={handleZoomIn}
            title="Zoom In"
            disabled={zoom >= 3.0}
          >
            <ZoomIn className="h-4 w-4" />
          </Button>

          <Button
            size="icon"
            variant="ghost"
            className="h-8 w-8"
            onClick={handleReset}
            title="Reset Pan & Zoom"
          >
            <RotateCcw className="h-3.5 w-3.5" />
          </Button>

          <div className="h-4 w-px bg-border/60 mx-1" />

          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            accept="image/*"
            onChange={handleFileChange}
          />
          <Button
            size="sm"
            variant="outline"
            className="h-8 px-2.5 text-xs gap-1.5 bg-background/50 hover:bg-primary hover:text-primary-foreground transition-all"
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Upload New</span>
          </Button>
        </div>
      </div>

      {/* Main Canvas Viewport */}
      <div
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDropActive(true);
        }}
        onDragLeave={() => setIsDropActive(false)}
        onDrop={handleDrop}
        className={cn(
          "relative flex-1 min-h-[460px] max-h-[700px] overflow-hidden select-none bg-neutral-950/90 flex items-center justify-center p-4 cursor-grab active:cursor-grabbing",
          isDropActive && "ring-2 ring-primary ring-inset bg-primary/5"
        )}
      >
        {/* Subtle grid pattern background */}
        <div
          className="absolute inset-0 opacity-15 pointer-events-none"
          style={{
            backgroundImage:
              "radial-gradient(circle, rgba(255,255,255,0.2) 1px, transparent 1px)",
            backgroundSize: "20px 20px",
          }}
        />

        {/* On-device OCR Scanning Laser Beam */}
        {isScanning && (
          <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_15px_#22d3ee] animate-scan z-30 pointer-events-none" />
        )}

        {/* Drag & Drop Overlay Indicator */}
        {isDropActive && (
          <div className="absolute inset-0 z-40 bg-primary/20 backdrop-blur-sm flex flex-col items-center justify-center text-primary-foreground pointer-events-none">
            <Upload className="h-12 w-12 animate-bounce text-primary mb-2" />
            <p className="text-sm font-semibold text-white">Drop prescription image here to inspect</p>
          </div>
        )}

        {/* Zoomed / Panned Canvas */}
        <div
          className="transition-transform duration-75 ease-out relative shadow-2xl rounded-lg"
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            transformOrigin: "center center",
          }}
        >
          {customImage ? (
            /* Uploaded Image view with interactive overlay boxes */
            <div className="relative max-w-full max-h-[620px] rounded-lg overflow-hidden border border-neutral-700 bg-white">
              <img
                src={customImage}
                alt="Uploaded Prescription"
                className="max-w-[500px] w-full h-auto object-contain block pointer-events-none"
              />
              {/* Overlays */}
              {showOverlays &&
                medications.map((med) => {
                  if (highlightUncertainOnly && !med.handwriting_uncertain) {
                    return null;
                  }
                  if (!med.bounding_box) return null;
                  const isSelected = selectedMedId === med.id;

                  return (
                    <div
                      key={med.id}
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectMed(med.id);
                      }}
                      className={cn(
                        "absolute rounded border-2 cursor-pointer transition-all duration-200 pointer-events-auto",
                        med.handwriting_uncertain
                          ? "border-amber-400 bg-amber-400/20 shadow-[0_0_12px_rgba(251,191,36,0.5)] animate-pulse-slow"
                          : isSelected
                          ? "border-cyan-400 bg-cyan-400/20 ring-2 ring-cyan-400"
                          : "border-emerald-400/70 bg-emerald-400/10 hover:border-emerald-400"
                      )}
                      style={{
                        left: `${med.bounding_box.x}%`,
                        top: `${med.bounding_box.y}%`,
                        width: `${med.bounding_box.width}%`,
                        height: `${med.bounding_box.height}%`,
                      }}
                    />
                  );
                })}
            </div>
          ) : (
            /* Synthetic High-Fidelity Medical Prescription Slip Canvas */
            <div className="w-[440px] sm:w-[480px] bg-[#fbfbfa] text-neutral-900 rounded-md border border-neutral-300 shadow-2xl p-6 relative font-sans overflow-hidden">
              {/* Paper Texture & Watermark */}
              <div className="absolute inset-0 bg-gradient-to-b from-amber-50/20 to-neutral-100/40 pointer-events-none" />
              <div className="absolute right-4 bottom-16 text-6xl font-serif text-neutral-200/50 rotate-[-25deg] select-none pointer-events-none font-bold">
                ARAKSHA
              </div>

              {/* Clinic Header */}
              <div className="border-b-2 border-neutral-900 pb-3 mb-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-base font-serif font-black tracking-wide text-neutral-900 uppercase">
                      Memorial Cardiology Institute
                    </h2>
                    <p className="text-[11px] text-neutral-600 font-sans">
                      Suite 400 • Medical Arts Pavilion • License #CAR-84910
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-1.5 py-0.5 bg-neutral-900 text-white text-[9px] font-mono tracking-widest font-semibold uppercase rounded">
                      Rx Only
                    </span>
                  </div>
                </div>

                <div className="mt-2.5 pt-2 border-t border-neutral-200 flex justify-between text-[11px] text-neutral-700">
                  <div>
                    <span className="font-semibold text-neutral-900">Dr. H. Vance, MD</span>
                    <span className="text-[10px] text-neutral-500 ml-1">FACC</span>
                  </div>
                  <div className="font-mono text-[10px] text-neutral-500">
                    Ph: (555) 019-4821
                  </div>
                </div>
              </div>

              {/* Patient Banner with On-Device Masking Stamp */}
              <div className="bg-neutral-100/80 rounded border border-neutral-200 p-2.5 mb-4 text-[11px] relative">
                <div className="grid grid-cols-2 gap-y-1">
                  <div>
                    <span className="text-neutral-500">Patient:</span>{" "}
                    <span className="font-semibold font-mono text-neutral-800">
                      PT-***-7182
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-neutral-500">Date:</span>{" "}
                    <span className="font-mono text-neutral-800">10-OCT-2026</span>
                  </div>
                  <div>
                    <span className="text-neutral-500">Age:</span>{" "}
                    <span className="text-neutral-800">58 yrs</span> / Male
                  </div>
                  <div className="text-right">
                    <span className="text-neutral-500">Ref:</span>{" "}
                    <span className="font-mono text-neutral-800">RX-89412</span>
                  </div>
                </div>

                <div className="mt-1 pt-1 border-t border-neutral-200 flex items-center justify-between text-[9px] text-emerald-700">
                  <span className="flex items-center gap-1 font-mono">
                    <ShieldCheck className="h-3 w-3 text-emerald-600" />
                    On-Device Masked Name: John D. [REDACTED]
                  </span>
                  <span className="text-neutral-400">DOB: [MASKED]</span>
                </div>
              </div>

              {/* Rx Symbol */}
              <div className="text-2xl font-serif font-black text-neutral-800 mb-2 leading-none italic">
                ℞
              </div>

              {/* Medication Lines with Interactive OCR Boxes */}
              <div className="space-y-3.5 my-2">
                {medications.map((med) => {
                  const isSelected = selectedMedId === med.id;
                  const isUncertain = med.handwriting_uncertain;
                  const hide = highlightUncertainOnly && !isUncertain;

                  if (hide) return null;

                  return (
                    <div
                      key={med.id}
                      onClick={() => onSelectMed(isSelected ? null : med.id)}
                      className={cn(
                        "relative p-2.5 rounded-md transition-all duration-200 cursor-pointer group",
                        showOverlays && isUncertain
                          ? "bg-amber-100/70 border-2 border-amber-500 shadow-[0_0_12px_rgba(245,158,11,0.25)]"
                          : showOverlays && isSelected
                          ? "bg-cyan-50/90 border-2 border-cyan-600 shadow-md ring-1 ring-cyan-400"
                          : showOverlays
                          ? "hover:bg-neutral-100/90 border border-neutral-300"
                          : "border border-transparent"
                      )}
                    >
                      {/* OCR Tag Label */}
                      {showOverlays && (
                        <div className="absolute -top-2.5 right-2 flex items-center gap-1">
                          {isUncertain ? (
                            <span className="inline-flex items-center gap-1 px-1.5 py-0.2 bg-amber-500 text-amber-950 font-bold text-[9px] rounded uppercase shadow-sm animate-pulse-slow">
                              <AlertTriangle className="h-2.5 w-2.5" />
                              Unclear Handwriting
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-0.5 px-1.5 py-0.2 bg-neutral-900/80 text-white font-mono text-[9px] rounded">
                              Line #{med.line_number} • {Math.round(med.confidence * 100)}%
                            </span>
                          )}
                        </div>
                      )}

                      {/* Handwritten Style Simulation for Line 3 (Uncertain) */}
                      {isUncertain ? (
                        <div>
                          <div className="flex items-baseline justify-between">
                            <span className="font-serif italic font-bold text-neutral-900 text-sm tracking-wide">
                              Warfarin (Coumadin)
                            </span>
                            <span className="font-serif italic text-amber-900 font-extrabold text-sm border-b-2 border-amber-400 border-dashed px-1">
                              ~5 mg (?)
                            </span>
                          </div>
                          <p className="font-serif italic text-neutral-600 text-xs mt-0.5">
                            Sig: 1 tab PO qPM (18:00) - titrate per INR
                          </p>
                          <div className="mt-1 text-[10px] text-amber-800 bg-amber-200/60 rounded px-1.5 py-0.5 flex items-center gap-1 font-sans font-medium">
                            <AlertTriangle className="h-3 w-3 shrink-0 text-amber-700" />
                            <span>Numeral ambiguous ('2.5' vs '5' mg). Pharmacist verify.</span>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <div className="flex items-baseline justify-between">
                            <span className="font-serif font-bold text-neutral-900 text-sm tracking-tight">
                              {med.name}
                            </span>
                            <span className="font-mono text-neutral-800 font-bold text-xs bg-neutral-200/70 px-1 rounded">
                              {med.dosage}
                            </span>
                          </div>
                          <p className="text-[11px] text-neutral-600 mt-0.5 font-sans">
                            Sig: {med.frequency}
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Bottom Doctor Signature Block */}
              <div className="mt-6 pt-3 border-t border-neutral-300 flex justify-between items-end">
                <div className="text-[10px] text-neutral-500 font-mono">
                  Dispense as Written
                  <br />
                  Refills: 0 (Zero)
                </div>
                <div className="text-right">
                  <div className="font-serif italic text-neutral-700 text-sm -mb-1 transform -rotate-3 select-none">
                    Harold Vance, M.D.
                  </div>
                  <div className="w-36 border-b border-neutral-800 mt-1" />
                  <span className="text-[9px] uppercase tracking-wider text-neutral-500">
                    Physician Signature
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Viewport Floating Quick Reset Helper */}
        <div className="absolute bottom-3 left-3 bg-neutral-900/80 backdrop-blur-md border border-neutral-800 text-[11px] text-neutral-400 px-2.5 py-1 rounded-full flex items-center gap-2 pointer-events-none">
          <Maximize2 className="h-3 w-3 text-cyan-400" />
          <span>Drag to pan • Click lines to inspect</span>
        </div>
      </div>
    </div>
  );
}
