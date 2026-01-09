@echo off
echo ========================================
echo Connexion au depot GitHub
echo ========================================
echo.

cd C:\Users\ubunt\tchad-langues-ai

echo Ajout du remote GitHub...
git remote add origin https://github.com/Natacha-K-Cyber/tchad-langues-ai.git

echo.
echo Verification du remote...
git remote -v

echo.
echo ========================================
echo IMPORTANT: Assure-toi d'avoir cree le depot sur GitHub d'abord!
echo URL: https://github.com/Natacha-K-Cyber/tchad-langues-ai
echo ========================================
echo.
echo Pour pousser le code, execute:
echo   git push -u origin main
echo.
pause

