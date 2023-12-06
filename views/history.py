import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QToolTip, QComboBox
from PyQt5.QtGui import QMouseEvent, QColor, QPainter
from PyQt5.QtCore import Qt

from utils.db_utils import fetch_from_db
from components.buttons import BackButton


def calculate_color(elapsed_time_str, min_val=0, max_val=10, repr=True):
    """Calculate the color based on the elapsed time string."""
    if elapsed_time_str == "00:00:00":
        if repr:
            return "rgb(255, 255, 255)"
        return QColor(255, 255, 255, 0)
    value = min(23, int(elapsed_time_str[:2]) + 1)
    value = max(min(value, max_val), min_val)
    normalized_value = (value - min_val) / (max_val - min_val)
    green_intensity = int(normalized_value * 255)
    r, g, b = green_intensity, 255 - int(green_intensity * 3 / 4), green_intensity
    if repr:
        return f"rgb({r}, {g}, {b})"
    return QColor(r, g, b, int(255 * 0.8))


class DateLabel(QLabel):
    def __init__(self, text, parent=None, date=None):
        super().__init__(text, parent)
        self.date = date
        self.parent_widget = parent
        self.setObjectName(f"DateLabel({self.date})")
        self.setAlignment(Qt.AlignCenter)

        total_seconds = fetch_from_db(self.date)
        # Convert total seconds to hours, minutes, and seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.elapsed_time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        self.color = calculate_color(self.elapsed_time_str, repr=False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)  # For smoother edges

        # Draw the circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        r = (
            min(self.width(), self.height()) // 8
        )  # radius; adjust the division factor to change circle size
        center_x = self.width() // 2
        center_y = self.height() // 2
        painter.drawEllipse(center_x, center_y, 2 * r, 2 * r)

        # Draw the text
        font = painter.font()
        font.setPointSize(10)  # You can adjust the font size as per your requirement
        painter.setFont(font)
        painter.setPen(Qt.black)  # Set text color
        font_metrics = painter.fontMetrics()
        painter.drawText(8, 16, self.text())

        painter.end()

    def enterEvent(self, event: QMouseEvent):
        # Show elapsed time as tooltip
        QToolTip.showText(event.globalPos(), self.elapsed_time_str, self)

    def leaveEvent(self, event: QMouseEvent):
        # Hide the tooltip
        QToolTip.hideText()


class HistoryView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        layout = QGridLayout(self)

        # Dropdown for selecting month
        self.month_selector = QComboBox(self)
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        self.month_selector.addItems(months)
        current_month = datetime.datetime.now().month
        self.month_selector.setCurrentIndex(
            current_month - 1
        )  # -1 because list index starts at 0
        self.month_selector.currentIndexChanged.connect(self.update_calendar_view)
        layout.addWidget(self.month_selector, 0, 6)

        current_year = datetime.datetime.now().year
        self.draw_history(current_year, current_month, layout)

        self.back_button = BackButton(self)
        layout.addWidget(self.back_button, 0, 0)

        self.setLayout(layout)
        self.setStyleSheet("border: 1px solid lightgray;")

    def draw_history(self, year, month, layout):
        import calendar

        # Clear any previous widgets except controls
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None and not isinstance(widget, (BackButton, QComboBox)):
                widget.deleteLater()

        cal = calendar.monthcalendar(year, month)
        for week_index, week in enumerate(cal):
            for day_index, day in enumerate(week):
                if day != 0:
                    date_str = f"{year}-{month:02}-{day:02}"
                    day_label = DateLabel(str(day), self, date_str)

                    # Equal space for dates
                    day_label.setFixedSize(40, 40)

                    layout.addWidget(day_label, week_index + 1, day_index)

    def update_calendar_view(self, month_index):
        year = datetime.datetime.now().year
        self.draw_history(
            year, month_index + 1, self.layout()
        )  # +1 because list index starts at 0
