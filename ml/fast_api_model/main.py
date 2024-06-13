from http.client import HTTPException

import fasttext
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from ml.fast_api_model.dependencies import predict_class


class PredictionRequest(BaseModel):
    text: str


app = FastAPI()

# with open('models/trained_model.pkl', 'rb') as f:
# model = pickle.load(f)


ft = fasttext.load_model('../ml_core/data/embedding_data/cc.fr.300.bin')


@app.post("/classify_o/")
async def classify(request: PredictionRequest):
    print(request.text)

    ### load embedder
    def text_to_vector(text):
        words = text.split(' ')
        word_vectors = [ft.get_word_vector(word) for word in words if word in ft.words]
        if not word_vectors:
            return np.zeros(300)
        return np.mean(word_vectors, axis=0)

    ### call the embedder
    text_to_vectors = np.expand_dims(text_to_vector(request.text), axis=0)

    ### call for prediction
    classification = predict_class(text_to_vectors)

    print(f"CLASSIFICATION \n {classification[0][0]}")

    if classification is None:
        raise HTTPException(status_code=404, detail="Classification failed")
    return {"class": str(classification[0][0])}