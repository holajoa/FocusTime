import pytest
from app import TimerApp
from PyQt5.QtWidgets import QApplication

app = QApplication([])


def test_settings_view():
    """
    Test that the settings view is displayed when the menu item is clicked,
    and that font and size settings can be changed and applied.
    """
    window = TimerApp()
    window.show()

    # Go to settings
    window.show_settings_view()
    assert window.settings_view.isVisible()

    # Change font and size
    original_font = window.timer_view.timer_label.font()
    window.settings_view.font_dropdown.setCurrentText("Roboto Mono")
    window.settings_view.font_size_scale.setValue(30)

    # Apply and verify changes
    window.settings_view.apply_and_callback()
    new_font = window.timer_view.timer_label.font()
    assert new_font.family() == "Roboto Mono"
    assert new_font.pointSize() == 30

    # Save and close
    window.settings_view.save_as_default()
    window.close()


def test_load_default_settings():
    """Test that the default settings are loaded when the app starts."""
    window = TimerApp()
    window.show()

    # Assumes the previous test has run and set the defaults
    font = window.timer_view.timer_label.font()
    assert font.family() == "Roboto Mono"
    assert font.pointSize() == 30

    window.close()
