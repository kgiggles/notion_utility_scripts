import os
import requests
import json
import random

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

NOTION_BEARER_TOKEN = os.environ.get("NOTION_BEARER_TOKEN")

# https://findigs.postman.co/workspace/KWG-Oura-Data~af608085-a79b-4e23-9e5a-b9da08700c83/overview
OURA_API_TOKEN = os.environ.get("OURA_API_TOKEN")
OURA_BASE_URL = os.environ.get("OURA_BASE_URL")
OURA_CLIENT_ID = os.environ.get("OURA_CLIENT_ID")
OURA_CLIENT_SECRET = os.environ.get("OURA_CLIENT_SECRET")


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


@app.post("/webhook/")
async def webhook_endpoint(request: Request):
    data = await request.json()
    # Process your data here (e.g., log it, trigger other actions, etc.)
    print(data)  # Example action: print data to console
    return JSONResponse(status_code=200, content={"message": "Data received"})
    # TODO need to validate wh subscription: https://cloud.ouraring.com/v2/docs#section/Setup


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



if __name__ == '__main__':
    pass
