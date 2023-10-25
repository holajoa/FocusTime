import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMenu, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import time
import threading
from views.history import HistoryFrame
from views.settings import SettingsFrame
from app_settings import load_settings
from db_utils import save_to_db, fetch_from_db
import datetime


class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Basic window settings
        self.setWindowTitle("Daily Timer")
        self.setGeometry(100, 100, 400, 300)
        
        # Initialize settings
        self.app_settings = load_settings()

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
        if not self.running:
            # Starting the timer
            self.start_time = time.time()
            self.elapsed_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(self.timer_label.text().split(":"))))  # Convert displayed time to seconds
            self.running = True
            self.play_pause_button.setText("⏸")
            self.timer_instance.start(1000)  # Trigger every 1 second
        else:
            # Pausing the timer
            self.running = False
            self.play_pause_button.setText("▶")
            self.timer_instance.stop()

    def update_timer_display(self):
        if self.running:
            elapsed_time = time.time() - self.start_time + self.elapsed_seconds
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

    def check_daily_reset(self):
        while True:
            now = datetime.datetime.now()
            # Check if it's close to midnight (within 2 seconds buffer to ensure we catch it)
            if now.hour == 23 and now.minute == 59 and now.second >= 58:
                self.perform_daily_reset()
                time.sleep(2)  # Sleep for a couple of seconds to pass midnight
            time.sleep(10)  # Check every 10 seconds

    def save_to_db(self):
        elapsed_time = self.timer_label.text()
        today = datetime.date.today().strftime('%Y-%m-%d')
        save_to_db(today, elapsed_time)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())
