import sqlite3
import datetime


DB_NAME = 'timer_data.db'

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_times
                      (date TEXT PRIMARY KEY, elapsed_time TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(today, elapsed_time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO daily_times (date, elapsed_time) VALUES (?, ?)', (today, elapsed_time))
    conn.commit()
    conn.close()

def fetch_from_db(date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT elapsed_time FROM daily_times WHERE date = ?', (date,))
    elapsed_time = cursor.fetchone()
    conn.close()
    return elapsed_time
