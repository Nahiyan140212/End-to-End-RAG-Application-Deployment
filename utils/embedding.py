# Using requests library for embeddings
import requests
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()


EURI_API_KEY = os.getenv("EURI_API_KEY")


def get_embedding(text, model="text-embedding-3-small"):
    url = "https://api.euron.one/api/v1/euri/alpha/embeddings"
    headers = {
        "Authorization": f"Bearer {EURI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "model": model
    }
    response = requests.post(url, headers=headers, json=payload)
    return np.array(response.json()['data'][0]['embedding'])
