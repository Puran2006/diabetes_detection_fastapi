from pydantic import BaseModel, Field
from typing import Dict

# Input Schema
class DiabetesInput(BaseModel):
    Pregnancies: float = Field(..., ge=0, description="Number of times pregnant")
    Glucose: float = Field(..., ge=0, description="Plasma glucose concentration")
    BloodPressure: float = Field(..., ge=0, description="Diastolic blood pressure")
    Insulin: float = Field(..., ge=0, description="2-Hour serum insulin")
    BMI: float = Field(..., ge=0, description="Body mass index (BMI)")
    DiabetesPedigreeFunction: float = Field(..., ge=0, description="Diabetes pedigree function")
    Age: float = Field(..., ge=0, description="Age in years")

    class Config:
        json_schema_extra = {
            "example": {
                "Pregnancies": 2,
                "Glucose": 120,
                "BloodPressure": 70,
                "Insulin": 85,
                "BMI": 28.5,
                "DiabetesPedigreeFunction": 0.5,
                "Age": 35
            }
        }

# Response Schema
class PredictionResponse(BaseModel):
    prediction: str
    probability: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "Non-Diabetic",
                "probability": "23.45%",
                "message": "Hello, user! Great news! You are not diabetic. Keep maintaining a healthy lifestyle!"
            }
        }

class ChatRequest(BaseModel):
    glucose: float
    blood_pressure: float
    insulin: float
    bmi: float
    age: int
    diabetes_pedigree_function: float
    prediction: str
    probability: str

    class Config:
        json_schema_extra = {
            "example": {
                "glucose": 140,
                "blood_pressure": 85,
                "insulin": 120,
                "bmi": 28.5,
                "age": 35,
                "diabetes_pedigree_function": 0.62,
                "prediction": "Diabetic",
                "probability": "76.89%"
            }
        }