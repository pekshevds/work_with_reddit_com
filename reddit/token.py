from reddit.reddit_utils import RedditAuth
from reddit.settings import (
    read_reddit_connection_settings,
    save_reddit_connection_setting,
    RedditSettings,
)


if __name__ == "__main__":
    settings = read_reddit_connection_settings()
    auth = RedditAuth(
        client_id=settings.get("CLIENT_ID", ""),
        secret_token=settings.get("SECRET_TOKEN", ""),
        username=settings.get("USERNAME", ""),
        password=settings.get("PASSWORD", ""),
    )
    auth.update_token()
    if auth.token:
        save_reddit_connection_setting(RedditSettings.TOKEN, auth.token)
