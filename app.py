import tkinter as tk
import time
import datetime
import threading
from frames.history import HistoryFrame
from frames.settings import SettingsFrame
from app_settings import load_settings


class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Daily Timer")
        self.geometry("400x300")

        # Add menu bar
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Show History", command=self.show_history_view)
        self.file_menu.add_command(label="Settings", command=self.show_settings_view)
        self.menu_bar.add_cascade(label="Menu", menu=self.file_menu)
        self.config(menu=self.menu_bar)
        
        # Initialize settings
        self.app_settings = load_settings()

        # Timer Frame
        self.timer_frame = tk.Frame(self)
        self.timer_frame.grid(row=0, column=0, sticky="nsew")
        self.timer_string = tk.StringVar(self, "00:00:00")
        
        self.timer_label = tk.Label(self.timer_frame, textvar=self.timer_string, 
                                    font=(self.app_settings.font_name, self.app_settings.font_size))
        self.timer_label.grid(row=0, column=0, pady=20)
        
        self.play_pause_button = tk.Button(self.timer_frame, text="▶️", command=self.toggle_timer)
        self.play_pause_button.grid(row=1, column=0, pady=(40, 0))

        # History Frame
        self.history_frame = HistoryFrame(self)
        
        # Settings Frame
        self.settings_frame = SettingsFrame(self, self.apply_settings)
        
        # Configure the rows and columns
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.timer_frame.grid_rowconfigure(1, weight=1)
        self.timer_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # Initialize
        self.running = False
        self.start_time = None

        # Start the daily reset checker
        self.daily_reset_thread = threading.Thread(target=self.check_daily_reset)
        self.daily_reset_thread.daemon = True  # Allow the app to exit even if thread is running
        self.daily_reset_thread.start()
        
    def apply_settings(self):
        font_name = self.app_settings.font_name
        font_size = int(self.app_settings.font_size)
        self.timer_label.config(font=(font_name, font_size))

    def show_settings_view(self):
        self.timer_frame.grid_remove()  # Hide the timer frame
        self.history_frame.grid_remove()  # Hide the history frame, if it's visible
        self.settings_frame.grid(row=0, column=0, sticky="nsew")  # Show the settings frame

    def show_history_view(self):
        self.timer_frame.grid_remove()
        self.settings_frame.grid_remove()  # Hide the settings frame
        self.history_frame.grid(row=0, column=0, sticky="nsew")

    def show_timer_view(self):
        self.history_frame.grid_remove()
        self.settings_frame.grid_remove()  # Hide the settings frame
        self.timer_frame.grid(row=0, column=0, sticky="nsew")

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
        HistoryFrame(self)
        
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
