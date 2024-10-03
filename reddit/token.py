import requests
from typing import Any
import reddit.config as config


def auth() -> dict[str, str]:
    return requests.auth.HTTPBasicAuth(config.CLIENT_ID, config.SECRET_TOKEN)


def data() -> dict[str, str]:
    return {
        "grant_type": "password",
        "username": config.USERNAME,
        "password": config.PASSWORD,
    }


def save_token(token) -> None:
    with open("token.txt", "w", encoding="utf-8") as file:
        file.write(token)


def read_token() -> str:
    try:
        with open("token.txt", "r") as file:
            token = file.readline()
    except FileNotFoundError:
        token = ""
    return token


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
    result = token_request(auth(), data())
    token = extract_token_from(result)
    if token:
        return token, True
    return token, False


if __name__ == "__main__":
    token, updated = update_user_token()
    if updated:
        save_token(token)
