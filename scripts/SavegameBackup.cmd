@echo off
cd %~dp0\..
call .venv\Scripts\activate
savegamebackup\app.py
call deactivate
