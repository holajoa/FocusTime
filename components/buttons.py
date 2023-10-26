from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from style.mainwindow import PLAY_PAUSE_BUTTON_STYLESHEET


class RoundButton(QPushButton):
    def __init__(
        self,
        parent=None,
        fixed_size=40,
    ):
        super().__init__(parent=parent)
        self.fixed_size = fixed_size
        self.setFixedSize(self.fixed_size, self.fixed_size)
        self.setStyleSheet(
            f"border-radius: {self.fixed_size//2}px; font-size: 20px; font-weight: bold;"
        )


class BackButton(RoundButton):
    def __init__(self, parent=None, fixed_size=30, icon_file="static/back_icon.png"):
        super().__init__(parent=parent, fixed_size=fixed_size)
        self.setIcon(QIcon(icon_file))
        icon_size = int(self.fixed_size * 0.6)
        self.setIconSize(QSize(icon_size, icon_size))
        self.clicked.connect(self.parent().parent.show_timer_view)


class PlayPauseButton(RoundButton):
    def __init__(
        self,
        parent=None,
        fixed_size=50,
        play_icon_file="static/play_icon.png",
        pause_icon_file="static/pause_icon.png",
    ):
        super().__init__(parent=parent, fixed_size=fixed_size)

        self.play_icon = QIcon(play_icon_file)
        self.pause_icon = QIcon(pause_icon_file)

        self.setIcon(self.play_icon)
        icon_size = int(self.fixed_size * 0.4)
        self.setIconSize(QSize(icon_size, icon_size))

        self.setStyleSheet(PLAY_PAUSE_BUTTON_STYLESHEET)

        self.clicked.connect(self.parent().toggle_timer)

    def toggle_icon(self, isRunning=False):
        if isRunning:
            # assert self.icon() == self.play_icon
            self.setIcon(self.pause_icon)
        else:
            # assert self.icon() == self.pause_icon
            self.setIcon(self.play_icon)
