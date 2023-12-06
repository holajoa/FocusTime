import sqlite3
import datetime
from config import TIME_DATABASE
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def initialize_db(database: Optional[str] = TIME_DATABASE):
    """Create the database if it doesn't exist"""
    import os

    if not database == TIME_DATABASE:
        logging.warning(
            f"Not using default database: {TIME_DATABASE}, initializing {database} instead. Ignore if testing."
        )
    if not os.path.exists(database):
        open(database, "w").close()

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS daily_times
           (id INTEGER PRIMARY KEY AUTOINCREMENT, 
           datetime TEXT NOT NULL, 
           DurationSec INTEGER NOT NULL)"""
    )
    conn.commit()
    conn.close()


def save_to_db(
    datetime_value: datetime.datetime,
    duration_sec: int,
    database: Optional[str] = TIME_DATABASE,
):
    """Save the elapsed time to the database."""
    if not database == TIME_DATABASE:
        logging.warning(
            f"Not using default database: {TIME_DATABASE}, saving to {database} instead. Ignore if testing."
        )
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO daily_times (datetime, DurationSec) VALUES (?, ?)",
        (datetime_value, duration_sec),
    )
    conn.commit()
    conn.close()


def fetch_from_db(date: datetime.date, database: Optional[str] = TIME_DATABASE) -> int:
    """Fetch the elapsed time for a given date from the database."""
    if not database == TIME_DATABASE:
        logging.warning(
            f"Not using default database: {TIME_DATABASE}, loading from {database} instead. Ignore if testing."
        )
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT SUM(DurationSec) FROM daily_times WHERE DATE(datetime) = ?"

    cursor.execute(query, (date,))
    duration_sec = cursor.fetchone()[0]
    conn.close()
    return duration_sec if duration_sec is not None else 0


def fetch_last_session(
    database: Optional[str] = TIME_DATABASE,
) -> Optional[Tuple[datetime.datetime, int]]:
    """Fetch the last used datetime and elapsed time from the database."""
    if not database == TIME_DATABASE:
        logging.warning(
            f"Not using default database: {TIME_DATABASE}, loading from {database} instead. Ignore if testing."
        )
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT datetime, DurationSec FROM daily_times ORDER BY datetime DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        # Assuming the database stores datetime in ISO format
        last_used_datetime = datetime.datetime.fromisoformat(row[0])
        elapsed_seconds = row[1]
        return last_used_datetime, elapsed_seconds
    else:
        return None
