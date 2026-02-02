from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import pipeline
from PIL import Image
import io
import logging
import traceback
from disease_knowledge import get_disease_info
from temperature_monitoring import TemperatureRiskAssessor, create_assessment_response
from weather_service import WeatherService, LocationService
from typing import Optional, List
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fish Disease Classifier API")

# CORS Configuration - Allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aqua-health-pro.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for model
classifier = None

@app.on_event("startup")
async def load_model():
    """Load model on startup with aggressive memory optimization"""
    global classifier
    try:
        logger.info("Loading model with memory optimization...")
        import torch
        import os
        
        # Read Hugging Face token (optional)
        hf_token = os.getenv('HF_TOKEN')
        if not hf_token:
            logger.warning("No HF_TOKEN found in environment variables, proceeding without authentication")
        
        # Set environment variables for memory optimization
        os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
        os.environ['HF_HOME'] = '/tmp/hf_home'
        
        # Disable gradients globally to save memory
        torch.set_grad_enabled(False)
        
        # Use CPU-only lightweight model loading
        classifier = pipeline(
            "image-classification",
            model="Saon110/fish-shrimp-disease-classifier",
            token=hf_token,
            device=-1,  # Force CPU
            torch_dtype=torch.float32,  # Use float32 for CPU
            trust_remote_code=True
        )
        
        # Free up any unused memory
        import gc
        gc.collect()
        
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.error(traceback.format_exc())

