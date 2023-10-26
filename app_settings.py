import pickle
from config import SETTINGS_DIR


class AppSettings:
    def __init__(self):
        self.font_name = "Arial"  # default font
        self.font_size = 24  # default size


def save_settings(settings):
    with open(SETTINGS_DIR, "wb") as f:
        pickle.dump(settings, f)


def load_settings():
    try:
        with open(SETTINGS_DIR, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        # If settings file doesn't exist or there's an error reading it, return default settings
        return AppSettings()
