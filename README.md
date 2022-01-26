# Task timer

Simple way to time tasks with built-in stopwatch like functionality.
Allows user and task to be specified from a dropdown and optional notes and ID for each task.
Recorded task details are appended to a CSV file.

<img width="131" alt="task_timer_screen_shot" src="https://user-images.githubusercontent.com/376295/151143120-c2e19f54-fcae-49a5-aafd-78dc85a370ea.png">


## Downloads
See [releases](https://github.com/Abe404/task_timer/releases)


## Settings file

The application will read the settings, including the task list, user names and csv output
location from a settings file that it will load from a file named task_time_settings.toml.txt in the home folder.
This file must exist before the application is started.

The following is some example contents of ~/task_timer_settings.toml.txt on OSX, where 
username whould be replaced with the current user.
```
user_names = ["user 1", "user 2", "user 3", "user 4"]
default_user_name = "user 1"
task_names = ["Kidney contour", "Bowel contour", "Spine contour", "another contour"]
csv_path = "/Users/username/task_times.csv"
```


### Development and Build process
The application is developed and built with python 3.9

#### To setup the development environment on OSX with python3.9

Create virtual environment (if you haven't already)
> python -m env venv

Activate it 
> source ./env/bin/activate

Install requirements
> pip install -r requirements.txt


#### To run the application from source

This assumues you already have the required dependencies installed from the development environment
> python main.py


#### Building the application.

To create the application using PyInstaller [0], which bundles an application and it's dependencies into a single package.
> python ./build/freeze.py

To build the installer.
> python ./build/installer.py


[0] https://pyinstaller.readthedocs.io/en/stable/
