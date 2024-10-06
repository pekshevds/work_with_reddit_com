from typing import Any
import random
from datetime import datetime, timedelta
import pytest
from reddit.db import Table, Post


@pytest.fixture
def make_date() -> Any:
    def inner() -> datetime:
        start = datetime.now().date()
        end = start + timedelta(days=1)
        date = start + (end - start) * random.random()
        return datetime(date.year, date.month, date.day)

    return inner


@pytest.fixture
def make_author() -> Any:
    def inner() -> str:
        authors = ["author1", "author2", "author3", "author4", "author4"]
        return random.choice(authors)

    return inner


@pytest.fixture
def post(make_date: Any, make_author: Any) -> Any:
    def inner() -> Post:
        return Post(
            author=make_author(),
            created=make_date(),
            num_comments=random.randint(1, 100),
        )

    return inner


@pytest.fixture
def full_table(post: Any) -> Table:
    table = Table()
    for _ in range(500):
        table.add(post())
    return table


@pytest.fixture
def empty_table() -> Table:
    return Table()


@pytest.fixture
def date() -> datetime:
    delta = datetime.now().date() - timedelta(days=3)
    return datetime(year=delta.year, month=delta.month, day=delta.day)


def test__add__check_that_new_posts_were_inserted_into_the_table(
    empty_table: Table, post: Any
) -> None:
    empty_table.add(post())
    empty_table.add(post())
    assert len(empty_table.raw_posts()) > 0


def test__posts_most_of_posts__check_that_the_table_of_posts_was_sorted_by_num_posts(
    full_table: Table, date: datetime
) -> None:
    rows = full_table.posts_most_of_posts(date)
    first_record = rows[0]
    last_record = rows[len(rows) - 1]
    assert first_record[1] > last_record[1]


def test__rows_most_of_comments___check_that_the_table_of_posts_was_sorted_by_num_comments(
    full_table: Table, date: datetime
) -> None:
    rows = full_table.posts_most_of_comments(date)
    first_record = rows[0]
    last_record = rows[len(rows) - 1]
    assert first_record[1] > last_record[1]
