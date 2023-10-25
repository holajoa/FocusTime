import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QToolTip
from PyQt5.QtGui import QMouseEvent
from db_utils import fetch_from_db


class DateLabel(QLabel):
    def __init__(self, text, parent=None, date=None):
        super().__init__(text, parent)
        self.date = date
        self.parent_widget = parent
        self.setObjectName(f"DateLabel({self.date})")

    def enterEvent(self, event: QMouseEvent):
        # Show elapsed time as tooltip
        elapsed_time = fetch_from_db(self.date)
        if elapsed_time:
            elapsed_time_str = elapsed_time[0]
        else:
            elapsed_time_str = "No data"
        QToolTip.showText(event.globalPos(), elapsed_time_str, self)

    def leaveEvent(self, event: QMouseEvent):
        # Hide the tooltip
        QToolTip.hideText()


class HistoryFrame(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        layout = QGridLayout(self)
        
        # Same logic for drawing the history
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        self.draw_history(current_year, current_month, layout)
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.parent.show_timer_view)
        layout.addWidget(self.back_button, 0, 0)
        
        self.setLayout(layout)

    def draw_history(self, year, month, layout):
        import calendar
        cal = calendar.monthcalendar(year, month)
        for week_index, week in enumerate(cal):
            for day_index, day in enumerate(week):
                if day != 0:
                    date_str = f"{year}-{month:02}-{day:02}"
                    day_label = DateLabel(str(day), self, date_str)
                    layout.addWidget(day_label, week_index+1, day_index)
