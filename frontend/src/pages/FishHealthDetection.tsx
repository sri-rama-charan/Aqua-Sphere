import { useState, useEffect } from "react";
import ImageUpload from "@/components/ImageUpload";
import DetectionButton from "@/components/DetectionButton";
import ResultsSection, { DetectionResult } from "@/components/ResultsSection";
import ErrorMessage from "@/components/ErrorMessage";
import { LanguageSelector } from "@/components/LanguageSelector";
import { Language, getTranslation } from "@/lib/translations";

const API_URL = import.meta.env.DEV
  ? "/api"
  : import.meta.env.VITE_API_URL || "/api";

const FishHealthDetection = () => {
  const [image, setImage] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<Language>("en");

  // Load language from localStorage on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem("preferredLanguage") as Language;
    if (savedLanguage && (savedLanguage === "en" || savedLanguage === "te")) {
      setLanguage(savedLanguage);
    }
  }, []);

  // Save language to localStorage when changed
  const handleLanguageChange = (newLanguage: string) => {
    const lang = newLanguage as Language;
    setLanguage(lang);
    localStorage.setItem("preferredLanguage", lang);
    
    // Clear results when language changes so user can re-detect in new language
    if (result) {
      setResult(null);
    }
  };

  const handleImageSelect = (selectedImage: string, file?: File) => {
    setImage(selectedImage);
    if (file) {
      setImageFile(file);
    }
    setResult(null);
    setError(null);
  };

  const handleImageClear = () => {
    setImage(null);
    setImageFile(null);
    setResult(null);
    setError(null);
  };

  const handleDetect = async () => {
    if (!imageFile) {
      setError(getTranslation(language, "errorUpload"));
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", imageFile);
      formData.append("language", language);

      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();

      const mappedResult: DetectionResult = {
        diseaseName: data.disease_name || getTranslation(language, "unknown"),
        confidence: Math.round((data.confidence || 0) * 100),
        cause: data.cause || getTranslation(language, "errorAnalysis"),
        severity: data.severity || getTranslation(language, "unknown"),
        treatment: data.treatment || getTranslation(language, "consultDoctor"),
        warning: data.warning || undefined,
      };

      setResult(mappedResult);
    } catch (err) {
      setError(getTranslation(language, "errorAnalysis"));
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    handleDetect();
  };

  return (
    <div className="space-y-6 px-4 mt-6">
      {/* Language Selector */}
      <div className="flex justify-end">
        <LanguageSelector 
          currentLanguage={language} 
          onLanguageChange={handleLanguageChange} 
        />
      </div>

      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold mb-2">
            {language === "en" ? "Detect Fish Disease" : "చేపల వ్యాధిని గుర్తించండి"}
          </h2>
          <p className="text-sm text-muted-foreground">
            {language === "en" 
              ? "Upload a fish image to detect diseases and get treatment recommendations"
              : "వ్యాధిలను గుర్తించడానికి మరియు చికిత్స సిఫార్సులను పొందడానికి చేపల చిత్రాన్ని అప్‌లోడ్ చేయండి"}
          </p>
        </div>

        <ImageUpload
          image={image}
          onImageSelect={handleImageSelect}
          onImageClear={handleImageClear}
          language={language}
        />

        {image && !result && !error && (
          <DetectionButton 
            isLoading={isLoading} 
            onDetect={handleDetect}
            language={language}
          />
        )}

        {error && <ErrorMessage message={error} onRetry={handleRetry} />}

        {result && <ResultsSection result={result} language={language} />}
      </div>

      <footer className="mt-8 text-center px-4">
        <p className="text-xs text-muted-foreground">
          {language === "en" 
            ? "Powered by AI • For professional aquaculture use"
            : "AI ద్వారా శక్తివంతం • వృత్తిపరమైన జల వ్యవసాయ వినియోగం కోసం"}
        </p>
      </footer>
    </div>
  );
};

export default FishHealthDetection;
