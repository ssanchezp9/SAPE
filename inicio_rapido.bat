@echo off
title SAPE Chat - Inicio Rápido

echo 🚀 Iniciando SAPE...

:: Iniciar API Server en ventana separada
start "SAPE API" cmd /c "python api_server.py"

:: Esperar 5 segundos para que el API se inicie
timeout /t 5 /nobreak >nul

:: Iniciar interfaz de chat
echo 🎨 Abriendo interfaz de chat...
python gradio_chat.py

pause
