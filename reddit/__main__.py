"""
Ваша задача – написать скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и выводит топ
пользователей, которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов.
Топ - это когда сверху тот, кто больше всех написал комментариев/постов, на втором месте следущий за ним и так далее."""

import requests
from typing import Any, NamedTuple
from datetime import datetime, timedelta
from reddit.db import Table
from reddit.token import read_token


class PostData(NamedTuple):
    author: str
    created_utc: datetime
    num_comments: int


def data_request(headers: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(
        "https://oauth.reddit.com/r/programming/new", headers=headers, params=params
    )
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {}


def extract_posts(response: dict[str, Any]) -> list[dict[str, Any]]:
    data = response.get("data", {})
    return data.get("children", [])


def extract_post_attributes(post: dict[str, Any]) -> PostData:
    return PostData(
        post.get("author", ""),
        datetime.fromtimestamp(post.get("created_utc", 0.0)),
        post.get("num_comments", 0),
    )


if __name__ == "__main__":
    TOKEN = read_token()
    if not TOKEN:
        raise ValueError("please, update token. python.exe -m reddit.token")
    headers = {"Authorization": f"bearer {TOKEN}"}
    params = {"limit": "100"}

    full_names = []
    table = Table()
    for _ in range(5):
        response = data_request(headers, params)
        posts = extract_posts(response)
        for post in posts:
            post_data = post.get("data", {})
            full_name = f"{post_data.get("kind")}_{post_data.get("id")}"
            params["after"] = full_name
            if full_name not in full_names:
                post_attr = extract_post_attributes(post_data)
                table.add_row(
                    post_attr.author, post_attr.created_utc, post_attr.num_comments
                )
                full_names.append(full_name)

    delta = datetime.now().date() - timedelta(days=3)
    date = datetime(year=delta.year, month=delta.month, day=delta.day)

    print("raw")
    for item in enumerate(table.raw_rows()):
        print(item)

    print("comments")
    for item in enumerate(table.rows_most_of_comments(date)):
        print(item)

    print("posts")
    for item in enumerate(table.rows_most_of_posts(date)):
        print(item)
