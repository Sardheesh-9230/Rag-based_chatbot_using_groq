@echo off
echo RAG Chatbot System Launcher
echo ==========================
echo.
echo 1. Start Web Interface for Document Upload
echo 2. Start Chatbot
echo 3. Process Documents (Build Index)
echo 4. Exit
echo.

:menu
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting Web Interface on http://localhost:5000
    echo Press Ctrl+C to stop the server
    echo.
    start "" http://localhost:5000
    python app.py
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Starting RAG Chatbot...
    echo.
    python chatbot.py
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Processing documents and building index...
    echo.
    python process_pdf.py
    echo.
    echo Done! Press any key to continue...
    pause > nul
    cls
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Goodbye!
    exit
)

echo Invalid choice. Please try again.
goto menu