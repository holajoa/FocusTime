import tkinter as tk
from typing import Callable 
from app_settings import save_settings, load_settings


class SettingsFrame(tk.Frame):
    def __init__(self, parent:tk.Tk, apply_callback:Callable):
        super().__init__(parent)

        self.parent = parent
        self.apply_callback = apply_callback
        
        # Add a back button
        self.back_button = tk.Button(self, text="Back", command=parent.show_timer_view)
        self.back_button.grid(row=0, column=0, pady=20, columnspan=2)

        
        default_settings = load_settings()
        
        self.font_var = tk.StringVar(value=default_settings.font_name)
        self.font_choices = ["Arial", "Times New Roman", "Courier New", "Verdana", "Helvetica", "Fixedsys"] 
        self.font_dropdown_label = tk.Label(self, text="Select Font")
        self.font_dropdown_label.grid(row=1, column=0, sticky="w", padx=10)
        self.font_dropdown = tk.OptionMenu(self, self.font_var, *self.font_choices)
        self.font_dropdown.grid(row=1, column=1, padx=10, pady=10)
        
        self.font_size_scale = tk.Scale(self, from_=10, to=80, orient="horizontal", label="Font Size")
        self.font_size_scale.set(default_settings.font_size)
        self.font_size_scale.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        self.apply_settings_button = tk.Button(self, text="Apply Settings", command=self.apply_and_callback)
        self.apply_settings_button.grid(row=3, column=0, pady=10, columnspan=2)
        
        self.default_button = tk.Button(self, text="Save as Default", command=self.save_as_default)
        self.default_button.grid(row=4, column=0, pady=20, columnspan=2)  # Adjust grid placement as necessary

    def apply_and_callback(self):
        self.parent.app_settings.font_name = self.font_var.get()
        self.parent.app_settings.font_size = int(self.font_size_scale.get())
        self.apply_callback()

    def save_as_default(self):
        # Get current settings from UI elements (or however you're storing them in this frame)
        # Here's an example assuming you have a dropdown for font and an entry for size:
        self.parent.app_settings.font_name = self.font_var.get()
        self.parent.app_settings.font_size = int(self.font_size_scale.get())
        
        save_settings(self.parent.app_settings)
