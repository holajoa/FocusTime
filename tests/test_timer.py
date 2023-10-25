import pytest
from app import TimerApp
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

app = QApplication([])


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
