from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PyQt5.QtCore import QTimer, Qt, pyqtSlot
from PyQt5.QtGui import QFont

from components.buttons import PlayPauseButton
from utils.db_utils import save_to_db, fetch_last_session, fetch_from_db
from utils.app_settings import load_settings
from config import LOG_DIR

import time
import datetime
import threading
import logging

from typing import Optional


logger = logging.getLogger(__name__)


class TimerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.database = self.parent().config["database"]

        layout = QVBoxLayout(self)

        self.timer_label = QLabel("00:00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)

        # Initialize settings
        self.app_settings = load_settings()

        # Apply font settings to timer label
        self.apply_settings()

        # Timer setup
        self.timer_instance = QTimer(
            self,
        )
        self.timer_instance.timeout.connect(self.update_timer_display)

        # Play/Pause button setup
        self.play_pause_button = PlayPauseButton(self)
        layout.addWidget(self.play_pause_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # Initialize
        self.running = False                # Timer running state
        self.start_time = None              # Time when the timer was started
        self.elapsed_seconds = 0            # Total elapsed time
        self.session_start_time = None      # Time when the current session was started
        self.session_elapsed_seconds = 0    # Elapsed time of the current session

        # Load timer state from file
        self.load_last_session()

        # Start the daily reset checker
        self.daily_reset_thread = threading.Thread(target=self.check_daily_reset)
        self.daily_reset_thread.daemon = (
            True  # Allow the app to exit even if thread is running
        )
        self.daily_reset_thread.start()

        if self.last_used_datetime.date() < datetime.date.today():
            self.reset_timer()

    def apply_settings(self):
        font_name = self.app_settings.font_name
        font_size = int(self.app_settings.font_size)
        font = QFont(font_name, font_size)
        self.timer_label.setFont(font)
        logging.info(f"Font applied: {font_name}, {font_size}")

    def load_last_session(self):
        last_session = fetch_last_session(self.database)
        if last_session:
            logging.info(f"Last session found: {last_session}")
            self.last_used_datetime, _ = last_session
            self.elapsed_seconds = fetch_from_db(
                date=self.last_used_datetime.date(), database=self.database
            )
            logging.info(
                f"Last session loaded: {self.last_used_datetime}, {self.elapsed_seconds}"
            )
        else:
            self.last_used_datetime = datetime.datetime.now()
            self.elapsed_seconds = 0
            logging.info(
                f"Last session not found, new session created: {self.last_used_datetime}, {self.elapsed_seconds}"
            )

        self.update_timer_display(force_update=True)

    @pyqtSlot()
    def toggle_timer(self, on=None):
        turn_on = on if on is not None else not self.running
        
        if turn_on:
            if self.running:
                return
            # Starting the timer
            if self.start_time is None:
                self.start_time = time.time() - self.elapsed_seconds
            self.running = True
            self.session_start_time = datetime.datetime.now()
            self.play_pause_button.toggle_icon(isRunning=True)
            self.timer_instance.start(1000)
        else:
            if not self.running:
                return
            logger.debug(f"start_time: {self.start_time}, elapsed_seconds: {self.elapsed_seconds}")
            # Stopping the timer, we calculate the total elapsed time
            self.elapsed_seconds = int(time.time() - self.start_time)
            self.session_elapsed_seconds = (datetime.datetime.now() - self.session_start_time).seconds
            self.start_time = None  # Reset start_time
            self.session_start_time = None
            self.running = False
            self.play_pause_button.toggle_icon(isRunning=False)
            self.timer_instance.stop()
            self.update_timer_display(force_update=True)
            self.save_session_to_db(
                datetime_value=datetime.datetime.now()
                - datetime.timedelta(seconds=self.session_elapsed_seconds),
                duration_sec=self.session_elapsed_seconds,
            )

    def update_timer_display(self, force_update=False):
        if self.running:
            elapsed_time = time.time() - self.start_time
        elif force_update:
            elapsed_time = self.elapsed_seconds
        else:
            return
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.setText(
            "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        )

    def reset_timer(self):
        self.timer_label.setText("00:00:00")
        self.elapsed_seconds = 0

    def save_session_to_db(
        self,
        datetime_value: Optional[datetime.datetime] = None,
        duration_sec: Optional[int] = None,
    ):
        if not datetime_value:
            datetime_value = self.last_used_datetime
        if not duration_sec:
            duration_sec = self.elapsed_seconds
        save_to_db(datetime_value, duration_sec, self.database)
        logging.info(f"Session saved: {datetime_value}, {duration_sec}")

    def perform_daily_reset(self):
        """Perform the daily save and reset operations."""
        running_state = self.running        # Save the running state
        self.toggle_timer(on=False)         # Pause the timer to save current session
        self.reset_timer()
        self.check_daily_reset()
        logging.info(
            f"Daily reset performed. Previous session saved: {self.last_used_datetime}, {self.session_elapsed_seconds}"
        )
        if running_state:                        # If the timer was running, resume it       
            self.toggle_timer(on=True)

    def check_daily_reset(self):
        now = datetime.datetime.now()
        # Calculate the time remaining until midnight
        midnight = now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
        delta_t = midnight - now
        seconds_to_midnight = delta_t.total_seconds()
        logging.info(f"{seconds_to_midnight} before midnight reset")

        # Set a timer to call the reset function at midnight
        threading.Timer(seconds_to_midnight, self.perform_daily_reset).start()

    def on_exit_app(self):
        if self.running:
            self.toggle_timer()  # Pause the timer
