"""
Fish & Shrimp Disease Knowledge Base
Contains detailed information about aquaculture diseases including causes, severity, and treatments.
Severity levels are determined by image analysis and disease progression indicators.
Optimized for mobile display with concise, actionable guidance.
"""

DISEASE_KNOWLEDGE = {
    "Fish_Bacterial Red disease": {
        "display_name": "Bacterial Red Disease (Hemorrhagic Septicemia)",
        "cause": "Caused by bacteria like Aeromonas or Pseudomonas. Results from poor water conditions, injuries, stress, or secondary infections. Can spread rapidly in crowded conditions.",
        "treatments": {
            "Low": "Early stage treatment: TEST WATER IMMEDIATELY - measure ammonia, nitrite, nitrate, pH, dissolved oxygen (DO), and temperature. Perform 25% water change. Target levels: ammonia 0 ppm, nitrite 0 ppm, nitrate <20 ppm, pH 6.5-8.5, DO >5 mg/L. Add aquarium salt (1 tablespoon per 5 gallons). Monitor closely for 48 hours. Reduce feeding by half. Increase aeration. RETEST water daily for 3 days, especially at sunrise when DO is lowest.",
            "Medium": "Active infection: TEST WATER TWICE DAILY (at sunrise and midday) for ammonia, nitrite, nitrate, pH, DO, temperature. Isolate affected fish if possible. Perform 30-40% water changes daily for 3 days. After each water change, retest within 2 hours. Use antibiotics (oxytetracycline 50-100 mg/L) in feed or water bath. Add salt (1-2 tablespoons per gallon). Maintain DO >5 mg/L, ammonia 0 ppm, nitrite 0 ppm. Monitor all fish daily. Continue daily water testing for 7-10 days.",
            "High": "URGENT - Advanced infection: IMMEDIATE comprehensive water testing required. Test ammonia, nitrite, nitrate, pH, DO, temperature EVERY 6 HOURS for first 48 hours. Immediate isolation required. Perform 50% water change. Retest after 1 hour. Start aggressive antibiotic treatment (oxytetracycline or sulfa drugs - consult dosage guidelines). Salt bath treatment (2-3% for 10-15 minutes). Maintain pristine conditions: ammonia 0 ppm, nitrite 0 ppm, DO >6 mg/L, pH 7.0-8.0, temperature stable. Consider euthanasia if fish is severely suffering. Disinfect equipment. Consult fish veterinarian immediately. Continue testing 3 times daily until recovery begins."
        }
    },
    "Fish_Bacterial diseases - Aeromoniasis": {
        "display_name": "Bacterial Diseases - Aeromoniasis",
        "cause": "Caused by Aeromonas bacteria (A. hydrophila, A. sobria). Occurs due to poor water quality, stress, overcrowding, injury, or weakened immune system. Common in warm water conditions.",
        "treatments": {
            "Low": "Mild symptoms: TEST water quality immediately (ammonia, nitrite, nitrate, pH, DO, temperature). Improve water quality with 20-25% water change. Target: ammonia 0 ppm, nitrite 0 ppm, pH 6.5-8.5, DO >4 mg/L. Ensure proper filtration. Add aquarium salt (1 tablespoon per 5 gallons). Boost immune system with vitamin-enriched feed. Monitor water temperature (keep stable 75-80°F). RETEST water every 2-3 days. Observe for 3-5 days.",
            "Medium": "Moderate infection: TEST water DAILY at sunrise for 1 week. Isolate infected fish. Perform 30% water changes every other day, retest 2 hours after each change. Use antibiotics (oxytetracycline or erythromycin) in feed at 50 mg/kg fish weight. Salt treatment (1-3 tablespoons per 5 gallons). Increase aeration - maintain DO >5 mg/L. Keep ammonia 0 ppm, nitrite 0 ppm. Reduce stocking density if possible. Continue testing until recovery.",
            "High": "Severe infection: Emergency testing protocol - test water EVERY 4-6 HOURS initially. Complete isolation. Perform 40-50% water change immediately. Retest within 1 hour. Aggressive antibiotic therapy (injectable antibiotics may be needed - consult vet). Medicated baths (furan compounds). Maintain pristine water conditions: ammonia 0 ppm, nitrite 0 ppm, nitrate <10 ppm, DO >6 mg/L, pH 7.0-8.0, stable temperature. Test twice daily (sunrise and midday) until stable. Professional veterinary consultation strongly recommended."
        }
    },
    "Fish_Bacterial gill disease": {
        "display_name": "Bacterial Gill Disease",
        "cause": "Caused by Flavobacterium branchiophilum bacteria. Triggered by poor water quality, high ammonia/nitrite levels, overcrowding, stress, and inadequate oxygen. Affects respiratory function.",
        "treatments": {
            "Low": "Early detection: IMMEDIATELY test water chemistry - CRITICAL for gill disease. Test ammonia, nitrite, nitrate, pH, and DO. Ammonia and nitrite MUST be 0 ppm - any detection is dangerous. DO must be >5 mg/L. Perform 25% water change. Retest after 30 minutes. Increase aeration significantly. Reduce feeding. Add salt bath (1 tablespoon per 5 gallons). Improve filtration capacity. Monitor breathing patterns closely. TEST water 3 TIMES DAILY (sunrise, midday, evening) for 5 days - gill disease is oxygen-critical.",
            "Medium": "Respiratory distress visible: URGENT testing protocol - test ammonia, nitrite, DO EVERY 3 HOURS for first 24 hours. Critical water quality intervention - reduce ammonia/nitrite to 0 ppm urgently. Perform 35-40% water change. Retest immediately after. Maintain DO >6 mg/L at all times. Use chloramine-T (10 mg/L for 30-60 minutes) or potassium permanganate bath (2 mg/L for 10-15 minutes). Reduce stocking density immediately. Maximum aeration. Continue testing 4 times daily (every 6 hours) until breathing normalizes.",
            "High": "LIFE-THREATENING - Severe gill damage: EMERGENCY - test water EVERY 2 HOURS for first 48 hours. Ammonia/nitrite/DO are life-or-death parameters. Immediately improve oxygen (add air stones, reduce temperature slightly to increase DO saturation). Perform 50% water change with aged, well-oxygenated water (pre-aerate for 30 min). Retest immediately. Maintain DO >7 mg/L, ammonia 0 ppm, nitrite 0 ppm, pH 7.0-7.5. Professional-grade treatments (chloramine-T or potassium permanganate - follow exact dosing). Consider moving to hospital tank with pristine water. Veterinary consultation critical - may need injectable antibiotics. Continue intensive testing (every 4 hours) until stable, then reduce to 3 times daily."
        }
    },
    "Fish_Fungal diseases Saprolegniasis": {
        "display_name": "Fungal Diseases - Saprolegniasis",
        "cause": "Caused by Saprolegnia fungus creating cotton-like growth on skin, fins, or gills. Secondary infection following injuries, stress, poor water quality, or other diseases. Thrives in cool, dirty water.",
        "treatments": {
            "Low": "Minor fungal patches: TEST water quality (pH, temperature, ammonia, nitrite, DO). Improve water quality with 25% water change. Target: pH 7.0-8.0, ammonia 0 ppm, nitrite 0 ppm, DO >5 mg/L. Increase water temperature gradually to 78-80°F (if species tolerates) - retest after temperature change. Add aquarium salt (1 tablespoon per 3 gallons). Use methylene blue dip (2-3 mg/L for 10 minutes). Ensure no sharp objects causing injuries. Monitor daily. RETEST water every 2-3 days during treatment.",
            "Medium": "Spreading fungal growth: TEST water DAILY (pH, temperature, ammonia, nitrite, DO, nitrate). Isolate affected fish. Perform 30% water changes every 2 days, retest 1-2 hours after each change. Salt bath treatment (2-3 tablespoons per gallon for 15 minutes daily). Use antifungal medications (malachite green 0.1 mg/L or potassium permanganate 2 mg/L). Remove dead tissue gently if accessible. Maintain stable temperature 78-80°F. Keep ammonia 0 ppm, nitrite 0 ppm, pH 7.0-8.0, DO >5 mg/L. Test twice daily (morning and evening) for first week.",
            "High": "Extensive fungal coverage: URGENT - TEST water EVERY 6 HOURS initially. Fungus spreading to vital areas. Complete isolation in hospital tank with pristine water (pre-test hospital tank water before transfer). Daily salt baths (3% solution for 10-15 minutes). Aggressive antifungal treatment (malachite green + formalin combination following product instructions). Maintain optimal conditions: temperature 78-80°F (stable), ammonia 0 ppm, nitrite 0 ppm, DO >6 mg/L, pH 7.0-7.5. May need to manually remove large fungal masses (under expert guidance). Consult aquatic veterinarian for advanced treatment options. Continue testing 3 times daily until improvement seen."
        }
    },
    "Fish_Healthy Fish": {
        "display_name": "Healthy Fish",
        "cause": "No disease detected - fish appears healthy with normal coloring, behavior, and no visible symptoms.",
        "treatments": {
            "Low": "Continue excellent aquaculture practices: Maintain optimal water quality (pH 6.5-8.5, ammonia 0 ppm, nitrite 0 ppm, nitrate <20 ppm). Provide balanced, high-quality nutrition. Avoid overcrowding (follow species-specific stocking guidelines). Perform regular 15-20% weekly water changes. Quarantine new fish for 2-4 weeks before introduction. Monitor daily for any changes in behavior or appearance.",
            "Medium": "Maintain preventive care routines (same as Low severity)",
            "High": "Maintain preventive care routines (same as Low severity)"
        }
    },
    "Fish_Parasitic diseases": {
        "display_name": "Parasitic Diseases",
        "cause": "Caused by external/internal parasites including Ichthyophthirius (ich/white spot), flukes (Gyrodactylus, Dactylogyrus), anchor worms (Lernaea), fish lice (Argulus). Spread through contaminated water, equipment, or introducing infected fish.",
        "treatments": {
            "Low": "Few parasites detected: TEST water (temperature, pH, ammonia, nitrite, DO). Parasites thrive in poor conditions. Identify parasite type by appearance. For ich: gradually raise temperature to 82°F (test every 2 hours during temperature change), add aquarium salt (1 tablespoon per 5 gallons). For flukes: use praziquantel at recommended dose. Perform 25% water changes every 3 days, retest after each change. Maintain: ammonia 0 ppm, nitrite 0 ppm, pH 7.0-8.0, DO >5 mg/L. Quarantine new arrivals strictly. UV sterilization if available. TEST water every 3 days during treatment.",
            "Medium": "Moderate parasite load: TEST water DAILY (temperature critical for ich treatment). Isolate heavily infected fish. For ich: raise temperature to 84-86°F (monitor temperature every 4 hours to ensure stability) + salt + copper-based medication (follow instructions carefully - copper is toxic if overdosed). For flukes: praziquantel treatment for full 7-10 day cycle. For visible parasites (anchor worms/lice): manual removal with tweezers + topical antiseptic + antiparasitic medication. Treat entire tank/pond, not just infected fish. Keep ammonia 0 ppm, nitrite 0 ppm, DO >5 mg/L (higher temperature reduces DO - add aeration). Test twice daily for first week.",
            "High": "Heavy parasite infestation: EMERGENCY - TEST water EVERY 6 HOURS. Multiple parasites or severe infestation. Combination treatment approach: identify ALL parasite types present. Maintain pristine water: ammonia 0 ppm, nitrite 0 ppm, nitrate <20 ppm, pH 7.0-8.0, DO >6 mg/L, stable temperature. Use appropriate medications (may need formalin, copper sulfate, or praziquantel combinations - never mix without expert guidance). Test copper levels if using copper-based treatments (toxic above 0.25 mg/L). Consider moving to separate treatment tank (test treatment tank water before transfer). Daily monitoring essential. Some severe cases may need veterinary-grade treatments. Professional consultation highly recommended. Continue testing 3 times daily throughout treatment."
        }
    },
    "Fish_Viral diseases White tail disease": {
        "display_name": "Viral Diseases - White Tail Disease",
        "cause": "Caused by viral infection (White Tail Disease Virus - WTDV) affecting the tail region and muscle tissue. Highly contagious in shrimp and some fish species. Spread through water, infected animals, and contaminated equipment. Stress and poor conditions increase susceptibility.",
        "treatments": {
            "Low": "Early viral signs: NOTE - No direct antiviral cure available. TEST water immediately (all parameters: temperature, pH, ammonia, nitrite, nitrate, DO, salinity if applicable). Stress from poor water accelerates viral spread. Focus on supportive care: Isolate affected individuals immediately to prevent spread. Improve water quality (25-30% water change). Retest after 2 hours. Maintain OPTIMAL conditions: temperature stable (species-specific), pH 7.5-8.5, ammonia 0 ppm, nitrite 0 ppm, DO >6 mg/L. Boost immune system with vitamin C supplemented feed (100-500 mg/kg feed). Reduce stress. Monitor all animals closely. TEST water DAILY for 2 weeks. Remove and properly dispose of any dead fish.",
            "Medium": "Active viral infection spreading: TEST water TWICE DAILY (sunrise and evening). Strict quarantine protocols - separate infected from healthy populations. Perform 30-40% water changes with UV-treated or aged water, retest 2 hours after. Enhance immune support with immunostimulants (beta-glucans, vitamins). Maintain pristine water quality: ammonia 0 ppm, nitrite 0 ppm, nitrate <10 ppm, pH 7.5-8.5, DO >6 mg/L, stable temperature. Reduce feeding to minimize waste. Increase aeration. Consider culling severely infected individuals to prevent further spread. Disinfect all equipment with iodine or chlorine solutions. Continue testing twice daily for entire outbreak period.",
            "High": "CRITICAL - Widespread viral outbreak: EMERGENCY - TEST water EVERY 4 HOURS for all critical parameters. Biosecurity measures required. Complete isolation of infected populations. Consider partial or complete culling to prevent catastrophic spread. Immediate 50% water change with disinfected, well-oxygenated water (pre-test water quality). Maintain PERFECT conditions: ammonia 0 ppm, nitrite 0 ppm, nitrate <5 ppm, pH 7.5-8.5, DO >7 mg/L, temperature optimal and stable (±0.5°C). Stop all transfers between tanks/ponds. Disinfect equipment, nets, hands between handling. May require depopulation and complete system disinfection. Consult with fish disease specialist or aquatic veterinarian immediately. Report to local aquaculture authorities if applicable. Focus on saving healthy populations through strict biosecurity. Intensive water testing (every 4-6 hours) until outbreak controlled."
        }
    },
    "Fish_Healthy Fish": {
        "display_name": "Healthy Fish",
        "cause": "No disease detected - fish appears healthy with normal coloring, behavior, and no visible symptoms.",
        "treatments": {
            "Low": "Continue excellent aquaculture practices: TEST water WEEKLY as preventive monitoring. Test at sunrise for most accurate readings. Maintain optimal water quality: pH 6.5-8.5, ammonia 0 ppm, nitrite 0 ppm, nitrate <20 ppm, DO >5 mg/L (test at sunrise when DO is lowest). Monitor temperature daily - maintain species-specific optimal range. Provide balanced, high-quality nutrition. Avoid overcrowding (follow species-specific stocking guidelines). Perform regular 15-20% weekly water changes. Quarantine new fish for 2-4 weeks before introduction (test quarantine tank water 3 times per week). Monitor daily for any changes in behavior or appearance. Recommended testing schedule: Weekly for routine monitoring, or more frequently if conditions change (heavy rain, temperature swings, etc.).",
            "Medium": "Maintain preventive care routines: TEST water WEEKLY. Same parameters as Low severity. Continue monitoring.",
            "High": "Maintain preventive care routines: TEST water WEEKLY. Same parameters as Low severity. Continue monitoring."
        }
    },
    "Shrimp_Black_Gill": {
        "display_name": "Shrimp Black Gill Disease",
        "cause": "Caused by bacterial infection (primarily Vibrio species) affecting gill tissue. Results from poor water quality, high organic load, overcrowding, stress, or inadequate water exchange. Black discoloration indicates melanization response.",
        "treatments": {
            "Low": "Early infection: TEST water immediately (ammonia, nitrite, pH, DO, salinity). Perform 30% water change. Target: ammonia 0 ppm, nitrite 0 ppm, salinity 15-25 ppt, DO >5 mg/L, pH 7.5-8.5. Increase water exchange rate. Reduce feeding by 50%. Add probiotics to water/feed. Improve aeration. RETEST daily for 5 days.",
            "Medium": "Active infection: TEST water TWICE DAILY (sunrise, evening). Isolate if possible. Perform 40% water change daily for 3 days, retest after each. Use antibiotics (florfenicol or oxytetracycline - follow dosage). Maintain DO >6 mg/L, ammonia 0 ppm, perfect salinity. Reduce stocking density. Stop feeding for 24 hours, then 30% normal. Continue testing twice daily for 7-10 days.",
            "High": "CRITICAL - Severe gill necrosis: EMERGENCY testing EVERY 4 HOURS. Massive water change (50-60%). Aggressive antibiotic treatment (consult aquaculture vet). Maintain pristine conditions: DO >7 mg/L, ammonia 0 ppm, nitrite 0 ppm, optimal salinity, pH 8.0. Maximum aeration. Consider emergency harvest of healthy shrimp. May need complete pond/tank treatment. Professional consultation critical."
        }
    },
    "Shrimp_Healthy": {
        "display_name": "Healthy Shrimp",
        "cause": "No disease detected - shrimp appears healthy with normal color, activity, and no visible symptoms.",
        "treatments": {
            "Low": "Maintain optimal shrimp culture: TEST water TWICE WEEKLY (more than fish due to shrimp sensitivity). Monitor: salinity 15-25 ppt, pH 7.5-8.5, ammonia 0 ppm, nitrite 0 ppm, DO >5 mg/L, alkalinity 80-120 ppm. Daily water exchange 10-15%. Provide quality feed 3-4 times daily. Maintain proper stocking density. Use probiotics weekly. Monitor for molting issues. Quarantine new stock 3-4 weeks.",
            "Medium": "Continue preventive care. TEST water TWICE WEEKLY.",
            "High": "Continue preventive care. TEST water TWICE WEEKLY."
        }
    },
    "Shrimp_White_Spot_Syndrome_Virus": {
        "display_name": "White Spot Syndrome Virus (WSSV)",
        "cause": "Caused by White Spot Syndrome Virus - HIGHLY CONTAGIOUS viral disease. Spreads through water, infected animals, contaminated equipment, and carriers. Causes white spots on shell. High mortality rate (up to 100% in 3-10 days). No cure exists.",
        "treatments": {
            "Low": "Early viral detection: NO ANTIVIRAL CURE - supportive care only. URGENT biosecurity! TEST water DAILY. Complete isolation immediately. Improve water quality (30% change). Optimal conditions: DO >6 mg/L, pH 8.0-8.5, salinity stable, temperature 28-30°C, ammonia 0 ppm. Boost immunity: vitamin C (500-1000 mg/kg feed), immunostimulants. Stop new introductions. Disinfect equipment. May need to cull affected pond. Report to authorities.",
            "Medium": "Active outbreak: TEST water EVERY 6 HOURS. STRICT QUARANTINE - virus spreading fast. Emergency harvest healthy shrimp if possible. Maintain PERFECT water: DO >7 mg/L, all parameters optimal. Vitamin C + immunostimulants maximum dose. Complete isolation. Disinfect everything (chlorine, iodine). Consider emergency depopulation to save other ponds. No cure - focus on preventing spread.",
            "High": "CATASTROPHIC OUTBREAK: Total loss likely within days. EMERGENCY DEPOPULATION recommended to prevent farm-wide catastrophe. Complete drain and disinfect pond (chlorine 100 ppm for 48 hours). Bury/burn infected shrimp. Disinfect ALL equipment, boots, nets. Stop all water flow to other ponds. Report to local aquaculture authority IMMEDIATELY. Quarantine entire farm. Recovery requires 2-3 weeks complete drying + disinfection before restocking."
        }
    },
    "Shrimp_White_Spot_Syndrome_Virus_and_Black_Gill": {
        "display_name": "WSSV + Black Gill (Co-infection)",
        "cause": "Dual infection: White Spot Syndrome Virus (viral) + bacterial gill infection (Vibrio). Extremely serious - compromised shrimp from one disease susceptible to the other. Combined effect causes rapid mortality. Poor water quality + stress are major triggers.",
        "treatments": {
            "Low": "Co-infection detected: EXTREMELY SERIOUS even at low level. TEST water EVERY 6 HOURS immediately. Emergency water change 50%. Perfect conditions critical: DO >6 mg/L, ammonia 0 ppm, salinity optimal, pH 8.0-8.5. Antibiotics for bacterial component (won't affect virus). Maximum immune support (vitamin C 1000 mg/kg). Complete isolation. Emergency harvest consideration. Consult aquaculture vet immediately.",
            "Medium": "Advanced co-infection: EMERGENCY DEPOPULATION STRONGLY RECOMMENDED. Both diseases progressing - very high mortality expected. If attempting treatment: antibiotics + perfect water (TEST EVERY 4 HOURS) + maximum aeration + immune support. Realistically, focus on: 1) Emergency harvest any healthy shrimp, 2) Prevent spread to other ponds, 3) Prepare for total loss and pond disinfection.",
            "High": "TERMINAL OUTBREAK: Total loss imminent. IMMEDIATE ACTIONS: 1) Emergency depopulation NOW, 2) Complete drain and disinfect (chlorine 100-150 ppm), 3) Dispose infected shrimp (burn/deep bury), 4) Quarantine entire operation, 5) Disinfect ALL equipment/clothing, 6) Stop water exchange to other areas, 7) Report to authorities, 8) Plan 3-4 week complete disinfection cycle before any restocking. This is aquaculture emergency - act fast to save other ponds."
        }
    }
}

