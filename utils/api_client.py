import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://jsonplaceholder.typicode.com"


class APIClient:
    """Base API client for JSONPlaceholder API."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        url = f"{BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        logger.info(f"GET {url} -> {response.status_code}")
        return response

    def post(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{BASE_URL}{endpoint}"
        response = self.session.post(url, json=payload)
        logger.info(f"POST {url} -> {response.status_code}")
        return response

    def put(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{BASE_URL}{endpoint}"
        response = self.session.put(url, json=payload)
        logger.info(f"PUT {url} -> {response.status_code}")
        return response

    def delete(self, endpoint: str) -> requests.Response:
        url = f"{BASE_URL}{endpoint}"
        response = self.session.delete(url)
        logger.info(f"DELETE {url} -> {response.status_code}")
        return response
