dir=$(pip show customtkinter | grep 'Location: ')
dir=${dir:10}
ctk='/customtkinter:customtkinter'
dirctk=$dir$ctk
echo $dirctk

pyinstaller --noconfirm --onedir --windowed --hidden-import='PIL._tkinter_finder' --add-data $dirctk --add-data 'resources/remove.png:.' 'src/main.py'
