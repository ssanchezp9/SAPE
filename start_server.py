"""
Script de inicio para el servidor API de SAPE
Proporciona una interfaz simple para iniciar el servidor con el SwarmMaster cargado
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def setup_environment():
    """Configura el entorno antes de iniciar el servidor"""
    
    # Verificar que estamos en el directorio correcto
    current_dir = Path.cwd()
    expected_files = ['requirements.txt', 'src', 'api_server.py']
    
    missing_files = []
    for file in expected_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Error: No se encontraron los siguientes archivos/directorios: {missing_files}")
        print(f"📁 Directorio actual: {current_dir}")
        print("🔍 Asegúrate de estar en el directorio raíz del proyecto SAPE")
        return False
    
    # Verificar variables de entorno necesarias
    required_env_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Error: Faltan las siguientes variables de entorno: {missing_vars}")
        print("💡 Asegúrate de tener configurado tu archivo .env o las variables de entorno")
        return False
    
    return True

def start_server(host="0.0.0.0", port=8000, reload=False):
    """Inicia el servidor FastAPI"""
    
    print("🔧 Configurando entorno...")
    if not setup_environment():
        sys.exit(1)
    
    print("✅ Entorno configurado correctamente")
    print(f"🚀 Iniciando servidor SAPE API en http://{host}:{port}")
    print("📦 Cargando SwarmMaster... (esto puede tardar unos segundos)")
    print("💡 El servidor estará listo cuando veas 'SwarmMaster cargado exitosamente'")
    print("🛑 Para detener el servidor, presiona Ctrl+C")
    print("-" * 60)
    
    try:
        # Ejecutar uvicorn con los parámetros especificados
        cmd = [
            sys.executable, "-m", "uvicorn",
            "api_server:app",
            f"--host={host}",
            f"--port={port}",
            "--log-level=info"
        ]
        
        if reload:
            cmd.append("--reload")
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

def main():
    """Función principal del script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Iniciar servidor API de SAPE")
    parser.add_argument("--host", default="0.0.0.0", help="Host para el servidor (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Puerto para el servidor (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Habilitar auto-reload para desarrollo")
    
    args = parser.parse_args()
    
    start_server(host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
