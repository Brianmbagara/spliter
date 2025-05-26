@echo off
REM Check Python version and site-packages
echo Checking Python version and site-packages...
python --version
python -m site

REM Install PyPDF2 in the current Python environment
echo Installing PyPDF2...
python -m pip install PyPDF2

REM Run the PDF processor script
echo Running PDF processor script...
python pdf_processor/src/main.py

echo.
echo When prompted, please enter the full path to the FOLDER containing your PDF files.
echo Do NOT include surrounding quotes.
echo Example: C:\Users\lenovo\OneDrive\Music\renaming\New folder\reanming
echo.
pause
