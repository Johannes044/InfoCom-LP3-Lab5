@echo off
cls

echo 🔄 Hämtar brancher från origin...
git fetch --all

echo.
echo 🌿 Tillgängliga remote brancher:
for /f "tokens=1 delims=" %%b in ('git branch -r ^| findstr /V "->"') do (
    echo %%b
)

echo.
set /p branch=📝 Ange namnet pa den branch du vill checka ut (utan "origin/"): 

:: Kontrollera om lokal branch redan finns
git rev-parse --verify %branch% >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Lokala branchen "%branch%" finns redan. Byter till den...
    git checkout %branch%
) else (
    echo 📦 Skapar lokal branch "%branch%" som spårar "origin/%branch%"...
    git checkout -b %branch% origin/%branch%
)