def determine_severity(confidence: float, disease_label: str) -> str:
    """
    Determine severity level based on confidence score and disease progression indicators.
    
    Args:
        confidence: Confidence score (0-1)
        disease_label: The disease label from model
    
    Returns:
        str: Severity level (Low, Medium, High)
    """
    # Healthy fish/shrimp is always low severity
    if "Healthy" in disease_label:
        return "Low"
    
    # For diseases, use confidence as proxy for severity/progression
    # Higher confidence with disease detection often indicates more visible/advanced symptoms
    if confidence >= 0.90:
        return "High"  # Very clear symptoms = advanced stage
    elif confidence >= 0.75:
        return "Medium"  # Moderate symptoms = progressing
    else:
        return "Low"  # Unclear/early symptoms = early stage


def get_treatment_summary(full_treatment: str, severity: str) -> str:
    """
    Generate mobile-friendly short summary of treatment.
    
    Args:
        full_treatment: Full treatment text
        severity: Severity level
    
    Returns:
        str: Concise treatment summary for mobile display
    """
    # Extract first 2-3 key actions from full treatment
    sentences = full_treatment.split('. ')
    
    if severity == "High":
        return f"🚨 URGENT: {sentences[0]}. {sentences[1] if len(sentences) > 1 else ''} Consult vet immediately."
    elif severity == "Medium":
        return f"⚠️ Act now: {sentences[0]}. {sentences[1] if len(sentences) > 1 else ''}"
    else:
        return f"📋 {sentences[0]}. Monitor closely for 3-5 days."


