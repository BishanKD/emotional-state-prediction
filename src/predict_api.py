from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from src.preprocess import clean_text
import tensorflow as tf

# # Load model and vectorizer
# with open("models/vectorizer.pkl", "rb") as f:
#     vectorizer = pickle.load(f)

# # with open("models/rfr_model.pkl", "rb") as f:
# #     model = pickle.load(f)
# with open("models/svr_model.pkl", "rb") as f:
#     model = pickle.load(f)

# Load tokenizer
with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load trained LSTM model
model = tf.keras.models.load_model("models/lstm_glove.keras")

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict")
def predict_emotion(data: InputText):
    clean = clean_text(data.text)
    # vector = vectorizer.transform([clean])
    seq = tokenizer.texts_to_sequences([clean])
    padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=200)
    pred = model.predict(padded)[0][0]
    pred = max(0.0, min(1.0, float(pred)))
    return {"emotion_score": round(pred, 3)}
