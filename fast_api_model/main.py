from fastapi import FastAPI
from pydantic import BaseModel
import pickle


class PredictionRequest(BaseModel):
    text: str


app = FastAPI()

# with open('models/trained_model.pkl', 'rb') as f:
    # model = pickle.load(f)


@app.post("/classify/")
async def classify(request: PredictionRequest):
    # prediction = model.predict([request.text])
    prediction = "we don't have a model yet"
    return {"prediction": prediction}
