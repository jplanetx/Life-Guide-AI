
@echo off
rem Activate the virtual environment
venv\Scripts\activate

rem Run the pre-commit checks
pre-commit run --all-files
