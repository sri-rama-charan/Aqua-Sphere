import React, { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertTriangle, Thermometer, MapPin, TrendingUp, CheckCircle } from "lucide-react";

interface TemperatureReading {
  temperature: number;
  unit: string;
}

interface SafeRange {
  min: number;
  max: number;
}

interface TemperatureRiskProps {
  current_temperature: number;
  safe_range: SafeRange;
  risk_level: "normal" | "caution" | "high_risk";
  risk_label: string;
  color_code: string;
  urgency_score: number;
  possible_issues: string[];
  recommended_actions: string[];
  species: string;
  disease_risks: Record<string, string>;
}

const riskColors = {
  normal: { bg: "bg-green-50", border: "border-green-200", text: "text-green-900" },
  caution: { bg: "bg-yellow-50", border: "border-yellow-200", text: "text-yellow-900" },
  high_risk: { bg: "bg-red-50", border: "border-red-200", text: "text-red-900" },
};

const riskIcons = {
  normal: <CheckCircle className="w-6 h-6 text-green-600" />,
  caution: <AlertTriangle className="w-6 h-6 text-yellow-600" />,
  high_risk: <AlertTriangle className="w-6 h-6 text-red-600" />,
};

export function TemperatureRiskCard(props: TemperatureRiskProps) {
  const colors = riskColors[props.risk_level];
  const isOutOfRange =
    props.current_temperature < props.safe_range.min ||
    props.current_temperature > props.safe_range.max;
  const urgencyLabel =
    props.urgency_score > 70
      ? "High"
      : props.urgency_score > 40
        ? "Moderate"
        : "Low";

  return (
    <Card className={`border-2 ${colors.border}`}>
      <CardHeader className={`${colors.bg} rounded-t-lg`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {riskIcons[props.risk_level]}
            <div>
              <CardTitle className={colors.text}>{props.risk_label}</CardTitle>
              <CardDescription>Temperature Risk Assessment</CardDescription>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">{props.current_temperature}°C</div>
            <div className="text-sm text-gray-600">Current</div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-6">
        {/* Species & Location Info */}
        <div className="mb-4 flex items-center gap-2">
          <Thermometer className="w-4 h-4 text-gray-600" />
          <span className="font-medium">{props.species}</span>
        </div>

        {/* Safe Range Display */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <div className="text-sm font-semibold mb-2">Safe Temperature Range</div>
          <div className="flex justify-between items-center">
            <div className="text-center flex-1">
              <div className="text-2xl font-bold text-blue-600">{props.safe_range.min}°C</div>
              <div className="text-xs text-gray-600">Minimum</div>
            </div>
            <div className="text-gray-400 mx-4">—</div>
            <div className="text-center flex-1">
              <div className="text-2xl font-bold text-blue-600">{props.safe_range.max}°C</div>
              <div className="text-xs text-gray-600">Maximum</div>
            </div>
          </div>

          {/* Temperature Status Bar */}
          <div className="mt-3">
            <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden flex">
              <div
                className="bg-blue-600"
                style={{
                  width: `${Math.max(0, Math.min(100, ((props.safe_range.max - props.safe_range.min) / 50) * 100))}%`,
                }}
              />
            </div>
            {isOutOfRange && (
              <div className="text-xs font-semibold mt-1 text-red-600">
                ⚠️ OUT OF SAFE RANGE
              </div>
            )}
          </div>
        </div>

        {/* Urgency Level */}
        <div className="mb-6">
          <div className="text-sm font-semibold mb-2">Priority Level: {urgencyLabel}</div>
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                props.urgency_score > 70
                  ? "bg-red-600"
                  : props.urgency_score > 40
                    ? "bg-yellow-600"
                    : "bg-green-600"
              }`}
              style={{ width: `${props.urgency_score}%` }}
            />
          </div>
        </div>

        {/* Possible Issues */}
        {props.possible_issues.length > 0 && (
          <div className="mb-6">
            <h3 className="font-semibold mb-2 text-sm">⚠️ Possible Issues</h3>
            <ul className="space-y-1">
              {props.possible_issues.map((issue, idx) => (
                <li key={idx} className="text-sm text-gray-700 flex gap-2">
                  <span className="text-gray-400">•</span>
                  {issue}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommended Actions */}
        {props.recommended_actions.length > 0 && (
          <div className="mb-6">
            <h3 className="font-semibold mb-2 text-sm flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Recommended Actions
            </h3>
            <ol className="space-y-2">
              {props.recommended_actions.map((action, idx) => (
                <li key={idx} className="text-sm text-gray-700 flex gap-2">
                  <span className="font-semibold text-gray-500 min-w-5">{idx + 1}.</span>
                  {action}
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Disease Risk Factors */}
        {Object.keys(props.disease_risks).length > 0 && (
          <div className="border-t pt-4">
            <h3 className="font-semibold mb-3 text-sm">Disease Risk Factors</h3>
            <div className="space-y-2">
              {Object.entries(props.disease_risks).map(([disease, risk]) => (
                <div key={disease} className="flex justify-between items-start text-sm">
                  <span className="text-gray-700 capitalize">{disease.replace("_", " ")}:</span>
                  <span className="font-medium text-gray-900">{risk}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
