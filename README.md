# Focus Time

A simple desktop application to monitor and visualise daily deep work hours. 

## Who Is This For?

Designed for individuals who want a straightforward way to track their total work time each day without:
- the fuss of detailed task breakdowns, or
- pomodoro timer sounds that disrupt focus.

## Installation
Download the installer [here](https://drive.google.com/file/d/1P2U3dRI39yIAtyyw_ozG_CI5taRO9Iyl/view?usp=drive_link).

Alternatively, clone the repository and build msi. 
```
git clone https://github.com/holajoa/FocusTime.git
cd FocusTime
python ./setup.py bdist_msi
```
Then run the installer. 

## Features
- **Time Recording**: Start, pause and resume work timer at any time. Cumulatively tracking work hours throughout the day. Automatic daily resets. 
- **Calendar Overview**: Easily view and log the total hours worked each day. A monthly calendar representation to provide a quick glance at your work routine. Hover over a date to see precise work duration.
- **Font and Size Adjustments**

### Next Steps
- [x] Refactor: Timer view separate from main `app.py`.
- [x] Change database datetime format. 
- [x] Create a config class for app, setting datebase etc
- [x] Change app icon.
- [ ] Change from msi to release. 
- [ ] Standardise stylesheet.
- [ ] Fix settings view UI.
- [ ] Fix history view colour display. 

*App icon from https://www.flaticon.com/free-icons/stopwatch"*
