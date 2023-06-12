@echo off

REM Use FLASK_DEBUG=True if needed

set "SCRIPT_DIR=%~dp0"
set "FLASK_APP=%SCRIPT_DIR%\standalone.py"

python -m flask run --host 0.0.0.0 --with-threads