@echo off
echo Setting up Fundi Platform...
echo.

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Creating superuser (optional)...
echo You can skip this by pressing Ctrl+C
python manage.py createsuperuser

echo.
echo Setup complete!
echo.
echo To run the server, use:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
pause






