# Diabetes Detection System

## 📌 Project Overview
This project is a **Diabetes Detection System** that includes a **FastAPI backend**, a **Streamlit frontend**, and a **machine learning model** for diabetes prediction. The system predicts diabetes risk based on user input and provides health recommendations using AI.

## 📂 Project Structure
```
/diabetes_detection
|-- fastapi_app
    │── models/
        ├── user.py # User table schema
    │── routers/
        ├── auth.py # Authentication routes
        ├── diabetes.py # Diabetes prediction and AI advice
        ├── users.py # User management
    │── schemas/
        ├── diabetes.py # Diabetes data schema
        ├── user.py # User data schema
    │── database.py # Database connection
    │── database_model.pkl # Pickle model for predictions
    │── database.db # SQLite database (must be created manually)
    │── utils.py # Utility functions
    │── main.py # FastAPI entry point
    │── app.log # Logging file (must be created manually)
    │── secret_key.py # Generates JWT secret key
    │── requirements.txt # Backend dependencies
│── frontend
    ├── app.py # Streamlit main app
    ├── predict.py # Diabetes prediction page
    ├── profile.py # User profile page
    │── requirements.txt # Frontend dependencies
│── model_preparation
    ├── diabetes-detection.ipynb # Model training
    ├── diabetes.csv # Dataset
│── saved_models
    │── diabetes_model.pkl # Trained model
│── requirements.txt # Full project dependencies (Backend, Frontend, ML)
│─ venv/ # Virtual environment (optional)
```

## 🛠️ Setup Instructions
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your_username/diabetes_detection.git
cd diabetes_detection
```

### **2️⃣ Create and Activate Virtual Environment**
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Mac/Linux)
venv\Scripts\activate  # Activate (Windows)
```

### **3️⃣ Install Dependencies**
This project has separate dependencies for **FastAPI**, **Streamlit frontend**, and **ML model preparation**.

#### **👉 Install Backend (FastAPI) Dependencies**
```bash
cd fastapi_app
pip install -r requirements.txt
```

#### **👉 Install Frontend (Streamlit) Dependencies**
```bash
cd ../frontend
pip install -r requirements.txt
```

#### **👉 Install All Dependencies (Backend + Frontend + ML Model)**
```bash
cd ..  # Go back to project root
pip install -r requirements.txt
```

### **4️⃣ Create Required Files**
Manually create the following files before running the project:
for windows
```cmd
cd fastapi_app
echo. > app.log
echo. > database.db
```
for mac/linux
```bash
touch fastapi_app/app.log  # Log file for backend
touch fastapi_app/database.db  # SQLite database file
```


### **5️⃣ Set Up Secret Keys**
#### **👉 Generate JWT Secret Key**
Run the following command to generate a secret key for authentication:
```bash
cd fastapi_app
python secret_key.py
```
Copy the generated key and add it to `utils.py` in **FastAPI**:
```python
SECRET_KEY = "your_generated_secret_key_here"
```

#### **👉 Add Hugging Face API Token**
Inside `fastapi_app/routers/diabetes.py`, set your **Hugging Face API token** for AI-generated health advice:
```python
HF_API_TOKEN = "your_huggingface_api_token_here"
```

## 🚀 Running the Project
### **1️⃣ Start FastAPI Backend**
```bash
cd fastapi_app
uvicorn main:app --reload
```
FastAPI will run on `http://127.0.0.1:8000`

### **2️⃣ Start Streamlit Frontend**
```bash
cd ../frontend
streamlit run app.py
```
The frontend will be available in your browser.

## 🔑 Authentication
This system uses **JWT-based authentication**. Users must log in to obtain a token and use protected endpoints.

## ✅ API Endpoints
### **User Authentication**
- `POST /register` - Register a new user
- `POST /login` - Log in to get a token

### **Diabetes Prediction**
- `POST /predict` - Predict diabetes risk
- `GET /chat` - Get AI health advice

### **Profile Management**
- `GET /users/profile` - View profile
- `PUT /users/update` - Update profile
- `PUT /users/update-password` - Change password
- `DELETE /users/delete` - Delete profile

## ⚠️ Notes
- Ensure `database.db` and `app.log` are created before running FastAPI.
- Keep your `SECRET_KEY` and `HF_API_TOKEN` confidential.
- Install dependencies separately if needed (`fastapi_app`, `frontend`).
- Or Generate `requirements.txt` for all, 
 ```bash
pip install -r requirements.txt
```
run this in the folder diabetes_detection_fastapi/

## 🎯 Future Enhancements
- Improve AI-generated health recommendations.
- Deploy to a cloud server.

---
Developed with ❤️ for Diabetes Detection 🚀

