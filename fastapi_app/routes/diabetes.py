from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
import logging
import pickle
from schemas.diabetes import DiabetesInput, PredictionResponse, ChatRequest
import numpy as np
from utils import get_current_user
from schemas.user import UserResponse
import requests

# setting Up Logginf files
logging.basicConfig(
    filename="app.log",  # Save logs in a file
    level=logging.INFO,  # Log level: INFO (can change to DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format logs
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)
logger = logging.getLogger(__name__)  # Create a logger instance

# Hugging Face API settings
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_API_KEY = "your_hugging_face_api_access_token"


# fast api
app = FastAPI()

#Loading our model
try:
    with open("diabetes_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model/scaler: {e}")
    raise RuntimeError("Model file is missing or corrupted!")
  
#model dependency func
def get_model(): # dependency function which can be used in future
    return model


router = APIRouter()


# Function to Generate Message and Advice
def generate_advice(prediction: int, probability: float) -> str:
    """Returns a user-friendly health message based on prediction probability."""
    if prediction == 1:
        if probability > 0.80:
            return "You are at high risk for diabetes. Please consult a doctor immediately!"
        elif probability > 0.50:
            return "You have a moderate risk for diabetes. Consider lifestyle changes and check with a doctor."
        else: 
            return "You have a low risk but should still maintain a healthy lifestyle."
    else:
        return "Great news! You are not diabetic. Keep maintaining a healthy lifestyle!"



@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK,
    summary="Predict Diabetes",
    description="Provide patient details and get a diabetes prediction with probability score."
)
def predict(data: DiabetesInput, model=Depends(get_model),
            user: UserResponse = Depends(get_current_user)
  ):
    try:
        # Convert input data to NumPy array
        input_data = np.array([[
            data.Pregnancies, data.Glucose, data.BloodPressure, 
            data.Insulin, data.BMI,
            data.DiabetesPedigreeFunction, data.Age
        ]])
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        advice = generate_advice(prediction, probability)
        logger.info(f" User '{user.username}' - Prediction: {result} (Probability: {probability:.2f}%)")
        personalized_message = f"Hello, {user.username}! {advice}"
        logger.info(f" Message:{personalized_message}")

        return {
            "prediction": result,
            "probability": f"{probability * 100:.2f}%",
            "message": personalized_message
        }

    except Exception as e:
        logger.error(f" Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error. Please check the model and input data."
        )


# Chatbot Route

@router.post("/chat", status_code=status.HTTP_200_OK)
def chat(request: ChatRequest, user: UserResponse = Depends(get_current_user)):
    """ Chatbot providing health advice based on diabetes risk prediction. """

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized: Please log in first.")

    # Construct user health summary
    health_summary = (
        f"User {user.username} has a {request.prediction} diabetes risk "
        f"with a probability of {request.probability}.\n"
        f"Health details:\n"
        f"- Glucose: {request.glucose}\n"
        f"- Blood Pressure: {request.blood_pressure}\n"
        f"- Insulin: {request.insulin}\n"
        f"- BMI: {request.bmi}\n"
        f"- Age: {request.age}\n"
        f"- Diabetes Pedigree Function: {request.diabetes_pedigree_function}\n"
        f"Provide **concise** health recommendations for diabetes prevention and management "
        f"in **bullet points** (avoid unnecessary introductions)."
    )

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": health_summary}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            bot_response = response.json()[0]["generated_text"]
            logger.info(f"Model Generated text : {bot_response}")
            advice_lines = bot_response.split("\n")
            structured_advice = []
            count = 0
            for line in advice_lines:
                line = line.strip()
                # Ignore lines that contain "User", "Health details", or input summary
                if count < 10 :
                    count = count + 1
                    continue
                structured_advice.append(f"{line}")

            logger.info(f" Advice:{structured_advice}")
            return {"advice": "\n".join(structured_advice)}

        else:
            logger.error(f"Hugging Face API Error: {response.json()}")
            raise HTTPException(status_code=500, detail="Chatbot service error.")

    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        raise HTTPException(status_code=500, detail="Chatbot service error.")
