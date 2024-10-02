import requests
import config


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


def update_user_token() -> bool:
    headers = {"User-Agent": "MyBot/0.0.1"}
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth(),
        data=data(),
        headers=headers,
    )
    token = res.json().get("access_token", "")
    if not token:
        return False
    save_token(token)
    return True


if __name__ == "__main__":
    update_user_token()
