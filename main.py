import os
import requests
import json
import random

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

NOTION_BEARER_TOKEN = os.environ.get("NOTION_BEARER_TOKEN")

# https://findigs.postman.co/workspace/KWG-Oura-Data~af608085-a79b-4e23-9e5a-b9da08700c83/overview
OURA_API_TOKEN = os.environ.get("OURA_API_TOKEN")
OURA_BASE_URL = os.environ.get("OURA_BASE_URL")
OURA_CLIENT_ID = os.environ.get("OURA_CLIENT_ID")
OURA_CLIENT_SECRET = os.environ.get("OURA_CLIENT_SECRET")
MY_CLIENT_VERIFICATION_TOKEN = os.environ.get("MY_CLIENT_VERIFICATION_TOKEN")


DATABASE_ID = "01f5145b31654dcbb56b7c7d9c20bea4" # TODO update to CENTCOM

_headers = {
    "Authorization": f"Bearer {NOTION_BEARER_TOKEN}",
    "Notion-Version": "2022-06-28",
}

TARGET_LIST = [
    "Responsible",
    "Accountable",
    "Consulted",
    "Informed",
]

app = FastAPI()


# Endpoint to handle the verification step
@app.get("/webhook/")
async def verify_webhook(request: Request):
    verification_token = request.query_params.get("verification_token")
    challenge = request.query_params.get("challenge")
    if not verification_token or not challenge:
        raise HTTPException(status_code=400,
                            detail="Missing verification parameters")

    # Verify the verification_token (you can add your verification logic here)
    # For simplicity, let's assume the verification is successful
    # You may want to replace this with your actual verification logic
    if verification_token != MY_CLIENT_VERIFICATION_TOKEN:
        raise HTTPException(status_code=403,
                            detail="Invalid verification token")

    return JSONResponse(content={"challenge": challenge})


# Endpoint to handle incoming webhook data
@app.post("/webhook/")
async def webhook_endpoint(request: Request):
    data = await request.json()
    # Process your data here (e.g., log it, trigger other actions, etc.)
    print(data)  # Example action: print data to console
    return JSONResponse(status_code=200, content={"message": "Data received"})


# Example of how to create a webhook subscription
def create_webhook_subscription(callback_url):
    url = "https://cloud.ouraring.com/v2/webhook/subscription"
    headers = {
        "x-client-id": "your_client_id",
        "x-client-secret": "your_client_secret",
        "Content-Type": "application/json"
    }
    payload = {
        "callback_url": callback_url
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Webhook subscription created successfully")
    else:
        print("Failed to create webhook subscription:", response.text)




def get_db_data():
    response = requests.get(
        f'https://api.notion.com/v1/databases/{DATABASE_ID}',
        headers=_headers
    )
    return response.json()

def update_db_properties(payload):
    response = requests.patch(
        f'https://api.notion.com/v1/databases/{DATABASE_ID}',
        headers=_headers,
        json=payload
    )
    return response.json()



# if __name__ == '__main__':
#     # Example usage: create a webhook subscription
#     create_webhook_subscription("https://yourdomain.com/webhook/")
