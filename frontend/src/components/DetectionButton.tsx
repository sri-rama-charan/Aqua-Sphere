import { Scan, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Language, getTranslation } from "@/lib/translations";

interface DetectionButtonProps {
  isLoading: boolean;
  onDetect: () => void;
  language: Language;
}

const DetectionButton = ({ isLoading, onDetect, language }: DetectionButtonProps) => {
  return (
    <section className="px-4 animate-fade-in" style={{ animationDelay: "0.2s" }}>
      <Button
        size="lg"
        className="w-full"
        onClick={onDetect}
        disabled={isLoading}
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin-slow" />
            {getTranslation(language, "analyzing")}
          </>
        ) : (
          <>
            <Scan className="w-5 h-5" />
            {getTranslation(language, "detectDisease")}
          </>
        )}
      </Button>
      
      {isLoading && (
        <p className="text-center text-sm text-muted-foreground mt-3 animate-pulse-soft">
          {getTranslation(language, "analyzing")}
        </p>
      )}
    </section>
  );
};

export default DetectionButton;
