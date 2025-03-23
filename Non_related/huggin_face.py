

import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": "Bearer <your_hugginface_api_access_token>"}


def chat_with_model(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

# Example usage
user_input = "What are some ways to manage diabetes?"
response = chat_with_model(user_input)
print(response)

