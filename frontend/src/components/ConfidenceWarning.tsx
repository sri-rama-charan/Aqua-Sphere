import { AlertTriangle, AlertCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

interface ConfidenceWarningProps {
  warning: {
    level: "high" | "medium";
    message: string;
  };
}

const ConfidenceWarning = ({ warning }: ConfidenceWarningProps) => {
  const isHighWarning = warning.level === "high";

  return (
    <Alert 
      variant={isHighWarning ? "destructive" : "default"}
      className={`animate-fade-in ${
        isHighWarning 
          ? "border-red-500 bg-red-50 dark:bg-red-950/20" 
          : "border-yellow-500 bg-yellow-50 dark:bg-yellow-950/20"
      }`}
    >
      {isHighWarning ? (
        <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
      ) : (
        <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
      )}
      <AlertTitle className={`${
        isHighWarning 
          ? "text-red-800 dark:text-red-300" 
          : "text-yellow-800 dark:text-yellow-300"
      }`}>
        {isHighWarning ? "Low Confidence Detection" : "Moderate Confidence"}
      </AlertTitle>
      <AlertDescription className={`${
        isHighWarning 
          ? "text-red-700 dark:text-red-400" 
          : "text-yellow-700 dark:text-yellow-400"
      } whitespace-pre-line`}>
        {warning.message}
      </AlertDescription>
    </Alert>
  );
};

export default ConfidenceWarning;
