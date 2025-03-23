import streamlit as st
import requests
import predict  
import profile

# API Endpoints
LOGIN_URL = "http://127.0.0.1:8000/login"
REG_URL = "http://127.0.0.1:8000/register"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Login"  # Default page
if "token" not in st.session_state:
    st.session_state.token = None  # Store authentication token

# Function to change page
def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()  # Refresh UI to prevent overlap issue

st.sidebar.title("📌 Navigation")
if st.session_state.token:
    selected_page = st.sidebar.radio("Go to", ["Predict", "Profile", "Logout", "About"], index=["Predict", "Profile", "Logout", "About"].index(st.session_state.page))
else:
    selected_page = st.sidebar.radio("Go to", ["Login", "Register", "About"], index=["Login", "Register", "About"].index(st.session_state.page))

if selected_page != st.session_state.page:
    navigate(selected_page)

def login():
    st.title("🔑 Login Page")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        response = requests.post(
            LOGIN_URL,
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.success(f"✅ Welcome, {username}!")
            navigate("Predict")  # Redirect to prediction page
        else:
            st.write("🔍 Debug Response:", response.status_code, response.text)

    st.markdown("**Don't have an account?**")
    if st.button("➡️ Register Here"):
        navigate("Register")

def register():
    st.title("📝 Register Page")

    username = st.text_input("👤 Username")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Register"):
        response = requests.post(
            REG_URL,
            json={"username": username, "email": email, "password": password},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 201:
            st.success(f"✅ User {username} registered successfully!")
            st.info("You can now log in.")
        else:
            st.error("❌ Registration failed")
            st.write("🔍 Debug Response:", response.status_code, response.text)

    st.markdown("**Already have an account?**")
    if st.button("➡️ Login Here"):
        navigate("Login")

def logout():
    st.session_state.token = None  # Clear token
    st.session_state.page = "Login"  # Redirect to login page
    st.rerun()  #  Force UI refresh to remove old content

def about():
    st.title("ℹ️ About This App")
    
    st.write("""
        ## 🔬 **Diabetes Prediction App**
        Welcome to the **Diabetes Prediction App**, a user-friendly tool that helps assess your risk of diabetes using **Machine Learning (ML)**.

        ### 🚀 **Key Features**
        ✅ **Register & Log In** – Secure authentication using **JWT tokens**  
        ✅ **Diabetes Prediction** – Get a **personalized risk assessment** based on health parameters  
        ✅ **User Profile** – View past predictions and manage your account  
        ✅ **FastAPI Backend** – High-performance API for processing predictions  
        ✅ **Interactive Chatbot** (*Coming Soon*) – AI-powered assistant for health guidance  

        ### 🏗️ **How It Works**
        1️⃣ **Enter your health details** (Glucose, BMI, Blood Pressure, etc.)  
        2️⃣ **Submit the form** to the **AI-powered model**  
        3️⃣ **Receive instant predictions** with a probability score  

        ### 🧠 **Technology Stack**
        - 🐍 **Backend:** FastAPI (Python)  
        - 🎨 **Frontend:** Streamlit  
        - 🤖 **Machine Learning:** Scikit-learn Model  
        - 🔒 **Authentication:** JWT Tokens  

        ---
        ⚡ **Developed using FastAPI & Streamlit**  
        💡 *Empowering early diabetes detection through AI & technology!*  
    """)


# Handle page selection
if st.session_state.page == "Login":
    login()
elif st.session_state.page == "Register":
    register()
elif st.session_state.page == "Predict":
    predict.predict()
elif st.session_state.page == "Profile":
    profile.profile()
elif st.session_state.page == "Logout":
    logout()  # Calls the improved logout function
elif st.session_state.page == "About":
    about()
