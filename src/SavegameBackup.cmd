@echo off
cd %~dp0
call ..\.venv\Scripts\activate
app.py
call deactivate
