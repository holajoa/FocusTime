import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QMenu,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon

from views.history import HistoryView
from views.settings import SettingsView
from views.timer import TimerView
from style.mainwindow import STYLESHEET
from config import LOG_DIR, CFG

from utils.db_utils import initialize_db
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_DIR + "/app.log",
    filemode="a+",
)


class TimerApp(QMainWindow):
    def __init__(self, config=CFG):
        super().__init__()
        self.config = config
        self.init_db(**config)
        self.initUI()

    def init_db(self, **config):
        initialize_db(**config)

    def initUI(self):
        # Basic window settings
        self.setWindowTitle("FocusTime")
        # self.setGeometry(100, 100, 500, 300)
        self.setMinimumHeight(200)
        self.setWindowIcon(QIcon("static/timer-clock.png"))

        # Menu bar setup
        menubar = self.menuBar()
        fileMenu = QMenu("Menu", self)
        historyAction = fileMenu.addAction("Show History")
        settingsAction = fileMenu.addAction("Settings")
        menubar.addMenu(fileMenu)

        # Connect menu actions to respective slots
        historyAction.triggered.connect(self.show_history_view)
        settingsAction.triggered.connect(self.show_settings_view)

        # Create a stacked widget to manage different views
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        # Timer View
        self.timer_view = TimerView(self)
        self.central_widget.addWidget(self.timer_view)

        # History and Settings View
        self.history_view = HistoryView(self)
        self.central_widget.addWidget(self.history_view)

        self.settings_view = SettingsView(self)
        self.central_widget.addWidget(self.settings_view)

        self.setAttribute(Qt.WA_DeleteOnClose)

    @property
    def app_settings(self):
        return self.timer_view.app_settings

    @property
    def running(self):
        return self.timer_view.running

    @app_settings.setter
    def app_settings(self, value):
        self.timer_view.app_settings = value

    def apply_settings(self):
        self.timer_view.apply_settings()

    @pyqtSlot()
    def show_settings_view(self):
        self.central_widget.setCurrentWidget(self.settings_view)
        self.adjustSize()

    @pyqtSlot()
    def show_history_view(self):
        self.central_widget.setCurrentWidget(self.history_view)
        self.adjustSize()

    @pyqtSlot()
    def show_timer_view(self):
        self.central_widget.setCurrentWidget(self.timer_view)
        self.adjustSize()

    def show_history(self):
        HistoryView(self)

    def closeEvent(self, event):
        if self.timer_view.running:
            reply = QMessageBox.question(
                self,
                "Exit Confirmation",
                "Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.timer_view.on_exit_app()
                event.accept()
            else:
                event.ignore()
        else:
            self.timer_view.on_exit_app()
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet(STYLESHEET)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())
