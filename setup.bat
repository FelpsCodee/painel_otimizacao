@echo off
echo ============================================
echo    PC Optimizer Pro - Setup
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale o Python 3.10+ primeiro.
    pause
    exit /b 1
)

echo Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ============================================
echo    Setup concluido com sucesso!
echo    Execute: run.bat
echo ============================================
pause
