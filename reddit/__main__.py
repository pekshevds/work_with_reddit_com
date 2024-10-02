"""
Ваша задача – написать скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и выводит топ пользователей,
которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов.
Топ - это когда сверху тот, кто больше всех написал комментариев/постов, на втором месте следущий за ним и так далее."""

import requests


def user_token() -> str:
    try:
        with open("token.txt", "r") as file:
            token = file.readline()
    except FileNotFoundError:
        token = ""
    return token


if __name__ == "__main__":
    TOKEN = user_token()
    if not TOKEN:
        raise ValueError("please, update token. python.exe -m reddit.token")
    headers = {"Authorization": f"bearer {TOKEN}"}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    print(response.json())
