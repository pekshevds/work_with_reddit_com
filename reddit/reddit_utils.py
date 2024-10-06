import httpx
from typing import Any
from pydantic import BaseModel

type Json = dict[str, Any]


class Post(BaseModel):
    id: str
    author: str
    created_utc: float
    num_comments: int
    kind: str = ""

    @property
    def after(self) -> str:
        return f"{self.kind}_{self.id}"


class RedditAuth:
    def __init__(
        self,
        client_id: str,
        secret_token: str,
        username: str,
        password: str,
        token: str = "",
        base_url: str = "https://www.reddit.com",
    ) -> None:
        self.client_id = client_id
        self.secret_token = secret_token
        self.username = username
        self.password = password
        self.token = token
        self.base_url = base_url

    @property
    def client(self) -> httpx.Client:
        auth = httpx.BasicAuth(username=self.client_id, password=self.secret_token)
        return httpx.Client(auth=auth)

    def update_token(self) -> None:
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }
        headers = {
            "User-Agent": "PostmanRuntime/7.41.2",
            "Content-Type": "application/json",
        }
        response = self.client.post(
            f"{self.base_url}/api/v1/access_token",
            data=data,
            headers=headers,
        )
        response.raise_for_status()
        self.token = response.json().get("access_token", "")


class RedditClient:
    def __init__(
        self, auth: RedditAuth, base_url: str = "https://oauth.reddit.com"
    ) -> None:
        self.headers = {"Authorization": f"bearer {auth.token}"}
        self.base_url = base_url

    def get_subreddit_new_posts(self, subreddit: str, after: str = "") -> list[Post]:
        params = {"limit": "100"}
        if after:
            params["after"] = after
        url = f"{self.base_url}/r/{subreddit}/new"

        response = httpx.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json().get("data")
        if not data:
            return []

        posts = data.get("children")
        return [Post(**post.get("data")) for post in posts]
