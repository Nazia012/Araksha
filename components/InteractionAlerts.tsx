"use client";

import React, { useState } from "react";
import {
  AlertOctagon,
  AlertTriangle,
  Info,
  ShieldAlert,
  BookOpen,
  ChevronDown,
  ChevronUp,
  Dna,
  ExternalLink,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { InteractionAlert } from "@/types/audit";
import { cn } from "@/lib/utils";

interface InteractionAlertsProps {
  interactions: InteractionAlert[];
  onAcknowledgeAlert?: (id: string) => void;
}

export function InteractionAlerts({
  interactions,
  onAcknowledgeAlert,
}: InteractionAlertsProps) {
  const [expandedId, setExpandedId] = useState<string | null>(
    interactions.length > 0 ? interactions[0].id : null
  );

  const toggleExpand = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  const majorCount = interactions.filter((i) => i.severity === "major").length;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldAlert className="h-4 w-4 text-destructive" />
          <h3 className="text-sm font-semibold tracking-tight text-foreground">
            Drug-Drug Interactions ({interactions.length})
          </h3>
        </div>
        <div className="flex items-center gap-2">
          {majorCount > 0 && (
            <Badge variant="destructive" className="animate-pulse-slow text-[11px] font-mono">
              {majorCount} Major Contraindication
            </Badge>
          )}
          <Badge variant="outline" className="text-[10px] text-muted-foreground font-mono">
            Deterministic Engine: Active
          </Badge>
        </div>
      </div>

      {interactions.length === 0 ? (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-950/20 p-6 text-center text-sm text-emerald-300">
          <CheckCircle2 className="mx-auto h-8 w-8 text-emerald-400 mb-2" />
          <p className="font-semibold">No Known Drug Interactions Detected</p>
          <p className="text-xs text-emerald-400/80 mt-1">
            All extracted medications were verified against DrugBank and clinical interaction databases.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {interactions.map((alert) => {
            const isMajor = alert.severity === "major";
            const isModerate = alert.severity === "moderate";
            const isExpanded = expandedId === alert.id;

            return (
              <div
                key={alert.id}
                className={cn(
                  "rounded-xl border transition-all duration-200 overflow-hidden shadow-sm",
                  isMajor
                    ? "border-red-500/70 bg-gradient-to-r from-red-950/30 via-card to-card shadow-[0_0_20px_rgba(239,68,68,0.12)]"
                    : isModerate
                    ? "border-amber-500/60 bg-gradient-to-r from-amber-950/25 via-card to-card"
                    : "border-cyan-500/50 bg-card/60"
                )}
              >
                {/* Header Banner */}
                <div
                  onClick={() => toggleExpand(alert.id)}
                  className={cn(
                    "p-4 cursor-pointer flex items-start justify-between gap-3 select-none",
                    isMajor ? "bg-red-500/10 hover:bg-red-500/15" : "hover:bg-muted/40"
                  )}
                >
                  <div className="flex items-start gap-3">
                    <div
                      className={cn(
                        "rounded-lg p-2 shrink-0 mt-0.5",
                        isMajor
                          ? "bg-red-500/20 text-red-400 ring-1 ring-red-500/40"
                          : isModerate
                          ? "bg-amber-500/20 text-amber-400 ring-1 ring-amber-500/40"
                          : "bg-cyan-500/20 text-cyan-400"
                      )}
                    >
                      {isMajor ? (
                        <AlertOctagon className="h-5 w-5" />
                      ) : isModerate ? (
                        <AlertTriangle className="h-5 w-5" />
                      ) : (
                        <Info className="h-5 w-5" />
                      )}
                    </div>

                    <div>
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <Badge
                          variant={isMajor ? "destructive" : isModerate ? "warning" : "info"}
                          className="text-[10px] uppercase font-bold tracking-wider"
                        >
                          {alert.severity} Risk
                        </Badge>
                        <span className="text-[11px] font-mono text-muted-foreground">
                          {alert.drugs_involved[0]} ↔ {alert.drugs_involved[1]}
                        </span>
                      </div>

                      <h4
                        className={cn(
                          "text-sm font-bold tracking-tight",
                          isMajor ? "text-red-200" : isModerate ? "text-amber-200" : "text-foreground"
                        )}
                      >
                        {alert.title}
                      </h4>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {alert.description}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-1.5 shrink-0 text-muted-foreground">
                    <Button
                      size="icon"
                      variant="ghost"
                      className="h-8 w-8 text-muted-foreground hover:text-foreground"
                    >
                      {isExpanded ? (
                        <ChevronUp className="h-4 w-4" />
                      ) : (
                        <ChevronDown className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                {/* Expanded Details Body */}
                {isExpanded && (
                  <div className="p-4 pt-0 border-t border-border/40 mt-1 space-y-4 text-xs">
                    {/* Biological Mechanism Card */}
                    <div className="rounded-lg border border-border/60 bg-muted/30 p-3">
                      <div className="flex items-center gap-1.5 text-xs font-semibold text-foreground mb-1.5">
                        <Dna className="h-3.5 w-3.5 text-cyan-400" />
                        <span>Biological Mechanism</span>
                      </div>
                      <p className="text-xs leading-relaxed text-muted-foreground">
                        {alert.mechanism}
                      </p>
                    </div>

                    {/* Clinical Action Directive */}
                    <div
                      className={cn(
                        "rounded-lg p-3 border",
                        isMajor
                          ? "bg-red-950/25 border-red-500/40 text-red-200"
                          : "bg-amber-950/20 border-amber-500/40 text-amber-200"
                      )}
                    >
                      <span className="font-bold text-[11px] uppercase tracking-wider block mb-1">
                        Mandatory Clinical Action
                      </span>
                      <p className="text-xs leading-relaxed font-sans">
                        {alert.clinical_action}
                      </p>
                      {alert.management_recommendation && (
                        <p className="mt-2 text-[11px] opacity-90 italic">
                          Recommendation: {alert.management_recommendation}
                        </p>
                      )}
                    </div>

                    {/* Trusted Citation Source */}
                    <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-border/30 text-[11px] text-muted-foreground">
                      <div className="flex items-center gap-1.5">
                        <BookOpen className="h-3.5 w-3.5 text-primary" />
                        <span className="font-semibold text-foreground">Evidence Source:</span>
                        <span className="font-mono text-muted-foreground">{alert.citation_source}</span>
                      </div>

                      {onAcknowledgeAlert && (
                        <Button
                          size="sm"
                          variant="outline"
                          className="h-7 text-xs border-border/80 hover:bg-muted"
                          onClick={() => onAcknowledgeAlert(alert.id)}
                        >
                          Acknowledge Warning
                        </Button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
