"""
Location-Based Temperature Risk Monitoring System
Monitors water temperature and provides risk assessment for fish farmers.
Supports species-specific safe temperature ranges and provides actionable recommendations.
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RiskLevel(str, Enum):
    """Risk classification levels"""
    NORMAL = "normal"
    CAUTION = "caution"
    HIGH_RISK = "high_risk"


@dataclass
class TemperatureReading:
    """Single temperature measurement"""
    current: float  # Celsius
    timestamp: str
    location: str


@dataclass
class RiskAssessment:
    """Temperature risk assessment result"""
    risk_level: RiskLevel
    current_temperature: float
    safe_range: Tuple[float, float]
    possible_issues: List[str]
    recommended_actions: List[str]
    urgency_score: float  # 0-100, higher = more urgent
    species: str


# Species-specific safe temperature ranges (in Celsius)
SPECIES_TEMPERATURE_RANGES = {
    "Tilapia": {"min": 25, "max": 32, "optimal": 28},
    "Catfish": {"min": 18, "max": 32, "optimal": 26},
    "Carp": {"min": 16, "max": 28, "optimal": 22},
    "Shrimp": {"min": 20, "max": 32, "optimal": 28},
    "Salmon": {"min": 8, "max": 16, "optimal": 12},
    "Trout": {"min": 10, "max": 18, "optimal": 14},
    "Milkfish": {"min": 25, "max": 32, "optimal": 28},
    "Bass": {"min": 15, "max": 28, "optimal": 22},
    "Pangasius": {"min": 25, "max": 32, "optimal": 28},
    "Eel": {"min": 22, "max": 28, "optimal": 25},
}

# Default ranges if species not specified
DEFAULT_TEMP_RANGE = {"min": 20, "max": 28, "optimal": 24}

# Temperature change rate risk thresholds (°C per hour)
RAPID_CHANGE_THRESHOLD = 2.0

# Historical data for comparing trends (simplified - in production use database)
TEMPERATURE_HISTORY = {}


class TemperatureRiskAssessor:
    """Evaluates temperature-based risks for aquaculture"""

    @staticmethod
    def get_safe_range(species: str = "Generic") -> Dict[str, float]:
        """Get safe temperature range for given species"""
        return SPECIES_TEMPERATURE_RANGES.get(species, DEFAULT_TEMP_RANGE)

    @staticmethod
    def classify_risk(
        current_temp: float,
        species: str = "Generic",
        previous_temp: Optional[float] = None,
        location: str = "Unknown"
    ) -> RiskAssessment:
        """
        Classify temperature risk based on current temperature and species.
        
        Args:
            current_temp: Current water temperature in Celsius
            species: Fish/shrimp species being farmed
            previous_temp: Previous temperature reading for trend analysis
            location: Location identifier for context
            
        Returns:
            RiskAssessment with risk level, possible issues, and recommendations
        """
        safe_range = TemperatureRiskAssessor.get_safe_range(species)
        min_safe, max_safe = safe_range["min"], safe_range["max"]
        optimal = safe_range["optimal"]
        
        possible_issues = []
        recommended_actions = []
        risk_level = RiskLevel.NORMAL
        urgency_score = 0
        
        # Check if temperature is within safe range
        if min_safe <= current_temp <= max_safe:
            # Within safe range - check if close to boundaries
            margin_low = current_temp - min_safe
            margin_high = max_safe - current_temp
            
            if margin_low < 2 or margin_high < 2:
                # Close to boundary
                risk_level = RiskLevel.CAUTION
                urgency_score = 30
                
                if margin_low < 2:
                    possible_issues.append("Temperature approaching minimum safe threshold")
                    possible_issues.append("Reduced metabolic activity and feeding")
                    recommended_actions.append("Monitor temperature closely")
                    recommended_actions.append("Ensure adequate aeration")
                    recommended_actions.append("Check heater functionality")
                else:
                    possible_issues.append("Temperature approaching maximum safe threshold")
                    possible_issues.append("Reduced oxygen availability")
                    possible_issues.append("Increased bacterial disease risk")
                    recommended_actions.append("Increase water aeration immediately")
                    recommended_actions.append("Check pond shade (e.g., netting or water hyacinth)")
                    recommended_actions.append("Monitor for disease signs")
            else:
                # Comfortably within range
                risk_level = RiskLevel.NORMAL
                urgency_score = 0
                possible_issues.append("No temperature-related action needed")
                recommended_actions.append("Continue normal monitoring")
                recommended_actions.append("Feed according to schedule")
        
        # Below minimum safe temperature
        elif current_temp < min_safe:
            below_by = min_safe - current_temp
            
            if below_by > 5:
                # Severely cold
                risk_level = RiskLevel.HIGH_RISK
                urgency_score = 95
                possible_issues = [
                    "CRITICAL: Water temperature far below safe range",
                    "Severe reduction in metabolism and immunity",
                    "Increased disease susceptibility",
                    "Poor feed conversion",
                    "Risk of cold-water shock mortality",
                    "Bacterial growth slowdown but parasites may thrive"
                ]
                recommended_actions = [
                    "IMMEDIATE: Activate backup heaters or heat source",
                    "Check heating system immediately",
                    "Reduce feeding to minimum",
                    "Increase aeration for oxygenation",
                    "Monitor fish closely for lethargy or disease signs",
                    "Consider emergency measures (shelter, insulation)",
                    "Prepare isolation tank with warmer water",
                    "Test water quality (oxygen, ammonia) frequently"
                ]
            else:
                # Moderately cold
                risk_level = RiskLevel.CAUTION
                urgency_score = 60
                possible_issues = [
                    "Water temperature below optimal range",
                    "Reduced feeding and growth rates",
                    "Slower immune response to pathogens",
                    "Increased susceptibility to bacterial diseases"
                ]
                recommended_actions = [
                    "Activate heating system if available",
                    "Reduce feeding by 50%",
                    "Increase water aeration",
                    "Monitor for disease signs daily",
                    "Maintain excellent water quality",
                    "Adjust feeding schedule to warmer times of day"
                ]
        
        # Above maximum safe temperature
        else:  # current_temp > max_safe
            above_by = current_temp - max_safe
            
            if above_by > 5:
                # Severely hot
                risk_level = RiskLevel.HIGH_RISK
                urgency_score = 98
                possible_issues = [
                    "CRITICAL: Water temperature far exceeds safe range",
                    "Severe oxygen depletion in water",
                    "Extreme metabolic stress on fish",
                    "Critical disease outbreak risk (bacterial and parasitic)",
                    "Zooplankton die-off reducing natural food",
                    "Potential thermal shock mortality",
                    "Ammonia and nitrite toxicity increases significantly"
                ]
                recommended_actions = [
                    "IMMEDIATE: Emergency cooling measures required",
                    "Increase aeration to MAXIMUM capacity",
                    "Add fresh, cooler water if available (avoid thermal shock)",
                    "Install shade structures (netting, water hyacinth, tarps)",
                    "Consider emergency partial water change with cooler source",
                    "Stop feeding immediately",
                    "Monitor oxygen levels continuously",
                    "Prepare quarantine tank for emergency treatment",
                    "Test water quality (especially dissolved oxygen and ammonia)",
                    "Contact veterinary expert immediately",
                    "Document all deaths for insurance/records"
                ]
            else:
                # Moderately hot
                risk_level = RiskLevel.CAUTION
                urgency_score = 70
                possible_issues = [
                    "Water temperature above optimal range",
                    "Reduced dissolved oxygen availability",
                    "Increased stress on fish",
                    "Elevated bacterial disease risk",
                    "Potential parasitic infections (Ichthyophthirius, Trichodina)",
                    "Increased ammonia/nitrite toxicity"
                ]
                recommended_actions = [
                    "Increase aeration immediately",
                    "Add shade to pond (aquatic plants, netting, partial tarp)",
                    "Perform 25-30% water change with cooler source if possible",
                    "Reduce feeding to 75% of normal",
                    "Monitor disease signs closely (gasping, fin clamping)",
                    "Test water quality daily (oxygen, ammonia, nitrite)",
                    "Consider emergency cooling (ice addition - use with caution)",
                    "Arrange for shade installation",
                    "Monitor forecast for temperature trends"
                ]
        
        # Check for rapid temperature changes
        if previous_temp is not None:
            temp_change = abs(current_temp - previous_temp)
            if temp_change > RAPID_CHANGE_THRESHOLD:
                # Rapid change is stressful
                possible_issues.insert(0, f"Rapid temperature change detected ({temp_change:.1f}°C)")
                recommended_actions.insert(0, "Monitor for shock-induced stress signs")
                # Increase urgency slightly
                urgency_score = min(100, urgency_score + 15)
        
        return RiskAssessment(
            risk_level=risk_level,
            current_temperature=current_temp,
            safe_range=(min_safe, max_safe),
            possible_issues=possible_issues,
            recommended_actions=recommended_actions,
            urgency_score=urgency_score,
            species=species
        )

    @staticmethod
    def get_disease_risk_factors(risk_level: RiskLevel, species: str) -> Dict[str, str]:
        """
        Map temperature risk level to disease outbreak probability.
        Returns disease-specific risks.
        """
        risk_mapping = {
            RiskLevel.NORMAL: {
                "bacterial_disease": "Low (optimal conditions)",
                "parasitic_disease": "Low",
                "viral_disease": "Low",
                "fungal_disease": "Low"
            },
            RiskLevel.CAUTION: {
                "bacterial_disease": "Moderate (stress weakens immunity)",
                "parasitic_disease": "Moderate to High (if too warm)",
                "viral_disease": "Moderate (stress increases vulnerability)",
                "fungal_disease": "Moderate (if too cold and damp)"
            },
            RiskLevel.HIGH_RISK: {
                "bacterial_disease": "CRITICAL (severe immune suppression)",
                "parasitic_disease": "CRITICAL (rapid reproduction in warm water)",
                "viral_disease": "CRITICAL (high stress = infection spreads rapidly)",
                "fungal_disease": "HIGH (if temperature too cold)"
            }
        }
        return risk_mapping.get(risk_level, risk_mapping[RiskLevel.NORMAL])

    @staticmethod
    def get_color_code(risk_level: RiskLevel) -> str:
        """Get color code for UI display"""
        colors = {
            RiskLevel.NORMAL: "#10b981",      # Green
            RiskLevel.CAUTION: "#f59e0b",     # Amber/Orange
            RiskLevel.HIGH_RISK: "#ef4444"    # Red
        }
        return colors.get(risk_level, "#6b7280")

    @staticmethod
    def get_risk_label(risk_level: RiskLevel) -> str:
        """Get human-readable risk label"""
        labels = {
            RiskLevel.NORMAL: "No Action Needed",
            RiskLevel.CAUTION: "Monitor Closely",
            RiskLevel.HIGH_RISK: "Immediate Action Required"
        }
        return labels.get(risk_level, "Unknown")


def create_assessment_response(assessment: RiskAssessment) -> Dict:
    """Convert RiskAssessment to JSON-serializable dict"""
    return {
        "risk_level": assessment.risk_level.value,
        "risk_label": TemperatureRiskAssessor.get_risk_label(assessment.risk_level),
        "color_code": TemperatureRiskAssessor.get_color_code(assessment.risk_level),
        "current_temperature": assessment.current_temperature,
        "safe_range": {
            "min": assessment.safe_range[0],
            "max": assessment.safe_range[1]
        },
        "urgency_score": assessment.urgency_score,
        "possible_issues": assessment.possible_issues,
        "recommended_actions": assessment.recommended_actions,
        "species": assessment.species,
        "disease_risks": TemperatureRiskAssessor.get_disease_risk_factors(
            assessment.risk_level, assessment.species
        )
    }
