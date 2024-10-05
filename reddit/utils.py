import requests
from datetime import datetime
from typing import Any, NamedTuple

type Post = dict[str, Any]


class PostData(NamedTuple):
    author: str
    created_utc: datetime
    num_comments: int


def data_request(token: str, after: str = "") -> dict[str, Any]:
    headers = {"Authorization": f"bearer {token}"}
    params = {"limit": "100"}
    if after:
        params["after"] = after
    response = requests.get(
        "https://oauth.reddit.com/r/programming/new", headers=headers, params=params
    )
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {}


def extract_posts(response: dict[str, Any]) -> list[Post]:
    data = response.get("data", {})
    return data.get("children", [])


def extract_post_data(post: dict[str, Any]) -> Post:
    return post.get("data", {})


def calculate_after(post_data: Post) -> str:
    return f"{post_data.get("kind", "")}_{post_data.get("id", "")}"


def extract_post_attributes(post_data: Post) -> PostData:
    return PostData(
        post_data.get("author", ""),
        datetime.fromtimestamp(post_data.get("created_utc", 0.0)),
        post_data.get("num_comments", 0),
    )
