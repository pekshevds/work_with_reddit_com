"""
Ваша задача – написать скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и выводит топ
пользователей, которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов.
Топ - это когда сверху тот, кто больше всех написал комментариев/постов, на втором месте следущий за ним и так далее."""

from datetime import datetime, timedelta
from reddit.db import Table, Post
from reddit.reddit_utils import RedditClient, RedditAuth
from reddit.settings import (
    read_reddit_connection_setting,
    read_reddit_connection_settings,
    RedditSettings,
)

AFTERS: list[str] = []
QUERY_COUNT: int = 5


def fill_table(
    table: Table, reddit_client: RedditClient, after: str, afters: list[str]
) -> None:
    # Дергаем порцию данных с reddit
    raw_posts = reddit_client.get_subreddit_new_posts(
        after=after, subreddit="programming"
    )
    for raw_post in raw_posts:
        if raw_post.id in afters:
            continue
        post = Post(
            author=raw_post.author,
            created=datetime.fromtimestamp(raw_post.created_utc),
            num_comments=raw_post.num_comments,
        )
        # Помещаем данные в сводную таблицу
        table.add(post)
        afters.append(raw_post.id)


def main() -> None:
    token = read_reddit_connection_setting(RedditSettings.TOKEN)
    if not token:
        raise ValueError("please, update token. python.exe -m reddit.token")
    after = ""
    # Сводная таблица
    table = Table()
    auth = RedditAuth(**read_reddit_connection_settings())
    reddit_client = RedditClient(auth)
    for _ in range(QUERY_COUNT):
        # Запоняем таблицу, на каждой итерации добавляем данные
        fill_table(table, reddit_client, after, AFTERS)

    # Расчет даты -3 дня
    delta = datetime.now().date() - timedelta(days=3)
    date = datetime(year=delta.year, month=delta.month, day=delta.day)

    print("raw")
    for item in enumerate(table.raw_posts()):
        print(item)

    print("comments")
    for item in enumerate(table.posts_most_of_comments(date)):
        print(item)

    print("posts")
    for item in enumerate(table.posts_most_of_posts(date)):
        print(item)


if __name__ == "__main__":
    main()
