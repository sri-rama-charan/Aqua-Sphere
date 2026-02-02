import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, Thermometer } from "lucide-react";
import { TemperatureRiskCard } from "./TemperatureRiskCard";

const SPECIES = [
  "Tilapia",
  "Catfish",
  "Carp",
  "Shrimp",
  "Salmon",
  "Trout",
  "Milkfish",
  "Bass",
  "Pangasius",
  "Eel",
];

export function ManualTemperatureChecker() {
  const [temperature, setTemperature] = useState("");
  const [species, setSpecies] = useState("Tilapia");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [riskData, setRiskData] = useState(null);

  const handleCheck = async () => {
    if (!temperature.trim()) {
      setError("Please enter a temperature");
      return;
    }

    const temp = parseFloat(temperature);
    if (isNaN(temp) || temp < -50 || temp > 60) {
      setError("Temperature must be between -50°C and 60°C");
      return;
    }

    setLoading(true);
    setError("");
    setRiskData(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/temperature/assess-risk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          temperature: temp,
          species: species,
          location: "Manual Entry",
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to assess temperature");
      }

      const data = await response.json();
      setRiskData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error assessing temperature");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Thermometer className="w-5 h-5" />
            Manual Temperature Assessment
          </CardTitle>
          <CardDescription>
            Check risk level for your current water temperature reading
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Temperature Input */}
            <div>
              <label className="text-sm font-medium">Water Temperature (°C)</label>
              <div className="flex gap-2 mt-1">
                <Input
                  type="number"
                  placeholder="Enter temperature (e.g., 28)"
                  value={temperature}
                  onChange={(e) => setTemperature(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleCheck()}
                  min="-50"
                  max="60"
                  step="0.1"
                  className="flex-1"
                />
                <span className="flex items-center font-semibold text-gray-600">°C</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">Valid range: -50°C to 60°C</p>
            </div>

            {/* Species Selection */}
            <div>
              <label className="text-sm font-medium">Aquaculture Species</label>
              <Select value={species} onValueChange={setSpecies}>
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {SPECIES.map((s) => (
                    <SelectItem key={s} value={s}>
                      {s}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Check Button */}
            <Button
              onClick={handleCheck}
              disabled={loading}
              className="w-full"
              size="lg"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Assessing...
                </>
              ) : (
                <>
                  <Thermometer className="w-4 h-4 mr-2" />
                  Assess Temperature Risk
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Risk Assessment Result */}
      {riskData && <TemperatureRiskCard {...riskData} />}
    </div>
  );
}

export default ManualTemperatureChecker;
