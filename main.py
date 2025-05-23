from fastapi import FastAPI, Query
from pydantic import BaseModel
import joblib
from classifier.utils import extract_features
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

class URLInput(BaseModel):
    url: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("classifier/randomForestV2/rf_model.pkl")
feature_names = joblib.load("classifier/randomForestV2/selected_columns.pkl")
label_encoder = joblib.load("classifier/randomForestV2/label_encoder.pkl")

@app.post("/predict")
def predict_url(data: URLInput):
    features = extract_features(data.url).to_frame().T

    for col in feature_names:
        if col not in features.columns:
            features[col] = 0
    features = features[feature_names]

    prediction = model.predict(features)[0]
    label_name = label_encoder.inverse_transform([prediction])[0]

    print(f'Url:{data.url}\n Class:{label_name}')
    return {"url": data.url, "predicted_class": label_name}
