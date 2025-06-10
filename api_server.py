"""
API Server para el sistema SAPE
Mantiene el SwarmMaster cargado y permite conversaciones persistentes a través de una API REST.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
import logging
from contextlib import asynccontextmanager

from src.agents.swarm_master import SwarmMaster
from src.utils.memory.conversation_memory import ConversationMemory
from src.utils.logger import logging_config

# Configurar logging
logger = logging_config.get_logger(__name__)

# SwarmMaster global compartido
global_swarm_master: Optional[SwarmMaster] = None

# Almacén de memorias de conversaciones separadas
conversation_memories: Dict[str, ConversationMemory] = {}

class ConversationRequest(BaseModel):
    """Modelo para las peticiones de conversación"""
    message: str
    conversation_id: Optional[str] = None
    
    class Config:
        # Ejemplo de uso en la documentación
        schema_extra = {
            "example": {
                "message": "Hola, quiero crear un resumen de un texto",
                "conversation_id": None  # Omitir para crear nueva conversación
            }
        }

class ConversationResponse(BaseModel):
    """Modelo para las respuestas de conversación"""
    conversation_id: str
    response: str
    message: str

class ConversationInfo(BaseModel):
    """Modelo para información de conversación"""
    conversation_id: str
    created_at: str
    message_count: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.
    Se ejecuta al inicio y al final de la aplicación.
    """
    global global_swarm_master
    
    # Startup
    logger.info("🚀 Iniciando servidor API...")
    logger.info("📦 Cargando SwarmMaster...")
    
    try:
        # Crear el SwarmMaster que se usará para todas las conversaciones
        global_swarm_master = SwarmMaster()
        logger.info("✅ SwarmMaster cargado exitosamente")
        logger.info(f"📊 Agentes disponibles: {len(global_swarm_master.agents)}")
        logger.info(f"📋 Planificadores disponibles: {len(global_swarm_master.planners)}")
        
    except Exception as e:
        logger.error(f"❌ Error al cargar SwarmMaster: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando servidor API...")
    conversation_memories.clear()
    logger.info("✅ Servidor cerrado correctamente")

# Crear la aplicación FastAPI con el lifespan
app = FastAPI(
    title="SAPE API",
    description="API para el sistema SAPE con SwarmMaster integrado",
    version="1.0.0",
    lifespan=lifespan
)



@app.post("/chat", response_model=ConversationResponse)
async def chat(request: ConversationRequest):
    """
    Endpoint principal para chatear con el SwarmMaster.
    Usa el SwarmMaster global como template y mantiene memorias separadas por conversación.
    """
    try:
        conversation_id = request.conversation_id
        
        # Si no hay conversation_id o es inválido, crear una nueva conversación
        if not conversation_id or conversation_id.strip() == "" or conversation_id == "string":
            conversation_id = str(uuid.uuid4())
            # Crear una nueva memoria para esta conversación
            conversation_memories[conversation_id] = ConversationMemory()
            logger.info(f"💬 Nueva conversación creada: {conversation_id}")
        
        # Verificar que la conversación existe, si no existe, crear una nueva
        if conversation_id not in conversation_memories:
            logger.warning(f"⚠️ Conversación {conversation_id} no encontrada, creando nueva conversación")
            conversation_id = str(uuid.uuid4())
            conversation_memories[conversation_id] = ConversationMemory()
            logger.info(f"💬 Nueva conversación creada (recuperación): {conversation_id}")
        
        # Obtener la memoria específica de esta conversación
        current_memory = conversation_memories[conversation_id]
        
        # Configurar temporalmente la memoria en el SwarmMaster global para esta request
        # Guardamos la memoria original
        original_memory = global_swarm_master.memory
        
        try:
            # Asignamos la memoria de la conversación actual
            global_swarm_master.memory = current_memory
            
            # Configurar la memoria en todos los agentes del SwarmMaster
            for agent in global_swarm_master.agents:
                if hasattr(agent, 'set_memory'):
                    agent.set_memory(current_memory)
            
            # Procesar el mensaje
            logger.info(f"💭 Procesando mensaje en conversación {conversation_id}: {request.message[:50]}...")
            response = global_swarm_master.run(request.message)
            
        finally:
            # Siempre restaurar la memoria original
            global_swarm_master.memory = original_memory
        
        logger.info(f"✅ Respuesta generada para conversación {conversation_id}")
        
        return ConversationResponse(
            conversation_id=conversation_id,
            response=response,
            message="Mensaje procesado correctamente"
        )
        
    except Exception as e:
        logger.error(f"❌ Error al procesar mensaje: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Iniciando servidor SAPE API...")
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Deshabilitar reload en producción
        log_level="info"
    )
