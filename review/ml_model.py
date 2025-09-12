import os
import pickle
from threading import Lock

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 150

# Globals for lazy load
_model = None
_tokenizer = None
_label_encoder = None
_lock = Lock()


def _get_model_paths():
    """Build absolute paths to your model files."""
    ml_dir = os.path.join(os.path.dirname(__file__), "ml_models")
    return {
        "model": os.path.join(ml_dir, "model_dl.h5"),
        "tokenizer": os.path.join(ml_dir, "tokenizer.pkl"),
        "label_encoder": os.path.join(ml_dir, "label_encoder.pkl"),
    }


def _load_model():
    """Actually load the model & pickled objects."""
    # Import inside to avoid heavy import at module load
    from tensorflow.keras.models import load_model

    paths = _get_model_paths()
    model = load_model(paths["model"])
    with open(paths["tokenizer"], "rb") as f:
        tokenizer = pickle.load(f)
    with open(paths["label_encoder"], "rb") as f:
        label_encoder = pickle.load(f)
    return model, tokenizer, label_encoder


def _ensure_loaded():
    """Load model/tokenizer/encoder only once, on first use."""
    global _model, _tokenizer, _label_encoder
    if _model is None:
        with _lock:
            if _model is None:  # double check inside lock
                _model, _tokenizer, _label_encoder = _load_model()


def predict_rating(text: str) -> int:
    """
    Predict a rating from review text.
    Returns an integer rating (e.g., 1–5).
    """
    if not text or not text.strip():
        return 0  # or raise ValueError if you want

    _ensure_loaded()

    # Preprocess text
    seq = _tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=MAX_LEN)

    # Model prediction
    prediction = _model.predict(padded)
    predicted_class = np.argmax(prediction, axis=1)

    # Map class back to rating
    rating = int(_label_encoder.inverse_transform(predicted_class)[0])
    return rating
