from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import io
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
@app.post("/predict-bulk")
async def predict_bulk(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Machine learning model failed to load.")
    
    # 1. Read the uploaded CSV file bytes
    contents = await file.read()
    
    try:
        # 2. Convert the raw bytes into a Pandas DataFrame
        input_data = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file format.")
    
    # 3. Validate that the CSV has the correct columns
    required_columns = ["income", "credit_score", "dti_ratio"]
    if not all(col in input_data.columns for col in required_columns):
        raise HTTPException(status_code=400, detail=f"CSV must contain columns: {required_columns}")
    
    # 4. Feed the entire batch of data to the model in one shot
    predictions = model.predict(input_data[required_columns])
    
    # 5. Append the predictions as new columns so the frontend can display them
    input_data["prediction"] = predictions
    input_data["risk_assessment"] = ["High Risk (Default)" if p == 1 else "Low Risk (Safe)" for p in predictions]
    
    # 6. Convert the DataFrame back to a JSON-friendly list of dictionaries
    return input_data.to_dict(orient="records")