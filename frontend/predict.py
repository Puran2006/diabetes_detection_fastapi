import streamlit as st
import requests
import json
import profile
# API Endpoint
PREDICT_URL = "http://127.0.0.1:8000/predict"  # FastAPI predict endpoint
CHAT_API_URL = "http://127.0.0.1:8000/chat"

# Prediction Page
def predict():
    st.title("🔬 Diabetes Prediction")
    st.write("Enter your details to predict your diabetes risk.")
    
    # Input fields
    Pregnancies = st.number_input("Pregnancies", min_value=0, step=1)
    Glucose = st.number_input("Glucose", min_value=0.0, step=0.1)
    BloodPressure = st.number_input("Blood Pressure", min_value=0.0, step=0.1)
    Insulin = st.number_input("Insulin", min_value=0.0, step=0.1)
    BMI = st.number_input("BMI", min_value=0.0, step=0.1)
    DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, step=0.01)
    Age = st.number_input("Age", min_value=0, step=1)
    
    if st.button("Predict"):
        # Prepare JSON payload
        input_data = {
            "Pregnancies": Pregnancies,
            "Glucose": Glucose,
            "BloodPressure": BloodPressure,
            "Insulin": Insulin,
            "BMI": BMI,
            "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
            "Age": Age
        }
        
        # Get token from session
        token = st.session_state.get("token")
        if not token:
            st.error("⚠️ Please log in first!")
            return

        # Send request to FastAPI
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        response = requests.post(PREDICT_URL, headers=headers, data=json.dumps(input_data))
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"🩺 Prediction: {result['prediction']}")
            st.write(f"📊 Probability: {result['probability']}")
            st.info(result["message"])
            prediction = result['prediction']
            probability = result['probability']
            if prediction == "Diabetic" :
                # send message to the chatbot
                chatbot_message = {
                    "prediction": prediction,
                    "probability": probability,
                    "glucose": Glucose,
                    "blood_pressure": BloodPressure,
                    "insulin": Insulin,
                    "bmi": BMI,
                    "age": Age,
                    "diabetes_pedigree_function": DiabetesPedigreeFunction,
                }

                chat_response = requests.post(CHAT_API_URL, headers=headers, json=chatbot_message)

                if chat_response.status_code == 200:
                    bot_advice  = chat_response.json()
                    
                    # Display Chatbot Advice
                    st.subheader("💡 Health Recommendations")
                    advice_lines = bot_advice['advice'].split("\n")
                    for line in advice_lines:
                        st.write(f"✅ {line}")  # Add bullet points for readability
                else:
                    st.error("⚠️ Failed to get health advice from AI")
                    st.write("🔍 Debug Response:", chat_response.status_code, chat_response.text)
            
        else:
            st.error("❌ Prediction failed")
            st.write("🔍 Debug Response:", response.status_code, response.text)
    if st.button("➡️ Logout Here"):
        st.session_state.token = None  # Clear token
        st.session_state.page = "Login"  # Redirect to login
        st.rerun() 

