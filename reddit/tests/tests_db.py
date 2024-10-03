import random
from datetime import datetime, timedelta
import pytest
from reddit.db import Table

FORMAT = "%d.%m.%Y %H:%M"
DAYS = 3


def random_date() -> datetime:
    start = datetime.now().date()
    end = start + timedelta(days=1)
    date = start + (end - start) * random.random()
    return datetime(date.year, date.month, date.day)


def author_author() -> str:
    authors = ["author1", "author2", "author3", "author4", "author4"]
    return random.choice(authors)


@pytest.fixture
def full_table() -> Table:
    table = Table()
    for _ in range(500):
        table.add_row(author_author(), random_date(), random.randint(1, 100))
    return table


@pytest.fixture
def empty_table() -> Table:
    return Table()


@pytest.fixture
def date() -> datetime:
    delta = datetime.now().date() - timedelta(days=DAYS)
    return datetime(year=delta.year, month=delta.month, day=delta.day)


def test__add_row__check_row_count_more_0_after_inserting(empty_table: Table) -> None:
    empty_table.add_row(author_author(), random_date(), random.randint(1, 100))
    assert len(empty_table.raw_rows()) > 0


def test__rows_most_of_posts__check_count_of_post_less_than_before_handling(
    full_table: Table, date: datetime
) -> None:
    count_before = len(full_table.raw_rows())
    count_after = len(full_table.rows_most_of_posts(date))
    assert count_after <= count_before


def test__rows_most_of_posts__check_count_of_post_in_the_first_record_more_than_the_last(
    full_table: Table, date: datetime
) -> None:
    rows = full_table.rows_most_of_posts(date)
    first_record = rows[0]
    last_record = rows[len(rows) - 1]
    assert first_record[1] > last_record[1]


def test__rows_most_of_comments__check_count_of_comments_less_than_before_handling(
    full_table: Table, date: datetime
) -> None:
    count_before = len(full_table.raw_rows())
    count_after = len(full_table.rows_most_of_comments(date))
    assert count_after <= count_before


def test__rows_most_of_comments__check_count_of_comments_in_the_first_record_more_than_the_last(
    full_table: Table, date: datetime
) -> None:
    rows = full_table.rows_most_of_comments(date)
    first_record = rows[0]
    last_record = rows[len(rows) - 1]
    assert first_record[1] > last_record[1]
