STYLESHEET = """
/* Base window */
QMainWindow {
    background-color: #FFFFFF; /* White background for the main window */
}

/* Menu bar */
QMenuBar {
    background-color: #F6F6F6;
    border-bottom: 1px solid #E0E0E0;
}

QMenuBar::item {
    padding: 5px 10px;
}

QMenuBar::item:selected {
    background-color: #E0E0E0;
}

QMenu {
    background-color: #F6F6F6;
    border: 1px solid #E0E0E0;
}

QMenu::item {
    padding: 5px 20px;
}

QMenu::item:selected {
    background-color: #E0E0E0;
}

/* Timer label */
QLabel {
    color: #333333; /* Dark text for contrast */
}

/* Buttons */
QPushButton {
    background-color: #2196F3; /* Blue color for the play/pause button */
    color: #FFFFFF; /* White text color for the button */
    border-radius: 25px; /* half of width/height to create a circle */
    width: 30px; /* fixed width */
    height: 30px; /* fixed height */
}

QPushButton:hover {
    background-color: #1E88E5; /* Slightly darker shade for hover effect */
}

QPushButton:pressed {
    background-color: #1976D2; /* Even darker shade for pressed effect */
}
"""

PLAY_PAUSE_BUTTON_STYLESHEET = """
    QPushButton {
        background-color: #2196F3;
        border-radius: 25px;  
        color: white;
        font-size: 35px;  
    }
    QPushButton:hover {
        background-color: #1E88E5; /* Slightly darker shade for hover effect */
    }
    QPushButton:pressed {
        background-color: #1976D2; /* Even darker shade for pressed effect */
    }
"""
