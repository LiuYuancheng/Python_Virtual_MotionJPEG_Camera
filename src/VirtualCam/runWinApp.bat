echo "Running Aviation Runway virtual camera - operation room [webCamApp.py]"
@echo off
REM Enable the virtual environment, replace the vEnv3.8 with the vEnv you configured.
call workon vEnv3.9
REM Check if the environment activation was successful
if %errorlevel% neq 0 (
    echo "Failed to activate virtual environment, run with default python interpreter"
    REM Run the program with python/python3
    echo "> Run program under default interpreter"
    python webCamApp.py
    pause
    exit /b %errorlevel%
)
echo "> Run program under virtual environment"
REM Run the Python script under virtual environment.
call webCamApp.py
pause