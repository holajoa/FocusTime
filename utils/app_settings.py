import json

from config import FONT_SETTINGS_DIR


class AppSettings:
    def __init__(self, font_name="Roboto Mono", font_size=50):
        self.font_name = font_name
        self.font_size = font_size

    def __dict__(self):
        return {
            "font_name": self.font_name,
            "font_size": self.font_size,
        }


def save_settings(settings):
    with open(FONT_SETTINGS_DIR, "w") as f:
        json.dump(settings.__dict__(), f)


def load_settings():
    try:
        with open(FONT_SETTINGS_DIR, "rb") as f:
            settings = json.load(f)
            return AppSettings(**settings)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return AppSettings()
