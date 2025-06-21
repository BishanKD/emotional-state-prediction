from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from src.preprocess import clean_text

# Load model and vectorizer
with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("models/rfr_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict")
def predict_emotion(data: InputText):
    clean = clean_text(data.text)
    vector = vectorizer.transform([clean])
    pred = model.predict(vector)[0]
    pred = max(0.0, min(1.0, pred))
    return {"emotion_score": round(pred, 3)}
