"""Test the history view and the history functionality."""
import pytest

from app import TimerApp
from views.history import DateLabel
from utils.db_utils import fetch_from_db

from PyQt5.QtWidgets import QApplication, QToolTip
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QPoint

import datetime

app = QApplication([])


def test_save_elapsed_time_at_midnight(mocker):
    window = TimerApp()

    # Mock the current time to a second before midnight
    mocker.patch("datetime.datetime")
    datetime.datetime.now.return_value = datetime.datetime(2023, 10, 24, 23, 59, 59)

    # Set a timer duration for testing purposes
    elapsed_seconds = 3600  # 1 hour
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    window.timer_view.timer_label.setText(
        "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    )

    # Trigger the function that should save the time at midnight
    window.timer_view.perform_daily_reset()

    # Fetch data for today
    today = datetime.date.today().strftime("%Y-%m-%d")
    saved_time = fetch_from_db(today)

    assert saved_time[0] == "01:00:00"

    window.close()


def test_history_view_and_calendar():
    window = TimerApp()
    window.show()

    # Open history view
    window.show_history_view()
    assert window.history_view.isVisible()

    # Simulate hovering over a date label
    test_day = 5
    current_date = datetime.date.today()
    test_date = datetime.date(current_date.year, current_date.month, test_day).strftime(
        "%Y-%m-%d"
    )
    date_label = window.history_view.findChild(DateLabel, f"DateLabel({test_date})")
    assert date_label is not None

    # Move the mouse cursor to the center of the date label
    QTest.mouseMove(
        date_label, QPoint(date_label.width() // 2, date_label.height() // 2)
    )

    # Check the content of the tooltip - PyQt doesn't provide direct functions to check tooltip content.
    # This assumes that fetch_from_db() returns a value for the date you're testing.
    elapsed_time = fetch_from_db(
        test_date
    )  # replace with the date string for the label you're hovering over
    if elapsed_time:
        expected_tooltip = elapsed_time[0]
    else:
        expected_tooltip = ""
    assert QToolTip.text() == expected_tooltip

    window.close()
