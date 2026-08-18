import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


def search_documents(
    query,
    limit,
    min_score,
    category=None,
    source=None,
    page=1,
):
    payload = {
        "query": query,
        "limit": limit,
        "min_score": min_score,
        "offset": (page - 1) * limit,
    }

    if category:
        payload["category"] = category

    if source:
        payload["source"] = source

    response = requests.post(
        f"{API_URL}/documents/search",
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def add_document(
    content,
    category,
    source,
):
    data = {
        "content": content,
        "category": category,
        "source": source,
    }

    response = requests.post(
        f"{API_URL}/documents/",
        json=data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()