@app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "online",
            "message": "Fish Disease Classifier API is running",
            "model_loaded": classifier is not None
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return JSONResponse(
        content={
            "status": "healthy" if classifier else "model_not_loaded",
            "model_loaded": classifier is not None
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.post("/predict")
async def predict_image(file: UploadFile = File(...), language: Optional[str] = Form("en")):
    """
    Predict fish disease from uploaded image
    
    Args:
        file: Image file
        language: Language code (en=English, te=Telugu). Default: en
    """
    try:
        # Validate language
        if language not in ["en", "te"]:
            language = "en"
        
        logger.info(f"Processing image: {file.filename}, language: {language}")
        
        # Check if model is loaded
        if classifier is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded yet. Please wait and try again."
            )
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        logger.info(f"Processing image: {file.filename}")
        
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Run the model
        logger.info("Running prediction...")
        preds = classifier(image)
        logger.info(f"Predictions: {preds}")
        
        # Prepare results
        fish_preds = [
            pred for pred in preds
            if pred["label"].startswith("Fish_")
        ]
        
        if not fish_preds:
            # If no fish predictions, return top prediction anyway
            top_prediction = preds[0] if preds else None
            if not top_prediction:
                raise HTTPException(
                    status_code=500,
                    detail="No predictions returned from model"
                )
            
            # Get enriched disease information even for non-fish predictions
            disease_info = get_disease_info(top_prediction["label"], float(top_prediction["score"]), language)
            
            return JSONResponse(
                content=disease_info,
                headers={
                    "Access-Control-Allow-Origin": "*",
                }
            )
        
        top_fish = fish_preds[0]
        
        # Log the prediction details
        logger.info(f"Top prediction - Label: {top_fish['label']}, Score: {top_fish['score']}, Language: {language}")
        
        # Get enriched disease information with language support
        disease_info = get_disease_info(top_fish["label"], float(top_fish["score"]), language)
        
        # Log the returned disease info
        logger.info(f"Disease info returned: {disease_info}")
        
        return JSONResponse(
            content=disease_info,
            headers={
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


# ============================================================================
# TEMPERATURE MONITORING ENDPOINTS
# ============================================================================

# Pydantic Models for request/response validation
class TemperatureCheckRequest(BaseModel):
    """Request model for temperature risk assessment"""
    temperature: float
    species: Optional[str] = "Generic"
    previous_temperature: Optional[float] = None
    location: Optional[str] = "Unknown"


class LocationWeatherRequest(BaseModel):
    """Request model for location-based weather check"""
    location: str  # Can be "city name", "city, country", or "lat,lon"
    species: Optional[str] = "Generic"
    include_forecast: Optional[bool] = True


@app.post("/temperature/assess-risk")
async def assess_temperature_risk(request: TemperatureCheckRequest):
    """
    Assess temperature-based risk for fish/shrimp farming.
    
    Args:
        temperature: Current water temperature in Celsius
        species: Type of fish/shrimp (Tilapia, Catfish, Carp, Shrimp, etc.)
        previous_temperature: Previous reading for trend analysis
        location: Location identifier
        
    Returns:
        Risk assessment with issues, actions, and disease risks
    """
    try:
        # Validate temperature input
        if not -50 <= request.temperature <= 60:
            raise HTTPException(
                status_code=400,
                detail="Temperature must be between -50°C and 60°C"
            )
        
        logger.info(f"Assessing temperature: {request.temperature}°C, species: {request.species}")
        
        # Get risk assessment
        assessment = TemperatureRiskAssessor.classify_risk(
            current_temp=request.temperature,
            species=request.species,
            previous_temp=request.previous_temperature,
            location=request.location
        )
        
        response = create_assessment_response(assessment)
        
        return JSONResponse(
            content=response,
            headers={"Access-Control-Allow-Origin": "*"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assessing temperature risk: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error assessing risk: {str(e)}"
        )


@app.post("/weather/location-check")
async def check_location_weather(request: LocationWeatherRequest):
    """
    Get current temperature and risk assessment for a location.
    
    Args:
        location: City name, "city,country", or "latitude,longitude"
        species: Fish/shrimp species for safe range comparison
        include_forecast: Whether to include 3-day forecast
        
    Returns:
        Current weather, temperature risk level, and 3-day forecast
    """
    try:
        logger.info(f"Checking weather for location: {request.location}")
        
        # Resolve location to coordinates
        location_data = await LocationService.resolve_location(request.location)
        if not location_data:
            raise HTTPException(
                status_code=404,
                detail=f"Location '{request.location}' not found. Try: 'city name' or 'lat,lon'"
            )
        
        lat, lon, location_name = location_data
        logger.info(f"Resolved to: {location_name} ({lat}, {lon})")
        
        # Get current weather
        weather = await WeatherService.get_current_weather(lat, lon, location_name)
        if not weather:
            raise HTTPException(
                status_code=502,
                detail="Failed to fetch weather data. Please try again later."
            )
        
        current_temp = weather.get("temperature")
        
        # Assess temperature risk
        assessment = TemperatureRiskAssessor.classify_risk(
            current_temp=current_temp,
            species=request.species,
            location=location_name
        )
        
        risk_response = create_assessment_response(assessment)
        
        # Get forecast if requested
        forecast_data = None
        if request.include_forecast:
            forecast = await WeatherService.get_forecast(lat, lon, days=3)
            if forecast:
                forecast_data = []
                for day in forecast:
                    # Assess risk for forecast temps
                    day_risk = TemperatureRiskAssessor.classify_risk(
                        current_temp=day.get("temp_mean", 0),
                        species=request.species,
                        location=location_name
                    )
                    forecast_data.append({
                        "date": day.get("date"),
                        "temp_min": day.get("temp_min"),
                        "temp_max": day.get("temp_max"),
                        "temp_mean": day.get("temp_mean"),
                        "weather": day.get("weather_description"),
                        "precipitation_mm": day.get("precipitation"),
                        "risk_level": day_risk.risk_level.value,
                        "urgency_score": day_risk.urgency_score
                    })
        
        return JSONResponse(
            content={
                "location": {
                    "name": location_name,
                    "latitude": lat,
                    "longitude": lon,
                    "timezone": weather.get("timezone", "Unknown")
                },
                "current_weather": {
                    "temperature": current_temp,
                    "conditions": weather.get("weather_description"),
                    "humidity_percent": weather.get("humidity"),
                    "wind_speed_kmh": weather.get("wind_speed"),
                    "timestamp": weather.get("timestamp")
                },
                "risk_assessment": risk_response,
                "forecast_3day": forecast_data,
                "species": request.species,
                "api_used": "Open-Meteo (free, no API key)"
            },
            headers={"Access-Control-Allow-Origin": "*"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking location weather: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error checking weather: {str(e)}"
        )


@app.get("/temperature/species-list")
async def get_species_list():
    """Get list of supported species and their safe temperature ranges"""
    from temperature_monitoring import SPECIES_TEMPERATURE_RANGES
    
    species_info = {}
    for species, temps in SPECIES_TEMPERATURE_RANGES.items():
        species_info[species] = {
            "safe_range_celsius": [temps["min"], temps["max"]],
            "optimal_celsius": temps["optimal"],
            "range_description": f"{temps['min']}°C - {temps['max']}C (optimal: {temps['optimal']}°C)"
        }
    
    return JSONResponse(
        content={
            "supported_species": species_info,
            "note": "Use species name exactly as shown. If species not found, 'Generic' range will be used."
        },
        headers={"Access-Control-Allow-Origin": "*"}
    )


@app.get("/weather/health")
async def weather_service_health():
    """Check if weather API is available"""
    from weather_service import verify_api_health
    
    health = await verify_api_health()
    
    status = "healthy" if all(health.values()) else "degraded"
    
    return JSONResponse(
        content={
            "status": status,
            "services": health,
            "open_meteo": "Open-Meteo (primary service)"
        },
        headers={"Access-Control-Allow-Origin": "*"}
    )
