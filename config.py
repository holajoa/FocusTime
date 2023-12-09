import os
from userpaths import get_my_documents

DOC_DIR = get_my_documents()
APP_DATA_DIR = os.path.join(DOC_DIR, "FocusTime")

LOG_DIR = os.path.join(APP_DATA_DIR, "app.log")
RESOURCES = os.path.join(APP_DATA_DIR, "resources")

DATABASE_DIR = os.path.join(RESOURCES, "database")
TIME_DATABASE = os.path.join(DATABASE_DIR, "timer_data.db")
FONT_SETTINGS_DIR = os.path.join(RESOURCES, "font_settings.json")   

TIMER_FONT_CHOICES = ["Roboto Mono", "Lucida Console", "Courier New", "Cascadia Mono"]

CFG = {"database": TIME_DATABASE}
