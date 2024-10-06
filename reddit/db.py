import sqlite3
from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    author: str
    created: datetime
    num_comments: int


class Table:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("file::memory:?cache=shared", uri=True)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS _table (author, created, num_comments)"
        )

    def __del__(self) -> None:
        self.connection.close()

    def add(self, post: Post) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO _table (author, created, num_comments) VALUES (?, ?, ?)",
            (
                post.author,
                post.created,
                post.num_comments,
            ),
        )

    def raw_posts(self) -> list[Post]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM _table")
        return [
            Post(author=post[0], created=post[1], num_comments=post[2])
            for post in cursor.fetchall()
        ]

    def posts(self, created: datetime) -> list[tuple[str, int, int]]:
        cursor = self.connection.cursor()
        return list(
            cursor.execute(
                """
                SELECT
                    author, COUNT(created) AS num_posts, SUM(num_comments) AS num_comments
                FROM _table
                WHERE
                    created >= ?
                GROUP BY
                    author
                ORDER BY
                    num_comments DESC, num_posts DESC
                """,
                (created,),
            )
        )

    def posts_most_of_comments(self, created: datetime) -> list[tuple[str, int]]:
        cursor = self.connection.cursor()
        return list(
            cursor.execute(
                """
                SELECT
                    author, SUM(num_comments) AS num_comments
                FROM _table
                WHERE
                    created >= ?
                GROUP BY
                    author
                ORDER BY
                    num_comments DESC
                """,
                (created,),
            )
        )

    def posts_most_of_posts(self, created: datetime) -> list[tuple[str, int]]:
        cursor = self.connection.cursor()
        return list(
            cursor.execute(
                """
                SELECT
                    author, COUNT(created) AS num_posts
                FROM _table
                WHERE
                    created >= ?
                GROUP BY
                    author
                ORDER BY
                    num_posts DESC
                """,
                (created,),
            )
        )
