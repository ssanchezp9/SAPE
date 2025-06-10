"""
Script para iniciar la interfaz de chat con Gradio
"""

import subprocess
import sys
import time
import threading
import requests
from pathlib import Path

def check_api_server():
    """Verifica si el API server está ejecutándose"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Inicia el API server si no está ejecutándose"""
    if not check_api_server():
        print("🚀 Iniciando API server...")
        # Ejecutar el API server en un proceso separado
        subprocess.Popen([
            sys.executable, "api_server.py"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        
        # Esperar a que el servidor esté listo
        print("⏳ Esperando a que el API server esté listo...")
        for i in range(30):  # Esperar máximo 30 segundos
            if check_api_server():
                print("✅ API server listo!")
                break
            time.sleep(1)
            print(f"   Esperando... ({i+1}/30)")
        else:
            print("❌ El API server no pudo iniciarse correctamente")
            return False
    else:
        print("✅ API server ya está ejecutándose")
    
    return True

def start_gradio():
    """Inicia la interfaz de Gradio"""
    print("🎨 Iniciando interfaz de chat con Gradio...")
    subprocess.run([sys.executable, "gradio_chat.py"])

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 SAPE - Interfaz de Chat")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("api_server.py").exists():
        print("❌ Error: No se encuentra api_server.py")
        print("   Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    if not Path("gradio_chat.py").exists():
        print("❌ Error: No se encuentra gradio_chat.py")
        sys.exit(1)
    
    # Iniciar API server si es necesario
    if start_api_server():
        # Iniciar interfaz de Gradio
        start_gradio()
    else:
        print("❌ No se pudo iniciar el sistema completo")
        sys.exit(1)
