from langchain_openai import ChatOpenAI
from src.models.plan import Plan
from langgraph.prebuilt import create_react_agent
from typing import List, Dict, Optional
from src.agents.base_agent import BaseAgent
from langgraph.prebuilt.chat_agent_executor import Prompt
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.utils.memory.conversation_memory import ConversationMemory

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class BasePlanner():
    """
    Clase base abstracta para todos los planificadores del sistema.
    Cada planner especializado debe heredar de esta clase e implementar
    los métodos abstractos.
    """

    def __init__(
        self, 
        name: str,
        goal: str,
        system_prompt: str,        agents: List[BaseAgent],
        memory: Optional[ConversationMemory] = None,
        temperature: float = 0.3,
        max_tokens: int = 8000,
        model: str = "gpt-4o-mini"
    ):
        self.name = name
        self.goal = goal
        self.system_prompt = system_prompt
        self.agents = agents
        self.memory = memory
        
        # Configurar LLM centralmente
        llm = ChatOpenAI(
            model=model, 
            temperature=temperature, 
            max_tokens=max_tokens
        )
        self.llm = llm.with_structured_output(Plan)

        self.agent_map = {agent.name: agent for agent in self.agents}

        logger.info(f"Planificador {self.name} creado con agentes: {[agent.name for agent in self.agents]}")
        logger.info(f"LLM configurado - modelo: {model}, temp: {temperature}, max_tokens: {max_tokens}")

    def run(self, user_input: str) -> str:
        """
        Ejecuta el planificador con el estado actual.
        
        Args:
            user_input: La entrada del usuario
            
        Returns:
            str: El resultado final de la ejecución del plan
        """
        logger.info(f"Planificador {self.name} procesando entrada: '{user_input}'")
        
        # Configurar memoria en agentes si está disponible
        if self.memory:
            for agent in self.agents:
                agent.set_memory(self.memory)
        
        # Generar el plan usando structured output
        plan: Plan = self._generate_plan(user_input)
        logger.info(f"Plan generado por {self.name}: {plan}")

        # Ejecutar el plan
        result = self.start_plan(plan, user_input)
        
        # Registrar la planificación en memoria
        if self.memory:
            self.memory.add_turn(
                user_input=user_input,
                agent_name=self.name,
                agent_response=f"Plan ejecutado con {len(plan.steps)} pasos. Resultado final: {result[:200]}{'...' if len(str(result)) > 200 else ''}",
                metadata={
                    "planner_type": "base_planner",
                    "plan_steps": len(plan.steps),
                    "agents_used": [step.agent for step in plan.steps],
                    "model": "gpt-4o-mini",
                    "plan_structure": [{"agent": step.agent, "task": step.task} for step in plan.steps]
                }
            )
        
        return result
    def _generate_plan(self, user_input: str) -> Plan:
        """
        Genera un plan usando structured output.
        
        Args:
            user_input: La entrada del usuario
            
        Returns:
            Plan: El plan estructurado generado
        """
        # Crear mensajes para el planificador
        messages = [
            SystemMessage(content=self._get_formatted_prompt()),
        ]
        
        # Incluir contexto de memoria si está disponible
        if self.memory:
            context = self.memory.get_context_for_agent(self.name, last_n_turns=2)
            if context:
                messages.append(SystemMessage(content=f"Contexto de conversación previa:\n{context}"))
            
            # Incluir historial reciente de mensajes
            recent_messages = self.memory.get_messages_for_langchain()
            if recent_messages:
                # Solo incluir los últimos 4 mensajes (2 turnos) para no sobrecargar
                messages.extend(recent_messages[-4:])
        
        messages.append(HumanMessage(content=user_input))

        # Usar el LLM con structured output para generar el plan
        plan: Plan = self.llm.invoke(messages)
        return plan

    def _get_formatted_prompt(self) -> str:
        """
        Formatea el prompt del planificador.
        """
        prompt = f"""Eres un planificador experto. Tu objetivo: {self.goal}

Agentes disponibles:
{chr(10).join([f"- {agent.name}: {agent.goal}" for agent in self.agents])}

Crea un plan paso a paso asignando cada tarea al agente más apropiado.
Ten en cuenta que solo puedes usar los agentes disponibles y que cada agente tiene un rol específico.

{self.system_prompt}
"""
        return prompt
    
    def start_plan(self, plan: Plan, user_input: str) -> str:
        """
        Ejecuta los pasos del plan secuencialmente.
        
        Args:
            plan: El plan a ejecutar
            user_input: La entrada original del usuario
            
        Returns:
            str: El resultado final de la ejecución del plan
        """
        last_response = None
        
        for i, step in enumerate(plan.steps):
            if step.agent in self.agent_map:
                logger.info(f"Ejecutando paso {i+1}/{len(plan.steps)}: {step.task} con agente {step.agent}")
                
                # Construir la tarea completa con contexto
                if i == 0:
                    # Primer paso: incluir la entrada original del usuario
                    full_task = f"Entrada del usuario: {user_input}\n\nTarea específica: {step.task}"
                else:
                    # Pasos posteriores: incluir respuesta anterior
                    full_task = f"Entrada del usuario: {user_input}\n\nRespuesta anterior: {last_response}\n\nTarea específica: {step.task}"
                
                current_response = self.agent_map[step.agent].run(
                    task=full_task
                )
                last_response = current_response
                
                logger.info(f"Paso {i+1} completado por {step.agent}")
            else:
                logger.error(f"Agente no encontrado: {step.agent}")
                
        return last_response

    def set_memory(self, memory: ConversationMemory) -> None:
        """Establece la memoria de conversación para este planificador."""
        self.memory = memory
        # Propagar la memoria a todos los agentes
        for agent in self.agents:
            agent.set_memory(memory)
        logger.info(f"Memoria establecida para planificador {self.name} y sus agentes")
    
    def clear_memory(self) -> None:
        """Limpia la memoria del planificador y sus agentes."""
        if self.memory:
            self.memory.clear_history()
        for agent in self.agents:
            agent.clear_memory()
        logger.info(f"Memoria limpiada para planificador {self.name} y sus agentes")
