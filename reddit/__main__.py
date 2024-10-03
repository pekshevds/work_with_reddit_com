"""
Ваша задача – написать скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и выводит топ
пользователей, которые написали больше всего комментариев и топ пользователей, которые написали больше всего постов.
Топ - это когда сверху тот, кто больше всех написал комментариев/постов, на втором месте следущий за ним и так далее."""

from datetime import datetime, timedelta
from reddit.db import Table
from reddit.token import read_token
from reddit.utils import (
    data_request,
    extract_posts,
    extract_post_data,
    extract_full_name,
    extract_post_attributes,
)

FULL_NAMES: list[str] = []


def fill_table(table: Table, token: str, after) -> None:
    full_name = ""
    # Дергаем порцию данных с reddit
    response = data_request(token, after)
    # Извлекаем посты из выборки данных
    posts = extract_posts(response)
    for post in posts:
        # Извлекаем основные (не технические) данные поста
        post_data = extract_post_data(post)
        # Извлекаем и рассчитываем полное уникальное имя поста
        full_name = extract_full_name(post_data)
        if full_name in FULL_NAMES:
            continue
        # Извлекаем атрибуты поста для анализа
        post_attr = extract_post_attributes(post_data)
        # Помещаем данные в сводную таблицу
        table.add_row(post_attr.author, post_attr.created_utc, post_attr.num_comments)
        FULL_NAMES.append(full_name)


if __name__ == "__main__":
    # Получаем токен
    TOKEN = read_token()
    if not TOKEN:
        raise ValueError("please, update token. python.exe -m reddit.token")
    FULL_NAMES = []
    QUERY_COUNT = 5
    full_name = ""
    # Сводная таблица
    table = Table()
    for _ in range(QUERY_COUNT):
        # Запоняем таблицу, на каждой итерации добавляем данные
        fill_table(table, TOKEN, full_name)

    # Расчет даты -3 дня
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
