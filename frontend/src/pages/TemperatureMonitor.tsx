import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import LocationWeatherChecker from "@/components/LocationWeatherChecker";
import ManualTemperatureChecker from "@/components/ManualTemperatureChecker";

const TemperatureMonitor = () => {
  const [activeTab, setActiveTab] = useState("manual");

  return (
    <div className="space-y-6 px-4 mt-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🌡️ Temperature Monitor</h2>
        <p className="text-sm text-muted-foreground">
          Monitor water temperature and get risk assessments for your fish species
        </p>
      </div>

      {/* Tabs for different checking methods */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="manual">Manual Check</TabsTrigger>
          <TabsTrigger value="location">Location Based</TabsTrigger>
        </TabsList>

        <TabsContent value="manual" className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Manual Temperature Check</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Enter your current water temperature and select your fish species to get a risk assessment
            </p>
          </div>
          <ManualTemperatureChecker />
        </TabsContent>

        <TabsContent value="location" className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Location-Based Weather Check</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Enter your pond location to get weather data and temperature forecasts with risk assessments
            </p>
          </div>
          <LocationWeatherChecker />
        </TabsContent>
      </Tabs>

      {/* Info Section */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">💡 How it works</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• <strong>Manual Check:</strong> Quickly assess risk with your current temperature</li>
          <li>• <strong>Location Based:</strong> Get real-time weather and 3-day forecast for your area</li>
          <li>• <strong>Risk Levels:</strong> Green (Normal) → Orange (Caution) → Red (High Risk)</li>
          <li>• <strong>Species Support:</strong> Tilapia, Catfish, Carp, Trout, and more</li>
        </ul>
      </div>

      <footer className="mt-8 text-center px-4">
        <p className="text-xs text-muted-foreground">
          Data helps prevent temperature-related fish diseases like fin rot, ich, and bacterial infections
        </p>
      </footer>
    </div>
  );
};

export default TemperatureMonitor;
