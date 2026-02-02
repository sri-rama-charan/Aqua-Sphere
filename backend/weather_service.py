"""
Weather Data Integration
Fetches weather data from free APIs and manages location-based queries.
Supports multiple free weather services for reliable fallback.
"""

import httpx
import logging
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import os

logger = logging.getLogger(__name__)

# Free weather APIs (no authentication required for basic usage)
WEATHER_API_PROVIDERS = {
    "open_meteo": {
        "url": "https://api.open-meteo.com/v1/forecast",
        "description": "Open-Meteo (no API key needed, 10,000 free requests/day)",
        "priority": 1
    },
    "wttr_in": {
        "url": "https://wttr.in",
        "description": "wttr.in (no API key needed, lightweight)",
        "priority": 2
    },
    "weather_gov": {
        "url": "https://api.weather.gov",
        "description": "NOAA Weather.gov (US only, no API key)",
        "priority": 3
    }
}


class LocationService:
    """Handles location querying and geocoding"""

    @staticmethod
    async def resolve_location(location_input: str) -> Optional[Tuple[float, float, str]]:
        """
        Resolve location name or coordinates to lat/lon.
        
        Args:
            location_input: Can be "city,country", "lat,lon", or just "city"
            
        Returns:
            Tuple of (latitude, longitude, location_name) or None if not found
        """
        try:
            # Check if input looks like coordinates
            if "," in location_input:
                parts = location_input.split(",")
                if len(parts) == 2:
                    try:
                        lat = float(parts[0].strip())
                        lon = float(parts[1].strip())
                        if -90 <= lat <= 90 and -180 <= lon <= 180:
                            return (lat, lon, f"Lat {lat:.2f}, Lon {lon:.2f}")
                    except ValueError:
                        pass
            
            # Use Open-Meteo's geocoding API (free, no key needed)
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={
                        "name": location_input,
                        "count": 1,
                        "language": "en",
                        "format": "json"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("results"):
                        result = data["results"][0]
                        lat = result.get("latitude")
                        lon = result.get("longitude")
                        name = result.get("name", location_input)
                        country = result.get("country", "")
                        display_name = f"{name}, {country}" if country else name
                        return (lat, lon, display_name)
        except Exception as e:
            logger.error(f"Error resolving location '{location_input}': {e}")
        
        return None

    @staticmethod
    def format_location(lat: float, lon: float) -> str:
        """Format coordinates for display"""
        return f"Lat {lat:.2f}°, Lon {lon:.2f}°"


class WeatherService:
    """Fetches weather data from free APIs"""

    @staticmethod
    async def get_current_weather(
        latitude: float,
        longitude: float,
        location_name: str = "Unknown"
    ) -> Optional[Dict]:
        """
        Fetch current weather using Open-Meteo (most reliable free option).
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            location_name: Display name of location
            
        Returns:
            Dict with current weather data or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    WEATHER_API_PROVIDERS["open_meteo"]["url"],
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
                        "timezone": "auto",
                        "temperature_unit": "celsius"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    current = data.get("current", {})
                    
                    return {
                        "location": location_name,
                        "latitude": latitude,
                        "longitude": longitude,
                        "temperature": current.get("temperature_2m"),
                        "weather_code": current.get("weather_code"),
                        "weather_description": WeatherService.decode_weather_code(
                            current.get("weather_code", 0)
                        ),
                        "humidity": current.get("relative_humidity_2m"),
                        "wind_speed": current.get("wind_speed_10m"),
                        "timestamp": current.get("time"),
                        "timezone": data.get("timezone")
                    }
        except Exception as e:
            logger.error(f"Error fetching weather for ({latitude}, {longitude}): {e}")
        
        return None

    @staticmethod
    async def get_forecast(
        latitude: float,
        longitude: float,
        days: int = 3
    ) -> Optional[List[Dict]]:
        """
        Fetch 3-day temperature forecast.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            days: Number of days to forecast (1-16)
            
        Returns:
            List of daily forecasts or None if failed
        """
        try:
            days = min(max(days, 1), 16)  # Clamp to valid range
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    WEATHER_API_PROVIDERS["open_meteo"]["url"],
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,weather_code,precipitation_sum",
                        "timezone": "auto",
                        "forecast_days": days,
                        "temperature_unit": "celsius"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    daily = data.get("daily", {})
                    
                    forecast = []
                    for i in range(len(daily.get("time", []))):
                        forecast.append({
                            "date": daily["time"][i],
                            "temp_min": daily["temperature_2m_min"][i],
                            "temp_max": daily["temperature_2m_max"][i],
                            "temp_mean": daily["temperature_2m_mean"][i],
                            "weather_code": daily["weather_code"][i],
                            "weather_description": WeatherService.decode_weather_code(
                                daily["weather_code"][i]
                            ),
                            "precipitation": daily["precipitation_sum"][i]
                        })
                    
                    return forecast
        except Exception as e:
            logger.error(f"Error fetching forecast for ({latitude}, {longitude}): {e}")
        
        return None

    @staticmethod
    def decode_weather_code(code: int) -> str:
        """
        Decode WMO weather code to human-readable description.
        Based on WMO Weather interpretation codes.
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Heavy drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }
        return weather_codes.get(code, "Unknown weather")

    @staticmethod
    async def get_historical_max_min(
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, float]]:
        """
        Get typical max/min temperatures for the location (long-term average).
        Useful for context about extreme temperatures.
        Note: This is simplified - in production, use historical weather databases.
        
        Returns:
            Dict with typical_max, typical_min
        """
        try:
            # For production, integrate with climate databases like NOAA or Copernicus
            # This is a simplified placeholder
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    WEATHER_API_PROVIDERS["open_meteo"]["url"],
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "daily": "temperature_2m_max,temperature_2m_min",
                        "start_date": "2024-01-01",
                        "end_date": "2024-12-31",
                        "timezone": "auto",
                        "temperature_unit": "celsius"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    daily = data.get("daily", {})
                    
                    if daily.get("temperature_2m_max"):
                        max_temps = [t for t in daily["temperature_2m_max"] if t is not None]
                        min_temps = [t for t in daily["temperature_2m_min"] if t is not None]
                        
                        return {
                            "typical_max": max(max_temps) if max_temps else None,
                            "typical_min": min(min_temps) if min_temps else None,
                            "avg_max": sum(max_temps) / len(max_temps) if max_temps else None,
                            "avg_min": sum(min_temps) / len(min_temps) if min_temps else None
                        }
        except Exception as e:
            logger.error(f"Error fetching historical data for ({latitude}, {longitude}): {e}")
        
        return None


# Health check function
async def verify_api_health() -> Dict[str, bool]:
    """Verify weather API availability"""
    health = {}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                WEATHER_API_PROVIDERS["open_meteo"]["url"],
                params={"latitude": 0, "longitude": 0, "current": "temperature_2m"}
            )
            health["open_meteo"] = response.status_code == 200
    except Exception as e:
        logger.error(f"Weather API health check failed: {e}")
        health["open_meteo"] = False
    
    return health
