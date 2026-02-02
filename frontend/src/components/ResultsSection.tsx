import {
  Bug,
  Percent,
  HelpCircle,
  AlertTriangle,
  Stethoscope,
} from "lucide-react";
import ResultCard from "./ResultCard";
import ConfidenceWarning from "./ConfidenceWarning";
import { Language, getTranslation } from "@/lib/translations";

export interface DetectionResult {
  diseaseName: string;
  confidence: number;
  cause: string;
  severity: "Low" | "Medium" | "High" | "Unknown" | string;
  treatment: string;
  warning?: {
    level: "high" | "medium";
    message: string;
  };
}

interface ResultsSectionProps {
  result: DetectionResult;
  language: Language;
}

const getSeverityVariant = (severity: string) => {
  // Handle both English and Telugu severity levels
  const lowerSeverity = severity.toLowerCase();
  if (lowerSeverity.includes("low") || severity === "తక్కువ") {
    return "success";
  } else if (lowerSeverity.includes("medium") || severity === "మధ్యస్థం") {
    return "warning";
  } else if (lowerSeverity.includes("high") || severity === "అధికం") {
    return "destructive";
  }
  return "default";
};

const ResultsSection = ({ result, language }: ResultsSectionProps) => {
  return (
    <section className="px-4 space-y-3">
      <h2 className="text-lg font-semibold text-foreground mb-4 animate-fade-in">
        {language === "en" ? "Detection Results" : "గుర్తింపు ఫలితాలు"}
      </h2>

      {result.warning && (
        <div className="mb-4">
          <ConfidenceWarning warning={result.warning} language={language} />
        </div>
      )}

      <ResultCard
        icon={Bug}
        label={getTranslation(language, "diseaseName")}
        value={result.diseaseName}
        variant="info"
        delay={0.1}
      />

      <ResultCard
        icon={Percent}
        label={getTranslation(language, "confidence")}
        value={`${result.confidence}%`}
        variant={result.confidence >= 80 ? "success" : "warning"}
        delay={0.15}
      />

      <ResultCard
        icon={HelpCircle}
        label={getTranslation(language, "cause")}
        value={result.cause}
        variant="default"
        delay={0.2}
      />

      <ResultCard
        icon={AlertTriangle}
        label={getTranslation(language, "severity")}
        value={result.severity}
        variant={getSeverityVariant(result.severity)}
        delay={0.25}
      />

      <ResultCard
        icon={Stethoscope}
        label={getTranslation(language, "treatment")}
        value={result.treatment}
        variant="success"
        delay={0.3}
      />
    </section>
  );
};

export default ResultsSection;
