
import os
import logging
from io import BytesIO
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ChestScan AI API",
    description=(
        "Prototype pédagogique de classification "
        "de radiographies thoraciques. "
        "Non destiné au diagnostic médical."
    ),
    version="0.2.0",
)

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", "/app/artifacts/models/model.keras")
)

CLASS_NAMES = ["NORMAL", "PNEUMONIA"]
IMAGE_SIZE = (180, 180)
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/bmp"}

model = None
model_load_error = None


def load_prediction_model():
    """Charge le modèle une seule fois au démarrage."""
    global model, model_load_error

    try:
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Modèle introuvable : {MODEL_PATH}"
            )

        model = tf.keras.models.load_model(
            MODEL_PATH,
            custom_objects={
                "preprocess_input": preprocess_input
            },
            compile=False,
        )

        if model.output_shape[-1] != 1:
            raise ValueError(
                f"Sortie inattendue : {model.output_shape}"
            )

        model_load_error = None
        logger.info("Modèle chargé : %s", MODEL_PATH)

    except Exception as exc:
        model = None
        model_load_error = str(exc)
        logger.exception("Impossible de charger le modèle")


@app.on_event("startup")
def startup_event():
    load_prediction_model()


@app.get("/")
def root():
    return {
        "application": "ChestScan AI API",
        "docs": "/docs",
        "health": "/health",
        "model_loaded": model is not None,
    }


@app.get("/health")
def health():
    return {
        "status": "ok" if model is not None else "degraded",
        "model_available": MODEL_PATH.is_file(),
        "model_loaded": model is not None,
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Modèle indisponible. Vérifiez les logs de l'API.",
        )

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Formats acceptés : JPEG, PNG ou BMP.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Fichier vide.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Taille maximale autorisée : 10 Mio.",
        )

    try:
        with Image.open(BytesIO(content)) as original:
            image = ImageOps.exif_transpose(original).convert("RGB")
            image = image.resize(IMAGE_SIZE)

            image_array = np.asarray(
                image, dtype=np.float32
            )

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Le fichier ne contient pas une image valide.",
        )


    batch = np.expand_dims(image_array, axis=0)

    try:
        raw_prediction = model.predict(batch, verbose=0)
        pneumonia_probability = float(raw_prediction[0][0])

    except Exception:
        logger.exception("Erreur pendant la prédiction")
        raise HTTPException(
            status_code=500,
            detail="Erreur pendant la prédiction.",
        )

    # Hypothèse : label 0 = NORMAL, label 1 = PNEUMONIA.
    predicted_index = (
        1 if pneumonia_probability >= 0.5 else 0
    )
    predicted_class = CLASS_NAMES[predicted_index]

    confidence = (
        pneumonia_probability
        if predicted_index == 1
        else 1.0 - pneumonia_probability
    )

    return {
        "filename": file.filename,
        "prediction": predicted_class,
        "confidence": round(confidence, 4),
        "pneumonia_probability": round(
            pneumonia_probability, 4
        ),
        "threshold": 0.5,
        "warning": (
            "Prototype pédagogique uniquement. "
            "Ce résultat ne constitue pas un diagnostic médical."
        ),
    }
