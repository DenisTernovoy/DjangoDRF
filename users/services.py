import requests
from config import settings


def create_stripe_session(price: str):
    """Создает сессию страйп"""

    headers = {"Authorization": f"Bearer {settings.STRIPE_API_KEY}"}
    data = {
        "success_url": "http://127.0.0.1:8000/",
        "line_items[0][price]": price,
        "line_items[0][quantity]": 1,
        "mode": "payment",
    }
    response = requests.post(
        f"{settings.STRIPE_BASE_URL}/v1/checkout/sessions", headers=headers, data=data
    ).json()

    return response["url"], response["id"]


def create_stripe_price(
    amount: int,
    name: str = None,
) -> str:
    """Создает цену страйп"""

    headers = {"Authorization": f"Bearer {settings.STRIPE_API_KEY}"}
    data = {
        "currency": "rub",
        "unit_amount": amount * 100,
        "product_data[name]": name,
    }
    response = requests.post(
        f"{settings.STRIPE_BASE_URL}/v1/prices", headers=headers, data=data
    )

    return response.json()


def check_stripe_status(stripe_session_id: str) -> str:
    """Проверка статуса платежа страйп"""

    headers = {"Authorization": f"Bearer {settings.STRIPE_API_KEY}"}
    response = requests.get(
        f"{settings.STRIPE_BASE_URL}/v1/checkout/sessions/{stripe_session_id}",
        headers=headers,
    )

    return response.json()["status"]
