@echo off
setlocal enabledelayedexpansion

:: Configuración de colores y título
title SAPE - Sistema de Chat
color 0A

echo.
echo ================================================
echo    🤖 SAPE - Sistema de Chat Inteligente
echo ================================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "api_server.py" (
    echo ❌ Error: No se encuentra api_server.py
    echo    Asegurate de ejecutar este script desde el directorio raiz del proyecto
    pause
    exit /b 1
)

if not exist "gradio_chat.py" (
    echo ❌ Error: No se encuentra gradio_chat.py
    echo    Ejecuta primero el script de Python para crear la interfaz
    pause
    exit /b 1
)

echo ✅ Archivos encontrados correctamente
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo    Instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

:: Verificar si el puerto 8000 está ocupado
netstat -an | find ":8000" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  El puerto 8000 ya está en uso
    echo    ¿Quieres continuar de todas formas? (s/n)
    set /p continuar=
    if /i "!continuar!" neq "s" (
        echo Operación cancelada
        pause
        exit /b 1
    )
)

echo 🚀 Iniciando API Server...
echo.

:: Crear ventana nueva para el API Server
start "SAPE API Server" cmd /k "python api_server.py"

:: Esperar a que el API server esté listo
echo ⏳ Esperando a que el API Server esté listo...
set /a contador=0
:check_server
set /a contador+=1
if !contador! gtr 30 (
    echo ❌ Timeout: El API Server no pudo iniciarse en 30 segundos
    echo    Revisa la ventana del API Server para ver errores
    pause
    exit /b 1
)

:: Verificar si el servidor está respondiendo
curl -s http://localhost:8000/docs >nul 2>&1
if %errorlevel% neq 0 (
    echo    Intentando conectar... (!contador!/30^)
    timeout /t 1 /nobreak >nul
    goto check_server
)

echo ✅ API Server está listo!
echo.

:: Esperar un poco más para asegurar estabilidad
timeout /t 2 /nobreak >nul

echo 🎨 Iniciando interfaz de chat con Gradio...
echo.
echo 📝 Instrucciones:
echo    - La interfaz se abrirá automáticamente en tu navegador
echo    - Si no se abre, ve a: http://localhost:7860
echo    - Para cerrar todo, cierra esta ventana y la del API Server
echo.

:: Iniciar Gradio en la misma ventana
python gradio_chat.py

echo.
echo 👋 ¡Gracias por usar SAPE!
pause
