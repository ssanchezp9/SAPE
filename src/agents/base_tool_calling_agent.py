from langchain_openai import ChatOpenAI
from typing import Sequence, Optional
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from src.agents.base_agent import BaseAgent
from src.utils.memory.conversation_memory import ConversationMemory

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class BaseToolCallingAgent(BaseAgent):
    """Agente Tool Calling que puede manejar mensajes complejos"""
    def __init__(self, name: str, goal: str, prompt_template: str, tools: Sequence[BaseTool], memory: Optional[ConversationMemory] = None):
        super().__init__(
            name=name,
            goal=goal,
            prompt_template=prompt_template,
            memory=memory
        )
        self.tools = tools
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_template),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        # Crear el agente tool calling
        self.agent = create_tool_calling_agent(self.llm, self.tools, prompt)
          # Crear el executor del agente
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            handle_parsing_errors=True
        )
    def run(self, task: str, last_response: str | None = None) -> str:
        """
        Ejecuta el agente tool calling con soporte para memoria.
        
        Args:
            task: La tarea a ejecutar
            last_response: Respuesta anterior (para compatibilidad hacia atrás)
            
        Returns:
            str: El resultado de la ejecución
        """
        logger.info(f"ToolCallingAgent {self.name} recibió tarea: '{task}'")
        
        # Preparar el historial de chat
        chat_history = []
        
        # Usar el historial de memoria
        if self.memory:
            chat_history = self.memory.get_messages_for_langchain()
            # Limitar el historial para evitar tokens excesivos
            chat_history = chat_history[-10:]  # Últimos 10 mensajes (5 turnos)
        
        # Si hay una respuesta anterior (compatibilidad hacia atrás), incluirla
        if last_response and not self.memory:
            chat_history = [AIMessage(content=last_response)]
        
        # Input para el agente
        agent_input = {
            "input": task,
            "chat_history": chat_history
        }
            
        result = self.agent_executor.invoke(agent_input)
        
        output = result.get('output', str(result))
        logger.info(f"Resultado del ToolCallingAgent {self.name}: {output}")
          # Guardar este turno en memoria
        if self.memory:
            # Obtener metadatos de las herramientas usadas
            tools_used = []
            if 'intermediate_steps' in result:
                for step in result['intermediate_steps']:
                    if hasattr(step[0], 'tool'):
                        tools_used.append(step[0].tool)
            
            self.memory.add_turn(
                user_input=task,
                agent_name=self.name,
                agent_response=output,
                metadata={
                    "model": "gpt-4o-mini",
                    "temperature": 0.2,
                    "agent_type": "tool_calling_agent",
                    "tools_used": tools_used
                }
            )
        
        return output
