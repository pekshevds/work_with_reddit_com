"""
Ваша задача – написать скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и выводит топ
пользователей, которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов.
Топ - это когда сверху тот, кто больше всех написал комментариев/постов, на втором месте следущий за ним и так далее."""

import requests
from datetime import datetime
from reddit.db import Table


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
    params = {"limit": "100"}

    full_names = []
    table = Table()
    for _ in range(5):
        response = requests.get(
            "https://oauth.reddit.com/r/programming/new", headers=headers, params=params
        )
        posts = response.json().get("data").get("children")
        for post in posts:
            data = post.get("data")
            fullname = f"{data.get("kind")}_{data.get("id")}"
            params["after"] = fullname
            if fullname not in full_names:
                table.add_row(
                    data.get("author"),
                    datetime.fromtimestamp(data.get("created_utc")).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                    data.get("num_comments"),
                )
                full_names.append(fullname)
    for item in enumerate(table.rows()):
        print(item)
