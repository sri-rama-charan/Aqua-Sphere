# 🐟🦐 Fish & Shrimp Disease Detection App

AI-powered mobile application for automated disease detection in aquaculture, supporting fish and shrimp health monitoring.

## 🎯 Features

- **11 Disease Classifications**: 7 fish diseases + 4 shrimp diseases
- **98.32% Accuracy**: Using Vision Transformer (ViT) model
- **Real-time Detection**: Upload photo, get instant diagnosis
- **Comprehensive Information**:
  - Disease name and confidence level
  - Cause and severity assessment
  - Water quality testing protocols
  - Detailed treatment recommendations
  - Low confidence warnings
- **Mobile Optimized**: Built with Capacitor for Android
- **Severity-Based Guidance**: Treatment protocols vary by disease stage

## 🏥 Supported Diseases

### Fish Diseases (7)
1. Bacterial Red Disease
2. Aeromoniasis
3. Bacterial Gill Disease
4. Fungal Saprolegniasis
5. Parasitic Diseases
6. Viral White Tail Disease
7. Healthy Fish

### Shrimp Diseases (4)
1. Black Gill
2. White Spot Syndrome Virus (WSSV)
3. WSSV + Black Gill Co-infection
4. Healthy Shrimp

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python)
- Transformers (HuggingFace)
- Vision Transformer (ViT) model
- PIL for image processing

**Frontend:**
- React + TypeScript
- Vite
- TailwindCSS + shadcn/ui
- Capacitor (Android native)

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- HuggingFace account (for model access)

## 🚀 Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your HuggingFace token to `.env`:
```
HF_TOKEN=your_huggingface_token_here
```

6. Start backend:
```bash
uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run at: `http://localhost:5173`

## 🔑 Getting HuggingFace Token

1. Create account at [HuggingFace](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create new token with `read` permission
4. Copy token to backend `.env` file

## 📱 Building for Android

1. Build frontend:
```bash
cd frontend
npm run build
```

2. Sync with Capacitor:
```bash
npx cap sync android
```

3. Open in Android Studio:
```bash
npx cap open android
```

4. Build APK in Android Studio

## 🌐 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /predict` - Disease detection (multipart/form-data with image file)

### Example Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@fish_image.jpg"
```

### Example Response

```json
{
  "disease_name": "Bacterial Red Disease",
  "confidence": 0.95,
  "cause": "Caused by bacteria...",
  "severity": "High",
  "treatment": "Full treatment instructions...",
  "treatment_summary": "🚨 URGENT: Test water every 2 hours...",
  "warning": {
    "level": "medium",
    "message": "Moderate confidence level..."
  }
}
```

## 📊 Severity Levels

Automatically determined by AI confidence:
- **High** (90%+ confidence): Advanced disease stage - urgent action
- **Medium** (75-90% confidence): Active infection - prompt treatment
- **Low** (<75% confidence): Early stage - monitor closely

## 🧪 Water Testing Protocols

Treatment recommendations include specific testing schedules:
- **Low severity**: Every 2-3 days
- **Medium severity**: Daily (twice per day)
- **High severity**: Every 2-6 hours

Critical parameters monitored:
- Ammonia (must be 0 ppm)
- Nitrite (must be 0 ppm)
- Dissolved Oxygen (>5-7 mg/L)
- pH (6.5-8.5 for fish, 7.5-8.5 for shrimp)
- Temperature (species-specific)
- Salinity (for shrimp)

## 🔒 Security Notes

- **Never commit** `.env` files
- **Never commit** signing keys (`.jks`, `.keystore`)
- Keep HuggingFace token secure
- Use environment variables for sensitive data

## 📁 Project Structure

```
fish-disease-detector/
├── backend/
│   ├── disease_knowledge.py  # Disease database
│   ├── main.py               # FastAPI server
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   └── lib/              # Utilities
│   ├── android/              # Android native project
│   └── package.json
└── DISEASE_INFO_GUIDE.md     # Disease information reference
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

Apache 2.0 License

## 🙏 Acknowledgments

- Model: [Saon110/fish-shrimp-disease-classifier](https://huggingface.co/Saon110/fish-shrimp-disease-classifier)
- Water quality protocols: FAO Aquaculture Guidelines
- UI Components: shadcn/ui

## ⚠️ Disclaimer

This tool is for **research and educational purposes**. Always consult qualified veterinary professionals for clinical diagnoses and treatment decisions. Model predictions should be validated against expert knowledge.

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Built for aquaculture farmers and fish health professionals** 🐟🦐
