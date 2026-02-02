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
import { Loader2, MapPin, Cloud } from "lucide-react";
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

interface WeatherData {
  location: { name: string; latitude: number; longitude: number };
  current_weather: { temperature: number; conditions: string; humidity_percent: number };
  risk_assessment: any;
  forecast_3day: any[];
  species: string;
}

export function LocationWeatherChecker() {
  const [location, setLocation] = useState("");
  const [species, setSpecies] = useState("Tilapia");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);

  const handleCheck = async () => {
    if (!location.trim()) {
      setError("Please enter a location");
      return;
    }

    setLoading(true);
    setError("");
    setWeatherData(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/weather/location-check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          location: location.trim(),
          species: species,
          include_forecast: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch weather data");
      }

      const data = await response.json();
      setWeatherData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error fetching weather data");
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
            <MapPin className="w-5 h-5" />
            Location-Based Temperature Monitoring
          </CardTitle>
          <CardDescription>
            Check current temperature and risk level for your aquaculture location
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Location Input */}
            <div>
              <label className="text-sm font-medium">Location</label>
              <Input
                placeholder="Enter city name (e.g., 'Bangkok') or coordinates (e.g., '13.7563,100.5018')"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleCheck()}
                className="mt-1"
              />
              <p className="text-xs text-gray-500 mt-1">
                Try: "Bangkok", "Bangkok, Thailand", or "13.7563,100.5018"
              </p>
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
                  Checking Weather...
                </>
              ) : (
                <>
                  <Cloud className="w-4 h-4 mr-2" />
                  Check Temperature Risk
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

      {/* Current Weather & Risk Assessment */}
      {weatherData && (
        <>
          {/* Location & Current Weather Card */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Current Weather at {weatherData.location.name}</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <div className="text-sm text-gray-600">Temperature</div>
                <div className="text-3xl font-bold text-blue-600">
                  {weatherData.current_weather.temperature}°C
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {weatherData.current_weather.conditions}
                </div>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <div className="text-sm text-gray-600">Humidity</div>
                <div className="text-3xl font-bold text-gray-900">
                  {weatherData.current_weather.humidity_percent}%
                </div>
              </div>

              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <div className="text-sm text-gray-600">Location</div>
                <div className="text-sm font-mono text-gray-900 mt-1">
                  {weatherData.location.latitude.toFixed(2)}°N, {weatherData.location.longitude.toFixed(2)}°E
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Risk Assessment */}
          <TemperatureRiskCard {...weatherData.risk_assessment} />

          {/* 3-Day Forecast */}
          {weatherData.forecast_3day && weatherData.forecast_3day.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>3-Day Temperature Forecast</CardTitle>
                <CardDescription>Predicted temperatures and risk levels</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {weatherData.forecast_3day.map((day: any, idx: number) => (
                    <div
                      key={idx}
                      className={`p-4 rounded-lg border ${
                        day.risk_level === "high_risk"
                          ? "bg-red-50 border-red-200"
                          : day.risk_level === "caution"
                            ? "bg-yellow-50 border-yellow-200"
                            : "bg-green-50 border-green-200"
                      }`}
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="font-semibold">{new Date(day.date).toLocaleDateString()}</div>
                          <div className="text-sm text-gray-600 mt-1">{day.weather}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold">
                            {day.temp_mean}°C
                          </div>
                          <div className="text-xs text-gray-600">
                            {day.temp_min}° - {day.temp_max}°
                          </div>
                        </div>
                      </div>
                      <div className="flex justify-between mt-2 text-sm">
                        <span className="font-medium capitalize">{day.risk_level.replace("_", " ")}</span>
                        <span className="text-gray-600">Urgency: {day.urgency_score}/100</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* API Info */}
          <div className="text-xs text-gray-500 text-center p-3 bg-gray-50 rounded-lg">
            Weather data powered by Open-Meteo (free API) • Updated {new Date().toLocaleTimeString()}
          </div>
        </>
      )}
    </div>
  );
}

export default LocationWeatherChecker;
