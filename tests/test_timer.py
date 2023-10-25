import pytest
from app import TimerApp
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

import json
from unittest.mock import patch
from unittest.mock import MagicMock


# Ensure that the app is created only once
@pytest.fixture(scope="session")
def app():
    return QApplication([])

def test_start_pause_timer():
    window = TimerApp()
    window.show()

    # Start timer
    QTest.mouseClick(window.play_pause_button, Qt.LeftButton)
    assert window.running == True

    # Pause timer
    QTest.mouseClick(window.play_pause_button, Qt.LeftButton)
    assert window.running == False

    window.close()


def test_save_and_load_timer_state_paused(app, tmp_path):
    # Use tmp_path to create a temporary file for saving timer state
    file = tmp_path / "timer_state.json"
    
    window = TimerApp()
    window.running = False
    window.elapsed_seconds = 1500  # assume 25 minutes have passed
    window.timer_state_file = file  # Override the default path with the temp path

    window.save_timer_state()
    window.running = True
    window.elapsed_seconds = 0
    window.load_timer_state()

    assert window.running == False
    assert window.elapsed_seconds == 1500


def test_save_and_load_timer_state_elapsed(app, tmp_path):
    file = tmp_path / "timer_state.json"

    window = TimerApp()
    window.elapsed_seconds = 12345  # For the purpose of this test
    window.timer_state_file = file

    window.save_timer_state()  # Save the state
    window.elapsed_seconds = 0  # Reset the elapsed time

    window.load_timer_state()  # Load the state

    assert window.elapsed_seconds == 12345


def test_handle_exit_while_timer_running_no(app, tmp_path):
    file = tmp_path / "timer_state.json"

    window = TimerApp()
    window.running = True
    window.timer_state_file = file

    mock_close_event = MagicMock()  # Create a mock event

    # Mocking the QMessageBox to return 'No'
    with patch("PyQt5.QtWidgets.QMessageBox.question", return_value=QMessageBox.No):
        window.closeEvent(mock_close_event)

    mock_close_event.ignore.assert_called_once()  # Ensure the ignore method was called
    
    # File shouldn't exist as the state should not be saved if the user chooses not to exit
    assert not file.exists()


def test_handle_exit_while_timer_running_yes(app, tmp_path):
    file = tmp_path / "timer_state.json"

    window = TimerApp()
    window.elapsed_seconds = 12345  # For the purpose of this test
    window.timer_state_file = file

    mock_close_event = MagicMock()  # Create a mock event

    # Mocking the QMessageBox to return 'Yes'
    with patch("PyQt5.QtWidgets.QMessageBox.question", return_value=QMessageBox.Yes):
        window.closeEvent(mock_close_event)
    
    mock_close_event.accept.assert_called_once()  # Ensure the accept method was called
    
    with open(file, 'r') as f:
        data = json.load(f)
    
    assert data["elapsed_seconds"] == 12345