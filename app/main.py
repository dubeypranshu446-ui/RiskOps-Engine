from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- ADD THIS IMPORT
import joblib
import pandas as pd
from .schemas import CreditApplication

app = FastAPI(title="RiskOps Engine API", version="1.0")

# <-- ADD THIS ENTIRE MIDDLEWARE BLOCK -->
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains/ports to access the API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model globally so it initializes immediately on server startup
try:
    model = joblib.load("artifacts/credit_model.joblib")
except Exception as e:
    model = None

@app.get("/")
def health_check():
    return {"status": "active", "system": "RiskOps Engine", "model_loaded": model is not None}

@app.post("/predict")
def predict_risk(application: CreditApplication):
    if not model:
        raise HTTPException(status_code=500, detail="Machine learning model failed to load.")
    
    # 1. Convert the incoming validated data into a Pandas DataFrame
    input_data = pd.DataFrame([application.model_dump()])
    
    # 2. Feed the data to the Random Forest model
    prediction = model.predict(input_data)[0]
    
    # 3. Format the response
    risk_level = "High Risk (Default)" if prediction == 1 else "Low Risk (Safe)"
    
    return {
        "prediction": int(prediction),
        "risk_assessment": risk_level
    }