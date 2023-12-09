from config import LOG_DIR, TIME_DATABASE
import os

# clear logs
with open(LOG_DIR, "w") as f:
    f.write("")

# remove database
os.remove(TIME_DATABASE)
