# Ballyhoo

Ballyhoo is a simple to-do list built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). The layout and functionality is inspired by Apple Reminders.

<p align="center">
  <img src="resources/screenshot.png"/>
</p>

## TODO

- [x] Refactoring
- [ ] DateTime picker
- [ ] Task editor
- [ ] Windows support
- [ ] Windows installer
- [ ] Add to startup support

## Installation

Extract `ballyhoo.zip` and run `main`.

## Building from source

### Dependencies

* `python3`
* `customtkinter`
* `pillow`

### Linux

Simply run the `scripts/build.sh` script.

### Windows

```
pyinstaller --noconfirm --onedir --windowed --hidden-import='PIL._tkinter_finder' --add-data '<site-packages path>/customtkinter;customtkinter' --add-data 'resources/remove.png;.' 'src/main.py'
```

To obtain the path to site-packages, simply run `pip show customtkinter`.
