import sqlite3
from datetime import datetime


class Table:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("file::memory:?cache=shared", uri=True)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS _table (author, created, num_comments)"
        )

    def __del__(self) -> None:
        self.connection.close()

    def add_row(self, author: str, created: datetime, num_comments: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO _table (author, created, num_comments) VALUES (?, ?, ?)",
            (
                author,
                created,
                num_comments,
            ),
        )

    def raw_rows(self) -> list[tuple[str, datetime, int]]:
        cursor = self.connection.cursor()
        return list(cursor.execute("SELECT * FROM _table"))

    def rows(self, created: datetime) -> list[tuple[str, int, int]]:
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

    def rows_most_of_comments(self, created: datetime) -> list[tuple[str, int]]:
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

    def rows_most_of_posts(self, created: datetime) -> list[tuple[str, int]]:
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
