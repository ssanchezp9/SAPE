# swarm_master.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from src.models.plan import SelectedPlan, PlanEvaluation
from src.agents.prompts.swarm_master_prompt import SWARM_MASTER_PROMPT, PLAN_EVALUATION_PROMPT
from src.utils.memory.conversation_memory import ConversationMemory
from src.start_app import initialize_swarm_master

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)


class SwarmMaster():
    def __init__(self):
        """
        Inicializa el SwarmMaster usando la lógica de inicialización centralizada.
        """
        logger.info("Iniciando SwarmMaster con lógica de inicialización centralizada")
        
        # Usar la función de inicialización centralizada
        components = initialize_swarm_master()
        
        # Asignar todos los componentes inicializados
        self.agents = components['agents']
        self.planners = components['planners']
        self.agent_map = components['agent_map']
        self.planner_map = components['planner_map']
        self.llm = components['llm_selector']
        self.llm_evaluator = components['llm_evaluator']
        self.memory = ConversationMemory()
        self.system_prompt = components['system_prompt']
        
        # Configuración de memoria siempre habilitada
        self.enable_memory = True
        
        logger.info(f"SwarmMaster inicializado exitosamente con {len(self.agents)} agentes y {len(self.planners)} planificadores.")
        
    def run(self, user_input: str) -> str:
        """
        Ejecuta el swarm master con el input del usuario.
        
        Args:
            user_input: La entrada del usuario
            
        Returns:
            str: El resultado de la ejecución del planificador seleccionado
        """
        planSelected : SelectedPlan = self.select_planner(user_input)
          # Ejecutar el planificador seleccionado
        result = self.planner_map[planSelected.planner_name].run({"input": user_input})
          # Registrar la interacción a nivel de SwarmMaster
        self.memory.add_turn(
            user_input=user_input,
            agent_name="SwarmMaster",
            agent_response=f"Planificador seleccionado: {planSelected.planner_name}",
            metadata={
                "planner_selected": planSelected.planner_name,
                "planner_reasoning": planSelected.reasoning if hasattr(planSelected, 'reasoning') else None
            }
        )
        return result

    def select_planner(self, input_prompt: str) -> SelectedPlan:
        """
        Selecciona el planificador adecuado basado en el input del usuario.
        """
        # Crear mensajes base
        messages = [
            SystemMessage(content=self._get_formated_prompt())
        ]
          # Añadir contexto de memoria si está disponible
        context = self.memory.get_conversation_summary(last_n_turns=2)
        if context and context != "No hay historial de conversación disponible.":
            messages.append(SystemMessage(content=f"Contexto de conversación reciente:\n{context}"))
        
        messages.append(HumanMessage(content=input_prompt))

        response: SelectedPlan = self.llm.invoke(messages)
        logger.info(f"El swarm master ha seleccionado el planificador: {response.planner_name}")
        return response

    def _get_formated_prompt(self) -> str:
        """
        Formatea el prompt del usuario para el LLM.
        """
        return SWARM_MASTER_PROMPT.format(
            planners=chr(10).join([f"- {planner.name}: {planner.goal}\n" for planner in self.planners])
        )