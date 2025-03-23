from fastapi import FastAPI, status
import uvicorn
from routes import diabetes, auth, users
from database import engine, Base


app = FastAPI(
    title="Diabetes Prediction API",
    description="A FastAPI-powered Machine Learning API for Diabetes Prediction",
    version="1.0.0"
)


# Create tables in the database
Base.metadata.create_all(bind=engine)


# Registering our Diabetes router
app.include_router(diabetes.router, tags=["Diabetes Prediction"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Diabetes Prediction API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
