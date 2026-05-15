from fastapi import FastAPI

import requests
import uuid
import json

app = FastAPI()

# НАСТРОЙКИ 3X-UI

PANEL_URL = "http://144.31.121.80:47271"

USERNAME = "admin"

PASSWORD = "admin"

INBOUND_ID = 1

SERVER_IP = "144.31.121.80"

PUBLIC_KEY = "CaGyFVxHqqrjgpjLjFzGs-s97-Rw2K3BNa6U5dmYoX4"

SHORT_ID = "9c1a9e"

API_KEY = "super_secret_backend_key"


@app.post("/create_vpn")
def create_vpn(data: dict):

    key_name = data["key_name"]
    client_id = str(uuid.uuid4())
    session = requests.Session()

    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    login_response = session.post(
        f"{PANEL_URL}/login",
        data=login_data
    )

    if login_response.status_code != 200:

        return {
            "error": "Ошибка авторизации"
        }

    settings = {
        "clients": [
            {
                "id": client_id,
                "flow": "xtls-rprx-vision",
                "email": key_name,
                "limitIp": 0,
                "totalGB": 0,
                "expiryTime": 0,
                "enable": True,
                "tgId": "",
                "subId": ""
            }
        ]
    }

    payload = {
        "id": INBOUND_ID,
        "settings": json.dumps(settings)
    }

    response = session.post(
        f"{PANEL_URL}/panel/api/inbounds/addClient",
        data=payload
    )

    if response.status_code != 200:

        return {
            "error": "Ошибка создания клиента"
        }

    vless_link = (
        f"vless://{client_id}@{SERVER_IP}:443"
        f"?type=tcp"
        f"&encryption=none"
        f"&security=reality"
        f"&pbk={PUBLIC_KEY}"
        f"&fp=chrome"
        f"&sni=www.github.com"
        f"&sid={SHORT_ID}"
        f"&spx=%2F"
        f"&flow=xtls-rprx-vision"
        f"#{key_name}"
    )

    return {
        "vpn_key": vless_link,
        "client_id": client_id
    }


@app.delete("/delete_vpn/{client_id}")
def delete_vpn(client_id: str):

    session = requests.Session()

    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    session.post(
        f"{PANEL_URL}/login",
        data=login_data
    )

    delete_response = session.post(
        f"{PANEL_URL}/panel/api/inbounds/{INBOUND_ID}/delClient/{client_id}"
    )

    return delete_response.json()