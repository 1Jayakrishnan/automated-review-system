import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'model_dl.h5')
TOKENIZER_PATH = os.path.join(BASE_DIR, 'ml_models', 'tokenizer.pkl')
LABELENC_PATH = os.path.join(BASE_DIR, 'ml_models', 'labelencoder.pkl')

# Load model & preprocessing objects once at import
model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, 'rb') as f:
    tokenizer = pickle.load(f)
with open(LABELENC_PATH, 'rb') as f:
    label_encoder = pickle.load(f)

MAX_LEN = 150  # must match training

def predict_rating(text: str) -> int:
    # Preprocess text and return predicted rating.
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post')
    preds = model.predict(padded)
    pred_index = np.argmax(preds, axis=1)[0]
    rating = label_encoder.inverse_transform([pred_index])[0]
    return int(rating)
