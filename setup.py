from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "packages": [],
    "excludes": [],
    "include_files": ["static", "resources"],
}

import sys

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        "app.py",
        base=base,
        target_name="FocusTime.exe",
        icon="static/timer-clock.ico",
    )
]

setup(
    name="FocusTime",
    version="1.0",
    description="FocusTime is a minimalistic desktop timer app that allows fully flexible time tracking of uninterrupted focus periods.",
    executables=executables,
    options={
        "build_exe": build_options,
        # "bdist_msi": {
        #     "data":{
        #         "Shortcut": [
        #             (
        #                 "DesktopShortcut",        # Shortcut
        #                 "DesktopFolder",          # Directory_
        #                 "FocusTime",              # Name
        #                 "TARGETDIR",              # Component_
        #                 "[TARGETDIR]FocusTime.exe",# Target
        #                 None,                     # Arguments
        #                 None,                     # Description
        #                 None,                     # Hotkey
        #                 "",                       # Icon
        #                 0,                        # IconIndex
        #                 None,                     # ShowCmd
        #                 "TARGETDIR",              # WkDir
        #             ),
        #             (
        #                 "StartupShortcut",        # Shortcut
        #                 "StartupFolder",          # Directory_
        #                 "FocusTime",              # Name
        #                 "TARGETDIR",              # Component_
        #                 "[TARGETDIR]FocusTime.exe",# Target
        #                 None,                     # Arguments
        #                 None,                     # Description
        #                 None,                     # Hotkey
        #                 "",                       # Icon
        #                 0,                        # IconIndex
        #                 None,                     # ShowCmd
        #                 "TARGETDIR",              # WkDir
        #             ),
        #         ]
        #     }
        # },
    },
)
