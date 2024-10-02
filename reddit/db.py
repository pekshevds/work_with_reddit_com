import sqlite3
from datetime import datetime


class Table:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("file::memory:?cache=shared", uri=True)
        self.connection.execute("CREATE TABLE _table (author, created, num_comments)")

    def add_row(self, author: str, created: datetime, num_comments: int) -> None:
        self.connection.execute(
            f"INSERT INTO _table (author, created, num_comments) VALUES ({author}, {created}, {num_comments})"
        )

    def rows(self) -> list[dict[str, datetime, int]]:
        return list(self.connection.execute("SELECT * FROM _table"))
