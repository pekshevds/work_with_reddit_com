from enum import Enum
from dotenv import load_dotenv, set_key
from os import environ

DOTENV_PATH = "reddit/.env"
load_dotenv(DOTENV_PATH)


class RedditSettings(Enum):
    CLIENT_ID = "CLIENT_ID"
    SECRET_TOKEN = "SECRET_TOKEN"
    USERNAME = "USERNAME"
    PASSWORD = "PASSWORD"
    TOKEN = "TOKEN"


def save_reddit_connection_setting(setting: RedditSettings, value: str) -> None:
    set_key(DOTENV_PATH, setting.value, value)


def save_settings(
    client_id: str, secret_token: str, username: str, password: str, token: str
) -> None:
    save_reddit_connection_setting(RedditSettings.CLIENT_ID, client_id)
    save_reddit_connection_setting(RedditSettings.SECRET_TOKEN, secret_token)
    save_reddit_connection_setting(RedditSettings.USERNAME, username)
    save_reddit_connection_setting(RedditSettings.PASSWORD, password)
    save_reddit_connection_setting(RedditSettings.TOKEN, token)


def read_reddit_connection_setting(setting: RedditSettings) -> str:
    return environ.get(setting.value, "")


def read_reddit_connection_settings() -> dict[str, str]:
    return {
        "client_id": environ.get("CLIENT_ID", ""),
        "secret_token": environ.get("SECRET_TOKEN", ""),
        "username": environ.get("USERNAME", ""),
        "password": environ.get("PASSWORD", ""),
        "token": environ.get("TOKEN", ""),
    }
