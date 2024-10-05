import requests
from typing import Any
from dotenv import load_dotenv, set_key
from os import environ

DOTENV_PATH = "reddit/.env"
load_dotenv(DOTENV_PATH)


def get_auth() -> dict[str, str]:
    return requests.auth.HTTPBasicAuth(
        environ.get("CLIENT_ID", ""), environ.get("SECRET_TOKEN", "")
    )


def get_data() -> dict[str, str]:
    return {
        "grant_type": "password",
        "username": environ.get("USERNAME", ""),
        "password": environ.get("PASSWORD", ""),
    }


def save_token(token: str) -> None:
    set_key(DOTENV_PATH, "TOKEN", token)


def read_token() -> str:
    return environ.get("TOKEN", "")


def extract_token_from(result: dict[str, Any]) -> str:
    return result.get("access_token", "")


def token_request(auth: dict[str, str], data: dict[str, str]) -> dict[str, Any]:
    headers = {"User-Agent": "MyBot/0.0.1"}
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )
    return res.json()


def update_user_token() -> tuple[str, bool]:
    result = token_request(get_auth(), get_data())
    token = extract_token_from(result)
    if token:
        return token, True
    return token, False


if __name__ == "__main__":
    token, updated = update_user_token()
    if updated:
        save_token(token)
