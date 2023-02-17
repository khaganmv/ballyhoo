@ECHO off

IF exist src\__pycache__ (rd /s /q src\__pycache__)
IF exist build (rd /s /q build)
IF exist dist (rd /s /q dist)
IF exist main.spec (del main.spec)
IF exist settings.json (del settings.json)
IF exist tasks.json (del tasks.json)
IF exist ballyhoo.zip (del ballyhoo.zip)
