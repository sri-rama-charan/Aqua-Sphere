# Temperature Monitoring Feature — Overview

This document consolidates all temperature monitoring documentation into a single, concise reference.

## 1) What this feature does
The temperature monitoring feature helps fish farmers prevent disease outbreaks by:
- Comparing water temperature to species-specific safe ranges.
- Classifying risk levels (Normal, Caution, High Risk).
- Explaining likely issues and recommended actions.
- Optionally using location-based weather data and a 3‑day forecast.

It is fully rule‑based (no ML), uses free APIs, and is easy to extend with new species or rules.

## 2) User flows
### A) Manual Temperature Check
1. User enters current water temperature.
2. Selects fish species.
3. System returns:
   - Risk level (color + label)
   - Safe range
   - Priority level (Low/Moderate/High)
   - Possible issues and actions

### B) Location‑Based Weather Check
1. User enters location (city or lat/long).
2. System resolves coordinates and fetches weather.
3. System returns:
   - Current temperature, weather summary
   - Risk assessment for current temperature
   - 3‑day forecast with daily risk levels (optional)

## 3) Risk logic (simplified)
- Each species has a safe temperature range.
- If current temp is within range → **Normal**.
- Slightly outside range → **Caution**.
- Far outside range → **High Risk**.

**Priority Level (Low/Moderate/High)** is derived from how far temperature is outside the safe range and drives urgency and actions.

## 4) Species support
Default species included:
- Tilapia, Catfish, Carp, Shrimp, Salmon, Trout, Milkfish, Bass, Pangasius, Eel

Add more by updating the species ranges in backend logic.

## 5) API endpoints (backend)
Base URL example: `http://localhost:8000`

### POST /temperature/assess-risk
**Body:**
```json
{ "temperature": 28, "species": "Tilapia", "location": "Manual Entry" }
```
**Returns:** risk level, safe range, issues, actions, disease risk factors.

### POST /weather/location-check
**Body:**
```json
{ "location": "Bangkok", "species": "Tilapia", "include_forecast": true }
```
**Returns:** resolved location, current weather, risk assessment, forecast (if requested).

### GET /temperature/species-list
Returns list of supported species and safe ranges.

### GET /weather/health
Health check for weather service readiness.

## 6) Frontend pages
- **Fish Health Detection**: disease prediction from image.
- **Temperature Monitor**: manual check + location-based check.

Navigation is via hamburger menu with page names:
- “🐟 Fish Health Detection”
- “🌡️ Temperature Monitor”

## 7) Configuration
### Frontend
Set API base URL using Vite env var:
```
VITE_API_URL=http://localhost:8000
```
If not set, it defaults to `http://localhost:8000`.

### Backend
Uses Open‑Meteo (free, no API key). No paid services required.

## 8) Files you may edit
### Backend
- `backend/temperature_monitoring.py`: risk logic and species ranges
- `backend/weather_service.py`: geocoding + weather fetch
- `backend/main.py`: API endpoints

### Frontend
- `frontend/src/components/ManualTemperatureChecker.tsx`
- `frontend/src/components/LocationWeatherChecker.tsx`
- `frontend/src/components/TemperatureRiskCard.tsx`
- `frontend/src/pages/TemperatureMonitor.tsx`

## 9) Extension ideas
- Add oxygen, pH, ammonia checks.
- Add push alerts for High Risk.
- Persist farm locations per user.
- Add localized languages for farmer messages.

---
If you want any extra details or examples added here, tell me what to include.