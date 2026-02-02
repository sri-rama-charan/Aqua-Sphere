import { useState } from "react";
import ImageUpload from "@/components/ImageUpload";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2 } from "lucide-react";

const API_URL = import.meta.env.DEV
  ? "/api"
  : import.meta.env.VITE_API_URL || "/api";

const FishSeedCount = () => {
  const [image, setImage] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [count, setCount] = useState<number | null>(null);
  const [confidencePercent, setConfidencePercent] = useState(7);

  const handleImageSelect = (selectedImage: string, file?: File) => {
    setImage(selectedImage);
    if (file) {
      setImageFile(file);
    }
    setCount(null);
    setError(null);
  };

  const handleImageClear = () => {
    setImage(null);
    setImageFile(null);
    setCount(null);
    setError(null);
  };

  const handleCount = async () => {
    if (!imageFile) {
      setError("Please upload an image first.");
      return;
    }

    setLoading(true);
    setError(null);
    setCount(null);

    try {
      const formData = new FormData();
      formData.append("file", imageFile);
      formData.append("confidence", String(confidencePercent / 100));

      const response = await fetch(`${API_URL}/seed-count`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to count fish seeds");
      }

      const data = await response.json();
      setCount(data.count ?? 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error counting fish seeds");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 px-4 mt-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">🐟 Fish Seed Counter</h2>
        <p className="text-sm text-muted-foreground">
          Upload a fry image and get an estimated count using the detection model.
        </p>
      </div>

      <ImageUpload
        image={image}
        onImageSelect={handleImageSelect}
        onImageClear={handleImageClear}
        language="en"
      />

      <Card>
        <CardHeader>
          <CardTitle>Detection Sensitivity</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="text-sm text-muted-foreground">
            Recommended: 5–10% confidence (model performs better here).
          </div>
          <div className="flex items-center gap-3">
            <input
              type="range"
              min={1}
              max={30}
              step={1}
              value={confidencePercent}
              onChange={(e) => setConfidencePercent(Number(e.target.value))}
              className="w-full"
            />
            <div className="min-w-[60px] text-right text-sm font-semibold">
              {confidencePercent}%
            </div>
          </div>
        </CardContent>
      </Card>

      <Button
        onClick={handleCount}
        disabled={loading || !imageFile}
        className="w-full"
        size="lg"
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Counting...
          </>
        ) : (
          "Count Fish Seeds"
        )}
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {count !== null && (
        <Card>
          <CardHeader>
            <CardTitle>Estimated Count</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-primary">{count}</div>
            <div className="text-sm text-muted-foreground mt-2">
              Confidence threshold used: {confidencePercent}%
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default FishSeedCount;
