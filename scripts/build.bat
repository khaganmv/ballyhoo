@ECHO off

FOR /F "tokens=* USEBACKQ" %%F IN (`pip show customtkinter ^| Findstr "Location: "`) DO (
    SET dir=%%F
)
set dir=%dir:~10%
set ctk=\customtkinter;customtkinter
set dirctk=%dir%%ctk%

pyinstaller --noconfirm --onefile --windowed --hidden-import=PIL._tkinter_finder --add-data %dirctk% --add-data resources/remove.png;. src/main.py
