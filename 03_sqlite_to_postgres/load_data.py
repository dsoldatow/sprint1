import sqlite3
from contextlib import contextmanager

from dataclasses import dataclass

import psycopg2
from psycopg2.extras import DictCursor

from models import Data
from models import table_to_models
from sql_queries import sql_query_insert
from sql_queries import sql_query_select_all

PORTION_VALUE = 100


@contextmanager
def sqllite_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def postgres_context(dsl: dict):
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()


def format_values(value):
    if isinstance(value, str):
        value = value.replace("'", "''")
    if value is None:
        value = 'Null'
    else:
        value = f"'{value}'"
    return value


@dataclass
class PostgresSaver:
    dsl: dict

    def save_all_data(self, all_data: list[Data]):
        for data in all_data:
            all_values = []
            if data.data:
                columns = ",".join(data.data[0].__dict__.keys())
            for row in data.data:
                values = list(row.__dict__.values())
                values = map(format_values, values)

                values = ','.join(values)
                all_values.append(f'({values})')
            if all_values:

                values_len = len(all_values)
                portion_number = 0
                # Порционно добавляем
                while values_len:
                    values_to_insert = all_values[portion_number * PORTION_VALUE: (portion_number + 1) * PORTION_VALUE]
                    sql_query = sql_query_insert.format(
                        table=data.table, columns=columns,
                        values=','.join(values_to_insert))
                    with postgres_context(self.dsl) as conn:
                        conn.cursor().execute(sql_query)
                        conn.commit()
                    portion_number += 1
                    values_len -= len(values_to_insert)


@dataclass
class SQLiteLoader:
    sqllite_path: str

    def load_movies(self):
        all_data = []
        for table in table_to_models:
            sql_query = sql_query_select_all.format(table=table)
            model_class = table_to_models[table]
            with sqllite_context(self.sqllite_path) as conn:
                data = conn.cursor().execute(sql_query)
                all_models = [model_class.from_dict(dict(row)) for row in data]
            all_data.append(Data(table=table, data=all_models))
        return all_data


def load_from_sqlite(sqllite_path: str, pg_dsl: dict):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_dsl)
    sqlite_loader = SQLiteLoader(sqllite_path)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    load_from_sqlite('db.sqlite', dsl)
