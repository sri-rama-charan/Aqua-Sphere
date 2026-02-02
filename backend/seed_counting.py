import os
import base64
import io
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image
import httpx

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover - handled at runtime
    YOLO = None

MODEL_ENV_KEY = "FISH_SEED_MODEL_PATH"
DEFAULT_MODEL_PATH = os.getenv(MODEL_ENV_KEY, "models/fish_seed_count.pt")
DEFAULT_CONFIDENCE = float(os.getenv("FISH_SEED_CONFIDENCE", "0.05"))

ROBOFLOW_MODEL_ID_DEFAULT = "fish-fry-detection-for-counting/1"
ROBOFLOW_BASE_URL_DEFAULT = "https://detect.roboflow.com"

_yolo_model = None


def _ensure_ultralytics_available() -> None:
    if YOLO is None:
        raise RuntimeError(
            "Ultralytics is not installed. Please add 'ultralytics' to backend requirements."
        )


def get_seed_model():
    global _yolo_model
    _ensure_ultralytics_available()

    if _yolo_model is None:
        if not os.path.exists(DEFAULT_MODEL_PATH):
            raise FileNotFoundError(
                f"Seed count model not found at '{DEFAULT_MODEL_PATH}'. "
                f"Set {MODEL_ENV_KEY} to the correct .pt file."
            )
        _yolo_model = YOLO(DEFAULT_MODEL_PATH)

    return _yolo_model


def _get_roboflow_config() -> Tuple[str, str, str]:
    api_key = os.getenv("ROBOFLOW_API_KEY", "").strip()
    model_id = os.getenv("ROBOFLOW_MODEL_ID", ROBOFLOW_MODEL_ID_DEFAULT).strip()
    base_url = os.getenv("ROBOFLOW_BASE_URL", ROBOFLOW_BASE_URL_DEFAULT).strip()
    return api_key, model_id, base_url


async def _predict_with_roboflow(image: Image.Image, confidence: float) -> Dict[str, Any]:
    api_key, model_id, base_url = _get_roboflow_config()
    if not api_key:
        raise RuntimeError(
            "Roboflow API key is not configured. Set ROBOFLOW_API_KEY or provide a local model path."
        )

    buffered = image.convert("RGB")
    async with httpx.AsyncClient(timeout=60) as client:
        png_buffer = io.BytesIO()
        buffered.save(png_buffer, format="PNG")
        png_bytes = png_buffer.getvalue()

        # Roboflow expects confidence as percentage (0-100)
        conf_percent = confidence * 100 if confidence <= 1 else confidence
        conf_percent = max(1, min(99, conf_percent))

        url = f"{base_url.rstrip('/')}/{model_id}"
        params = {
            "api_key": api_key,
            "confidence": conf_percent,
        }

        files = {"file": ("image.png", png_bytes, "image/png")}
        response = await client.post(url, params=params, files=files)
        response.raise_for_status()
        data = response.json()

    predictions = data.get("predictions", [])
    detections = []
    for pred in predictions:
        x = float(pred.get("x", 0))
        y = float(pred.get("y", 0))
        w = float(pred.get("width", 0))
        h = float(pred.get("height", 0))
        conf = float(pred.get("confidence", 0))
        class_id = pred.get("class", 0)
        detections.append(
            {
                "bbox": [round(x - w / 2, 2), round(y - h / 2, 2), round(x + w / 2, 2), round(y + h / 2, 2)],
                "confidence": round(conf, 4),
                "class_id": class_id,
            }
        )

    return {
        "count": len(detections),
        "confidence_threshold": conf_percent / 100,
        "detections": detections,
    }


async def predict_seed_count(image: Image.Image, confidence: Optional[float] = None) -> Dict[str, Any]:
    conf_threshold = DEFAULT_CONFIDENCE if confidence is None else confidence
    conf_threshold = max(0.001, min(0.999, conf_threshold))

    if os.path.exists(DEFAULT_MODEL_PATH):
        model = get_seed_model()
        results = model.predict(source=image, conf=conf_threshold, verbose=False)
        if not results:
            return {
                "count": 0,
                "confidence_threshold": conf_threshold,
                "detections": [],
            }

        result = results[0]
        detections: List[Dict[str, Any]] = []

        if result.boxes is not None:
            for box in result.boxes:
                xyxy = box.xyxy[0].tolist()
                conf = float(box.conf[0]) if box.conf is not None else 0.0
                cls = int(box.cls[0]) if box.cls is not None else 0
                detections.append(
                    {
                        "bbox": [round(v, 2) for v in xyxy],
                        "confidence": round(conf, 4),
                        "class_id": cls,
                    }
                )

        return {
            "count": len(detections),
            "confidence_threshold": conf_threshold,
            "detections": detections,
        }

    return await _predict_with_roboflow(image=image, confidence=conf_threshold)
