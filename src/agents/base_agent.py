from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import Optional
from src.utils.memory.conversation_memory import ConversationMemory


from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class BaseAgent():

    def __init__(
        self, 
        name: str, 
        goal: str,
        prompt_template: str, 
        memory: Optional[ConversationMemory] = None,
        temperature: float = 0.3,
        max_tokens: int = 6000,
        model: str = "gpt-4o-mini"
    ):
        self.name = name
        self.goal = goal
        self.prompt_template = prompt_template
        self.memory = memory
        
        self.llm = ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens)

        logger.info(f"Agente {self.name} creado sin herramientas")
        logger.info(f"LLM configurado - modelo: {model}, temp: {temperature}, max_tokens: {max_tokens}")

    def run(self, task: str, last_response: str = None) -> str:
        """
        Ejecuta el agente con el estado actual.
        
        Args:
            task: La tarea a ejecutar
            last_response: Respuesta anterior (para compatibilidad hacia atrás)
            
        Returns:
            str: La respuesta del agente
        """
        logger.info(f"Agente {self.name} recibió tarea: '{task}'")
        
        messages = [
            SystemMessage(content=self.prompt_template),
        ]
        
        # Incluir contexto de memoria
        if self.memory:
            context = self.memory.get_context_for_agent(self.name, last_n_turns=3)
            if context:
                messages.append(SystemMessage(content=f"Contexto de conversación previa:\n{context}"))
            
            # Incluir historial reciente de mensajes
            recent_messages = self.memory.get_messages_for_langchain()
            if recent_messages:
                # Solo incluir los últimos 6 mensajes (3 turnos) para no sobrecargar
                messages.extend(recent_messages[-6:])
        
        # Añadir la tarea actual
        messages.append(HumanMessage(content=task))
        
        # Si hay una respuesta anterior (para compatibilidad), incluirla
        if last_response:
            messages.append(AIMessage(content=last_response))

        response = self.llm.invoke(messages)
        logger.info(f"Respuesta del LLM para {self.name}: {response.content}")

        # Guardar este turno en memoria
        if self.memory:
            self.memory.add_turn(
                user_input=task,
                agent_name=self.name,
                agent_response=response.content,
                metadata={
                    "model": "gpt-4o-mini",
                    "temperature": 0.2,
                    "agent_type": "base_agent"
                }
            )

        return response.content
    def set_memory(self, memory: ConversationMemory) -> None:
        """Establece la memoria de conversación para este agente."""
        self.memory = memory
        logger.info(f"Memoria establecida para agente {self.name}")
    
    def clear_memory(self) -> None:
        """Limpia la memoria del agente."""
        if self.memory:
            self.memory.clear_history()
            logger.info(f"Memoria limpiada para agente {self.name}")
    
    def get_conversation_summary(self) -> str:
        """Obtiene un resumen de la conversación."""
        if self.memory:
            return self.memory.get_conversation_summary()
        return "No hay memoria de conversación disponible."
    
    def __call__(self, state: dict) -> str:
        return self.run(str(state))
