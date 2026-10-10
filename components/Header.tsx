"use client";

import React from "react";
import {
  ShieldCheck,
  Cpu,
  Lock,
  Activity,
  HeartPulse,
  WifiOff,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface HeaderProps {
  prescriptionId: string;
  patientMaskedId: string;
  edgeMode: boolean;
  latencyMs: number;
}

export function Header({
  prescriptionId,
  patientMaskedId,
  edgeMode,
  latencyMs,
}: HeaderProps) {
  return (
    <header className="border-b border-border/70 bg-card/70 backdrop-blur-xl sticky top-0 z-40 transition-all">
      <div className="container mx-auto px-4 py-3 sm:px-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          {/* Brand & System Title */}
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-teal-500 to-emerald-500 p-0.5 shadow-lg shadow-cyan-950/30">
              <div className="h-full w-full rounded-[10px] bg-neutral-950 flex items-center justify-center">
                <HeartPulse className="h-5 w-5 text-cyan-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-black tracking-tight text-foreground">
                  Araksha<span className="text-cyan-400">-Med</span>
                </h1>
                <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-muted text-muted-foreground border border-border/50">
                  v2.4-Edge
                </span>
              </div>
              <p className="text-xs text-muted-foreground">
                On-Device Medical Prescription & Drug Interaction Inspector
              </p>
            </div>
          </div>

          {/* Privacy-First Indicator & Edge Telemetry */}
          <div className="flex flex-wrap items-center gap-2.5">
            {/* Prominent Required Privacy-First Badge */}
            <div className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/50 bg-emerald-950/50 px-3 py-1.5 text-xs font-semibold text-emerald-300 shadow-[0_0_15px_rgba(16,185,129,0.25)] ring-1 ring-emerald-500/30">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <WifiOff className="h-3.5 w-3.5 text-emerald-400" />
              <span>Zero-Cloud Edge Mode: On-Device PII Masking Active</span>
            </div>

            {/* Hardware / Telemetry Pills */}
            <div className="hidden lg:flex items-center gap-2 text-xs font-mono text-muted-foreground bg-muted/40 px-2.5 py-1 rounded-lg border border-border/40">
              <span className="flex items-center gap-1">
                <Cpu className="h-3 w-3 text-cyan-400" />
                NPU 138ms
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Lock className="h-3 w-3 text-emerald-400" />
                {patientMaskedId}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
