@echo off
REM ===================================================================
REM Script de Inicio para Generador de Exámenes con IA (Windows)
REM Requiere: Python y uv instalados
REM ===================================================================

echo.
echo ==========================================
echo  Generador de Exámenes Universitarios
echo  (Entorno Windows - uv)
echo ==========================================
echo.

REM 1. Verificar si uv está instalado
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se encontró 'uv' en el sistema.
    echo Por favor, instálelo primero ejecutando:
    echo    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo O descárguelo desde: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo [OK] uv encontrado.

REM 2. Sincronizar el entorno virtual e instalar dependencias
echo [INFO] Sincronizando entorno virtual e instalando dependencias...
call uv sync
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al sincronizar el entorno. Verifique su conexión a internet o el archivo pyproject.toml.
    pause
    exit /b 1
)

echo [OK] Entorno listo.

REM 3. Ejecutar la aplicación principal
echo [INFO] Iniciando la aplicación...
echo.
call uv run python main.py

REM 4. Manejo de errores de ejecución
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ADVERTENCIA] La aplicación se cerró con un código de error: %ERRORLEVEL%
    echo Posibles causas:
    echo - Falta tkinter (viene con la instalación estándar de Python para Windows).
    echo - Ollama no está ejecutándose o el modelo no está descargado.
    pause
)
