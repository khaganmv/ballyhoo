@ECHO off

FOR /F "tokens=* USEBACKQ" %%F IN (`pip show customtkinter ^| Findstr "Location: "`) DO (
    SET dir=%%F
)
set dir=%dir:~10%
set ctk=\customtkinter;customtkinter
set dirctk=%dir%%ctk%

set flags=--noconfirm --onefile --windowed
set lib=--hidden-import=PIL._tkinter_finder --add-data %dirctk%
set data=--add-data resources/clock_light.png;. --add-data resources/clock_dark.png;. --add-data resources/remove.png;. --add-data resources/ballyhoo.ico;.
set bin=--name ballyhoo --icon=resources/ballyhoo.ico src/main.py

pyinstaller %flags% %lib% %data% %bin%
