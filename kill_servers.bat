@echo off
echo Shutting down the Truth-Seeking Pod...

echo.
echo Killing llama-server instances...
taskkill /F /IM llama-server.exe /T >nul 2>&1

echo Killing associated command prompt windows...
taskkill /F /FI "WINDOWTITLE eq Debater Server*" /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Referee Server*" /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Streamlit UI*" /T >nul 2>&1

echo.
echo Shutdown complete!
pause