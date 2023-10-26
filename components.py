from PyQt5.QtWidgets import QPushButton


class RoundButton(QPushButton):
    def __init__(self, parent=None, ):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet("border-radius: 20px; font-size: 20px; font-weight: bold;")
        
class BackButton(RoundButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("⬅")
        self.clicked.connect(self.parent().parent.show_timer_view)
        