def get_disease_info(label: str, confidence: float):
    """
    Get comprehensive disease information based on model prediction.
    
    Args:
        label: The disease label from the model
        confidence: Confidence score (0-1)
    
    Returns:
        dict: Disease information including name, cause, severity, and treatment
    """
    # Log the input for debugging
    print(f"[DEBUG] get_disease_info called with label='{label}', confidence={confidence}")
    
    # Get disease info from knowledge base
    disease_data = DISEASE_KNOWLEDGE.get(label)
    
    if not disease_data:
        # Log that disease was not found
        print(f"[DEBUG] Disease '{label}' not found in knowledge base")
        print(f"[DEBUG] Available diseases: {list(DISEASE_KNOWLEDGE.keys())}")
        
        # Fallback for unknown diseases
        disease_name = label.replace("Fish_", "").replace("_", " ")
        return {
            "disease_name": disease_name,
            "confidence": confidence,
            "cause": "Information not available for this condition. Please consult a fish disease specialist for accurate diagnosis.",
            "severity": "Unknown",
            "treatment": "Consult a professional fish disease specialist or aquatic veterinarian for proper diagnosis and treatment plan.",
            "warning": None
        }
    
    # Determine severity based on confidence and disease type
    severity = determine_severity(confidence, label)
    
    # Get severity-appropriate treatment
    treatment = disease_data["treatments"].get(severity, disease_data["treatments"]["Medium"])
    
    # Prepare response
    response = {
        "disease_name": disease_data["display_name"],
        "confidence": confidence,
        "cause": disease_data["cause"],
        "severity": severity,
        "treatment": treatment,
        "treatment_summary": get_treatment_summary(treatment, severity),  # Mobile-friendly short version
        "warning": None
    }
    
    # Add warning for low confidence predictions
    if confidence < 0.7:  # Below 70% confidence
        response["warning"] = {
            "level": "high",
            "message": "⚠️ Low confidence detection. The AI model is uncertain about this diagnosis. This may indicate early-stage disease or image quality issues. Please consult a fish disease specialist or aquatic veterinarian for professional confirmation before starting any treatment. Consider taking multiple clear photos from different angles for better analysis."
        }
    elif confidence < 0.85:  # Between 70-85% confidence
        response["warning"] = {
            "level": "medium",
            "message": "Note: Moderate confidence level. While the detection appears reasonable, we recommend monitoring your fish closely and consulting a specialist if symptoms worsen or persist. The severity level is estimated based on visible symptoms."
        }
    
    return response

def get_confidence_threshold_message(confidence: float) -> str:
    """
    Get appropriate message based on confidence level.
    
    Args:
        confidence: Confidence score (0-1)
    
    Returns:
        str: Appropriate message for the confidence level
    """
    if confidence >= 0.9:
        return "High confidence detection. The diagnosis is highly reliable."
    elif confidence >= 0.8:
        return "Good confidence level. The diagnosis appears accurate."
    elif confidence >= 0.7:
        return "Moderate confidence. Consider monitoring and consulting a specialist if needed."
    else:
        return "Low confidence. Professional consultation strongly recommended."
