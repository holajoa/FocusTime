import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMenu, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from views.history import HistoryFrame
from views.settings import SettingsFrame
from app_settings import load_settings
from db_utils import save_to_db

from config import TIMER_STATE

import datetime
import time
import threading
import json


class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Basic window settings
        self.setWindowTitle("Daily Timer")
        self.setGeometry(100, 100, 400, 300)
        
        # Initialize settings
        self.app_settings = load_settings()
        self.timer_state_file = TIMER_STATE

        # Menu bar setup
        menubar = self.menuBar()
        fileMenu = QMenu('Menu', self)
        historyAction = fileMenu.addAction('Show History')
        settingsAction = fileMenu.addAction('Settings')
        menubar.addMenu(fileMenu)

        # Connect menu actions to respective slots
        historyAction.triggered.connect(self.show_history_view)
        settingsAction.triggered.connect(self.show_settings_view)
        
        # Create a stacked widget to manage different views
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        # Timer Frame (we use a QWidget with a layout)
        self.timer_widget = QWidget(self)
        layout = QVBoxLayout()

        self.timer_string = "00:00:00"
        self.timer_label = QLabel(self.timer_string, self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.apply_settings()    # Apply font settings to timer label
        layout.addWidget(self.timer_label)
        
        self.play_pause_button = QPushButton("▶", self, )
        layout.addWidget(self.play_pause_button)
        self.play_pause_button.clicked.connect(self.toggle_timer)
        
        self.timer_widget.setLayout(layout)
        self.central_widget.addWidget(self.timer_widget)  # Add to stacked widget

        # History and Settings Frame
        self.history_frame = HistoryFrame(self)
        self.central_widget.addWidget(self.history_frame)

        self.settings_frame = SettingsFrame(self)
        self.central_widget.addWidget(self.settings_frame)
        
        # Timer setup
        self.timer_instance = QTimer(self)
        self.timer_instance.timeout.connect(self.update_timer_display)

        # Initialize
        self.running = False
        self.start_time = None
        self.elapsed_seconds = 0
        
        # Load timer state from file
        self.load_timer_state()
        self.update_timer_display(force_update=True)

        # Start the daily reset checker
        self.daily_reset_thread = threading.Thread(target=self.check_daily_reset)
        self.daily_reset_thread.daemon = True  # Allow the app to exit even if thread is running
        self.daily_reset_thread.start()
        
    def apply_settings(self):
        font_name = self.app_settings.font_name
        font_size = int(self.app_settings.font_size)
        font = QFont(font_name, font_size)
        self.timer_label.setFont(font)

    @pyqtSlot()
    def show_settings_view(self):
        self.central_widget.setCurrentWidget(self.settings_frame)

    @pyqtSlot()
    def show_history_view(self):
        self.central_widget.setCurrentWidget(self.history_frame)

    @pyqtSlot()
    def show_timer_view(self):
        self.central_widget.setCurrentWidget(self.timer_widget)

    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            self.timer_string.set("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))
            self.after(1000, self.update_timer)

    @pyqtSlot()
    def toggle_timer(self):
        self.elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(self.timer_label.text().split(":"))))  # Convert displayed time to seconds
        if not self.running:
            # Starting the timer
            self.start_time = time.time()
            self.running = True
            self.play_pause_button.setText("⏸")
            self.timer_instance.start(1000)  # Trigger every 1 second
        else:
            # Pausing the timer
            self.running = False
            self.play_pause_button.setText("▶")
            self.timer_instance.stop()

    def update_timer_display(self, force_update=False):
        if self.running:
            elapsed_time = time.time() - self.start_time + self.elapsed_seconds
        elif force_update:
            elapsed_time = self.elapsed_seconds
        else: 
            return 
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.setText("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))

    def show_history(self):
        HistoryFrame(self)
        
    def reset_timer(self):
        self.timer_string = "00:00:00"
    
    def perform_daily_reset(self):
        """Perform the daily save and reset operations."""
        self.save_to_db()
        self.reset_timer()
        self.check_daily_reset()  # Check again at midnight

    def check_daily_reset(self):
        now = datetime.datetime.now()
        # Calculate the time remaining until midnight
        midnight = now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
        delta_t = midnight - now
        seconds_to_midnight = delta_t.total_seconds()
        
        # Set a timer to call the reset function at midnight
        threading.Timer(seconds_to_midnight, self.perform_daily_reset).start()

    def save_to_db(self):
        elapsed_time = self.timer_label.text()
        today = datetime.date.today().strftime('%Y-%m-%d')
        save_to_db(today, elapsed_time)
    
    def save_timer_state(self):
        data = {
            'running': self.running,
            'elapsed_seconds': self.elapsed_seconds if not self.running else 0
        }
        with open(self.timer_state_file, 'w') as file:
            json.dump(data, file)
            
    def load_timer_state(self):
        try:
            with open(self.timer_state_file, 'r') as file:
                data = json.load(file)
                self.running = data.get('running', False) 
                self.elapsed_seconds = data.get('elapsed_seconds', 0)
        except FileNotFoundError:
            pass
    
    def closeEvent(self, event):
        if self.running:
            reply = QMessageBox.question(self, 'Exit Confirmation', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.toggle_timer()  # Pause the timer
                self.save_timer_state()
                event.accept()
            else:
                event.ignore()
        else:
            self.save_timer_state()
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())