from fastapi import FastAPI, Query
from pydantic import BaseModel
import joblib
from classifier.utils import extract_features
import pandas as pd

class URLInput(BaseModel):
    url: str

app = FastAPI()

model = joblib.load("classifier/randomforest/rf_model.pkl")
feature_names = joblib.load("classifier/randomforest/selected_columns.pkl")

@app.post("/predict")
def predict_url(data: URLInput):
    features = extract_features(data.url).to_frame().T

    for col in feature_names:
        if col not in features.columns:
            features[col] = 0
    features = features[feature_names]

    prediction = model.predict(features)[0]
    return {"url": data.url, "prediction": int(prediction)}
