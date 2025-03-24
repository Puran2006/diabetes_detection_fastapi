# Use an official Python image as the base
FROM python:3.13.1-slim

# Set the working directory
WORKDIR /app

# Copy FastAPI and Streamlit requirements separately
COPY fastapi_app/requirements.txt ./fastapi_requirements.txt
COPY frontend/requirements.txt ./frontend_requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r fastapi_requirements.txt
RUN pip install --no-cache-dir -r frontend_requirements.txt

# Copy only necessary directories
COPY fastapi_app /app/fastapi_app
COPY frontend /app/frontend

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Start both FastAPI and Streamlit using a process manager (e.g., Supervisor)
CMD ["sh", "-c", "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]
