import tkinter as tk
import time
import datetime
import threading
from db_utils import save_to_db
from calendar_history import CalendarHistory


class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Daily Timer")
        self.geometry("300x150")

        # Timer label
        self.timer_string = tk.StringVar(self, "00:00:00")
        self.timer_label = tk.Label(self, textvar=self.timer_string, font=("Arial", 24))
        self.timer_label.pack(pady=20)

        # Play/Pause button (combined start and pause/resume)
        self.play_pause_button = tk.Button(self, text="▶", command=self.toggle_timer)
        self.play_pause_button.pack(side=tk.LEFT, padx=10)
        
        # Add "Show History" button
        self.history_button = tk.Button(self, text="Show History", command=self.show_history)
        self.history_button.pack(pady=10)

        # Initialize
        self.running = False
        self.start_time = None

        # Start the daily reset checker
        self.daily_reset_thread = threading.Thread(target=self.check_daily_reset)
        self.daily_reset_thread.daemon = True  # Allow the app to exit even if thread is running
        self.daily_reset_thread.start()

    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            self.timer_string.set("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))
            self.after(1000, self.update_timer)

    def toggle_timer(self):
        if not self.running:  # If timer not running, start it
            self.start_time = time.time() - sum(int(x) * 60 ** i for i, x in enumerate(reversed(self.timer_string.get().split(":"))))
            self.running = True
            self.play_pause_button.config(text="⏸")
            self.update_timer()
        else:  # If timer running, pause it
            self.running = False
            self.play_pause_button.config(text="▶")

    def show_history(self):
        CalendarHistory(self)
        
    def reset_timer(self):
        self.timer_string.set("00:00:00")
    
    def check_daily_reset(self):
        while True:
            now = datetime.datetime.now()
            # Check if it's close to midnight (within 2 seconds buffer to ensure we catch it)
            if now.hour == 23 and now.minute == 59 and now.second >= 58:
                self.save_to_db()
                time.sleep(2)  # Sleep for a couple of seconds to pass midnight
                self.reset_timer()
            time.sleep(10)  # Check every 10 seconds


if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
