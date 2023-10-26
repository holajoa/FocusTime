from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QHBoxLayout


class LabeledSlider(QWidget):
    def __init__(self, orientation, parent=None, text: str = ""):
        super(LabeledSlider, self).__init__(parent)

        # Create the label and the slider
        self.label = QLabel(text, self)
        self.slider = QSlider(orientation, self)

        # Create a horizontal layout
        layout = QHBoxLayout(self)

        # Add the label and slider to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        # Set the layout to the widget
        self.setLayout(layout)

        self.setMaximumHeight(100)

    def value(self):
        """Returns the current value of the slider."""
        return self.slider.value()

    def setValue(self, value):
        """Sets the value of the slider."""
        self.slider.setValue(value)

    def setRange(self, min: int, max: int):
        """Sets the range of the slider."""
        self.slider.setRange(min, max)
