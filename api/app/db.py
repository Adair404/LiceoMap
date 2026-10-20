from datetime import date, datetime, timedelta
from decimal import Decimal

import pymysql
import pymysql.cursors

from . import config


def get_db():
    conn = pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        yield conn
    finally:
        conn.close()


def _clean_value(value):
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        return f"{total // 3600:02d}:{total % 3600 // 60:02d}"
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def clean(row: dict | None) -> dict | None:
    if row is None:
        return None
    return {key: _clean_value(value) for key, value in row.items()}


def query(conn, sql: str, params: tuple = ()) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return [clean(row) for row in cur.fetchall()]


def query_one(conn, sql: str, params: tuple = ()) -> dict | None:
    rows = query(conn, sql, params)
    return rows[0] if rows else None
