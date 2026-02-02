# Fish Disease Detection - Enhanced Information System

## Overview
The system now provides comprehensive disease information including causes, severity levels, detailed treatment recommendations, and **critical water testing protocols** based on real-world aquaculture best practices (FAO guidelines).

## Key Water Parameters to Monitor

### Essential Parameters (Test for ALL diseases):
1. **Ammonia (NH₃)** - Must be 0 ppm (toxic to fish)
2. **Nitrite (NO₂⁻)** - Must be 0 ppm (toxic to fish)
3. **Nitrate (NO₃⁻)** - Should be <20 ppm (acceptable up to 40 ppm)
4. **pH** - Optimal range 6.5-8.5 (varies by species)
5. **Dissolved Oxygen (DO)** - Minimum 5 mg/L (higher for gill diseases)
6. **Temperature** - Species-specific, maintain stability

### Testing Schedule Based on Severity:

#### **Low Severity (Early Stage Disease)**
- **Frequency**: Test immediately, then every 2-3 days
- **Best time**: At sunrise (when DO is lowest)
- **Parameters**: All 6 essential parameters
- **Retest**: After each water change (wait 1-2 hours)

#### **Medium Severity (Active Infection)**
- **Frequency**: Test DAILY (twice per day: sunrise + midday)
- **Best times**: 
  - Sunrise (minimum DO, lowest pH)
  - Midday or early afternoon (maximum pH, check if fish are stressed)
- **Parameters**: All 6 essential parameters
- **Retest**: 1-2 hours after water changes
- **Duration**: Continue for 7-10 days or until stable

#### **High Severity (Critical/Emergency)**
- **Frequency**: Test EVERY 2-6 HOURS initially
- **Bacterial Gill Disease**: Every 2-3 hours (oxygen-critical!)
- **Viral Outbreak**: Every 4 hours
- **Bacterial Infections**: Every 4-6 hours
- **Parameters**: ALL parameters, focus on ammonia/nitrite/DO
- **Duration**: Continue intensive testing for 48 hours, then reduce to 3-4 times daily

### Special Testing Notes by Disease Type:

**Bacterial Gill Disease** (OXYGEN-CRITICAL)
- Test DO every 2-3 hours in high severity
- Ammonia and nitrite are life-or-death - must stay at 0 ppm
- Test BEFORE and AFTER any treatment

**Viral Diseases** (WATER QUALITY-DEPENDENT)
- No cure available - water quality is everything
- Test twice daily minimum, even in low severity
- Perfect water conditions slow viral spread

**Parasitic Diseases** (TEMPERATURE-DEPENDENT)
- Monitor temperature every 4 hours when treating ich
- Test copper levels if using copper-based treatments (toxic >0.25 mg/L)
- Temperature changes affect DO - retest DO after temp adjustments

**Fungal Diseases** (pH & TEMPERATURE-DEPENDENT)
- Test pH daily (fungi thrive in wrong pH)
- Monitor temperature stability (gradual changes only)
- Test after temperature adjustments

## Features Implemented

### 1. Disease Knowledge Base
Located in `backend/disease_knowledge.py`, contains detailed information for 10 fish diseases:

- **Aeromoniasis** (Medium severity)
- **Bacterial Gill Disease** (High severity)
- **Bacterial Red Disease** (High severity)
- **Columnaris** (High severity)
- **Epizootic Ulcerative Syndrome** (High severity)
- **Healthy Fish** (Low severity)
- **Parasitic Diseases** (Medium severity)
- **Red Spots Disease** (Medium severity)
- **Tail and Fin Rot** (Medium severity)
- **White Spot Disease (Ich)** (Medium severity)

Each disease includes:
- **Display Name**: User-friendly disease name
- **Cause**: Detailed explanation of disease causes and triggers
- **Severity**: Low, Medium, or High
- **Treatment**: Comprehensive, actionable treatment steps for farmers

### 2. Confidence-Based Warnings

The system automatically generates warnings based on confidence levels:

- **Below 70% confidence**: HIGH WARNING
  - Red alert displayed
  - Recommends consulting a specialist before treatment
  - Suggests taking additional photos from different angles

- **70-85% confidence**: MEDIUM WARNING
  - Yellow notice displayed
  - Advises monitoring and specialist consultation if symptoms persist

- **85%+ confidence**: No warning
  - High reliability detection
  - Treatment recommendations can be followed with confidence

### 3. Backend Enhancements

**File**: `backend/main.py`
- Imports disease knowledge base
- Enriches model predictions with comprehensive disease information
- Returns structured JSON with all disease details and warnings

**API Response Structure**:
```json
{
  "disease_name": "Bacterial diseases - Aeromoniasis",
  "confidence": 0.99,
  "cause": "Caused by Aeromonas bacteria...",
  "severity": "Medium",
  "treatment": "Isolate infected fish. Improve water quality...",
  "warning": {
    "level": "medium",
    "message": "Warning message text..."
  }
}
```

### 4. Frontend Enhancements

**New Component**: `frontend/src/components/ConfidenceWarning.tsx`
- Displays visual warnings for low/medium confidence
- Color-coded alerts (red for high warning, yellow for medium)
- Clear messaging to guide farmers

**Updated Component**: `frontend/src/components/ResultsSection.tsx`
- Now displays warning alerts when confidence is low
- Shows all disease information in organized cards
- Improved user experience with visual feedback

**Updated Component**: `frontend/src/pages/Index.tsx`
- Properly maps backend response to frontend structure
- Handles optional warning field

## Usage for Farmers

1. **Upload fish image** → App analyzes it
2. **View detection results** including:
   - Disease name
   - Confidence level
   - Cause of the disease
   - Severity level
   - Detailed treatment steps
3. **If low confidence**: System warns to consult specialist
4. **If high confidence**: Follow treatment recommendations
5. **Monitor fish**: Track progress and adjust treatment

## Treatment Information Quality

All treatment recommendations include:
- ✅ Immediate actions to take
- ✅ Water quality improvements
- ✅ Medication recommendations (specific antibiotics/treatments)
- ✅ Dosage guidance (e.g., "1-3 tablespoons per 5 gallons")
- ✅ Environmental adjustments (temperature, aeration, etc.)
- ✅ Isolation and biosecurity measures
- ✅ Follow-up care instructions

## Severity Levels Explained

- **Low**: Minimal risk, preventive care recommended
- **Medium**: Requires treatment, manageable with proper care
- **High**: Urgent action needed, potentially fatal if untreated

## Future Enhancements (Optional)

- Add images/diagrams for each disease
- Multi-language support for international farmers
- Treatment cost estimates
- Local veterinarian finder
- Treatment progress tracker
- Historical disease records per farm

## Testing the System

1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Upload a fish image
4. Verify all information displays correctly
5. Test with different confidence scenarios

## Notes

- Knowledge base is easily extensible - add new diseases to `DISEASE_KNOWLEDGE` dictionary
- Warning thresholds can be adjusted in `get_disease_info()` function
- All information based on aquaculture best practices and veterinary guidelines
