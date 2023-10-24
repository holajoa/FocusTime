import tkinter as tk
import datetime
from db_utils import fetch_from_db


class CalendarHistory(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Elapsed Time History")
    
        # Get the current month and year
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        # Draw calendar
        self.draw_calendar(current_year, current_month)

    def draw_calendar(self, year, month):
        # Use Python's calendar module to get the month's day matrix
        import calendar
        cal = calendar.monthcalendar(year, month)

        # For each day in the matrix, create a label in the grid
        for week_index, week in enumerate(cal):
            for day_index, day in enumerate(week):
                if day != 0:
                    day_label = tk.Label(self, text=str(day))
                    day_label.grid(row=week_index, column=day_index, padx=5, pady=5, sticky="nsew")

                    # Bind click event to display elapsed time
                    day_label.bind("<Button-1>", lambda event, date=f"{year}-{month:02}-{day:02}": self.display_elapsed_time(event, date))

        # Stretch columns and rows to fit the window
        for i in range(7):
            self.grid_columnconfigure(i, weight=1)
        for i in range(len(cal)):
            self.grid_rowconfigure(i, weight=1)

    def display_elapsed_time(self, event, date):
        # Fetch elapsed time from database for the given date
        elapsed_time = fetch_from_db(date)

        # If there's an elapsed time for the date, display it; otherwise, show "No data"
        if elapsed_time:
            elapsed_time_str = elapsed_time[0]
        else:
            elapsed_time_str = "No data"

        # Create a small popup to display the elapsed time
        elapsed_time_popup = tk.Toplevel(self)
        elapsed_time_popup.title(f"Elapsed Time for {date}")
        elapsed_time_label = tk.Label(elapsed_time_popup, text=elapsed_time_str, font=("Arial", 16))
        elapsed_time_label.pack(pady=20, padx=20)
        