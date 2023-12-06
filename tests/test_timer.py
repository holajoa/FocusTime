import pytest

from app import TimerApp

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent

from utils.db_utils import initialize_db

import json


class MockCloseEvent(QCloseEvent):
    pass

# Ensure that the app is created only once
@pytest.fixture(scope="session")
def app():
    return QApplication([])


def test_start_pause_timer():
    window = TimerApp()
    window.show()

    # Start timer
    QTest.mouseClick(window.timer_view.play_pause_button, Qt.LeftButton)
    assert window.running == True

    # Pause timer
    QTest.mouseClick(window.timer_view.play_pause_button, Qt.LeftButton)
    assert window.running == False

    window.close()


def test_save_and_load_timer_state_paused(app, tmp_path):
    # Use tmp_path to create a temporary file for saving timer state
    file = tmp_path / "timer_data.db"
    window = TimerApp(config={"database": file})
    
    window.timer_view.running = False
    window.timer_view.elapsed_seconds = 1500  # assume 25 minutes have passed

    window.timer_view.save_session_to_db()  # Save the state
    window.timer_view.elapsed_seconds = 0
    window.timer_view.load_last_session()  # Load the state

    assert window.timer_view.running == False
    assert window.timer_view.elapsed_seconds == 1500


def test_save_and_load_timer_state_elapsed(app, tmp_path):
    file = tmp_path / "timer_data.db"
    window = TimerApp(config={"database": file})

    window.timer_view.elapsed_seconds = 12345  # For the purpose of this test

    window.timer_view.save_session_to_db()  # Save the state
    window.timer_view.elapsed_seconds = 0  # Reset the elapsed time

    window.timer_view.load_last_session()  # Load the state

    assert window.timer_view.elapsed_seconds == 12345