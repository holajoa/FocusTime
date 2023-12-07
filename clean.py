from config import LOG_DIR, TIME_DATABASE
from sqlite3 import connect

# clear logs
with open(LOG_DIR, "w") as f:
    f.write("")

# clear database
conn = connect(TIME_DATABASE)
cursor = conn.cursor()
cursor.execute("DELETE FROM daily_times")
conn.commit()
conn.close()
