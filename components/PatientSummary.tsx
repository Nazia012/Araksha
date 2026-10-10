"use client";

import React, { useState } from "react";
import {
  Sparkles,
  Sun,
  CloudSun,
  Moon,
  AlertCircle,
  Clock,
  Apple,
  ShieldCheck,
  CheckCircle2,
  ChevronRight,
  Info,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { PatientSummary as PatientSummaryType, ScheduleItem } from "@/types/audit";
import { cn } from "@/lib/utils";

interface PatientSummaryProps {
  summary: PatientSummaryType;
}

export function PatientSummary({ summary }: PatientSummaryProps) {
  const [activeTab, setActiveTab] = useState("all");

  const renderScheduleItems = (
    items: ScheduleItem[],
    timingName: string,
    icon: React.ReactNode,
    timingColor: string
  ) => {
    if (!items || items.length === 0) {
      return (
        <div className="rounded-lg border border-border/40 bg-muted/20 p-3 text-xs text-muted-foreground text-center">
          No medication scheduled for {timingName}.
        </div>
      );
    }

    return (
      <div className="space-y-2.5">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 rounded-xl border border-border/60 bg-card/60 p-3.5 shadow-sm transition-all hover:border-primary/40 hover:bg-muted/30"
          >
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-sm text-foreground">
                  {item.med}
                </span>
                <span className="font-mono text-xs px-2 py-0.5 rounded bg-muted text-muted-foreground border border-border/50">
                  {item.dose}
                </span>
                {item.with_food && (
                  <Badge variant="info" className="text-[10px] font-normal">
                    With food
                  </Badge>
                )}
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {item.instructions}
              </p>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <span
                className={cn(
                  "inline-flex items-center gap-1 text-[11px] font-medium px-2 py-1 rounded-full border",
                  timingColor
                )}
              >
                {icon}
                {timingName}
              </span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <Card className="border-border/70 bg-card/50 backdrop-blur-md overflow-hidden">
      {/* Card Header with Gemma Badge */}
      <CardHeader className="pb-3 border-b border-border/40 bg-muted/20">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <div className="rounded-lg bg-gradient-to-tr from-cyan-500/20 to-purple-500/20 p-2 text-cyan-400 border border-cyan-500/30">
              <Sparkles className="h-4 w-4 animate-pulse-slow" />
            </div>
            <div>
              <CardTitle className="text-base font-bold text-foreground">
                How to take your medication (Gemma Plain-Language Assistant)
              </CardTitle>
              <CardDescription className="text-xs text-muted-foreground mt-0.5">
                On-device language model translation simplified for patients
              </CardDescription>
            </div>
          </div>

          <Badge variant="outline" className="text-[11px] border-cyan-500/30 bg-cyan-950/20 text-cyan-300 font-mono gap-1">
            <ShieldCheck className="h-3 w-3 text-cyan-400" />
            Gemma-2B Edge
          </Badge>
        </div>

        {summary.instructions && (
          <div className="mt-3 rounded-lg bg-primary/10 border border-primary/20 p-3 text-xs text-foreground/90 leading-relaxed">
            {summary.instructions}
          </div>
        )}
      </CardHeader>

      <CardContent className="p-5 space-y-5">
        {/* Timing Pill Schedule Breakdown */}
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {/* Morning Card */}
            <div className="rounded-xl border border-amber-500/30 bg-amber-950/10 p-3.5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-xs font-bold text-amber-300 uppercase tracking-wider">
                  <Sun className="h-4 w-4 text-amber-400" />
                  Morning
                </span>
                <span className="text-[10px] font-mono text-muted-foreground">08:00 AM</span>
              </div>
              {renderScheduleItems(
                summary.schedule.morning,
                "Morning",
                <Sun className="h-3 w-3" />,
                "text-amber-300 bg-amber-950/40 border-amber-500/40"
              )}
            </div>

            {/* Afternoon Card */}
            <div className="rounded-xl border border-cyan-500/30 bg-cyan-950/10 p-3.5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-xs font-bold text-cyan-300 uppercase tracking-wider">
                  <CloudSun className="h-4 w-4 text-cyan-400" />
                  Afternoon
                </span>
                <span className="text-[10px] font-mono text-muted-foreground">13:00 PM</span>
              </div>
              {renderScheduleItems(
                summary.schedule.afternoon,
                "Afternoon",
                <CloudSun className="h-3 w-3" />,
                "text-cyan-300 bg-cyan-950/40 border-cyan-500/40"
              )}
            </div>

            {/* Night Card */}
            <div className="rounded-xl border border-indigo-500/30 bg-indigo-950/10 p-3.5 space-y-2">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-xs font-bold text-indigo-300 uppercase tracking-wider">
                  <Moon className="h-4 w-4 text-indigo-400" />
                  Night
                </span>
                <span className="text-[10px] font-mono text-muted-foreground">20:00 PM</span>
              </div>
              {renderScheduleItems(
                summary.schedule.night,
                "Night",
                <Moon className="h-3 w-3" />,
                "text-indigo-300 bg-indigo-950/40 border-indigo-500/40"
              )}
            </div>
          </div>

          {/* As Needed PRN Section */}
          {summary.schedule.as_needed && summary.schedule.as_needed.length > 0 && (
            <div className="rounded-xl border border-red-500/40 bg-red-950/10 p-4">
              <div className="flex items-center gap-2 mb-3">
                <AlertCircle className="h-4 w-4 text-red-400" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-red-300">
                  As Needed (PRN) & Acute Warnings
                </h4>
              </div>
              <div className="space-y-2">
                {summary.schedule.as_needed.map((item, i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-red-500/30 bg-card/60 p-3 text-xs space-y-1"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-red-200">{item.med}</span>
                      <span className="font-mono text-[11px] text-muted-foreground bg-muted px-2 py-0.5 rounded">
                        {item.dose}
                      </span>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">
                      {item.instructions}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Dietary & Lifestyle Cautions */}
        {summary.dietary_notes && summary.dietary_notes.length > 0 && (
          <div className="rounded-xl border border-border/60 bg-muted/30 p-3.5 space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-foreground">
              <Apple className="h-3.5 w-3.5 text-emerald-400" />
              <span>Dietary & Lifestyle Considerations</span>
            </div>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-muted-foreground">
              {summary.dietary_notes.map((note, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-primary font-bold mt-0.5">•</span>
                  <span>{note}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Clinical Disclaimer Requirement */}
        <div className="rounded-xl border border-amber-500/30 bg-amber-950/15 p-3 text-center">
          <p className="text-xs font-medium text-amber-200/90 leading-relaxed flex items-center justify-center gap-1.5">
            <Info className="h-3.5 w-3.5 shrink-0 text-amber-400" />
            <span>{summary.clinical_disclaimer}</span>
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
