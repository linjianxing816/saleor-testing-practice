import os

import requests
from dotenv import load_dotenv

load_dotenv()


class SaleorClient:
    def __init__(self):
        self.url = os.getenv("SALEOR_API_URL")

    def graphql(self, query, variables=None, token=None):
        payload = {
            "query": query,
            "variables": variables or {}
        }

        headers = {
            "Content-Type": "application/json"
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.post(
            self.url,
            json=payload,
            headers=headers,
            timeout=20
        )

        return response