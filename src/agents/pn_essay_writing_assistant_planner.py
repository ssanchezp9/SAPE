from src.agents.base_planner import BasePlanner
from src.agents.base_agent import BaseAgent
from src.models.plan import Plan
from src.agents.prompts.essay_writing_assistant_planner_prompt import ESSAY_WRITING_ASSISTANT_PLANNER_PROMPT
from typing import Dict, List, Optional

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class EssayWritingAssistantPlanner(BasePlanner):
    """
    Planificador integral para asistir en la redacción de ensayos académicos.
    
    Capacidades:
    - Investigación exhaustiva del tema (RagAgent)
    - Síntesis de fuentes y argumentos (ResumidorAgent)
    - Organización visual de ideas (ConceptMapAgent)
    - Estructuración del ensayo (EssayPlanAgent)
    """

    def __init__(self, agents: List[BaseAgent]):        super().__init__(
            name="EssayWritingAssistantPlanner",
            goal="Proporcionar asistencia integral desde la investigación hasta la planificación de ensayos académicos",
            system_prompt=ESSAY_WRITING_ASSISTANT_PLANNER_PROMPT,
            agents=agents,
            temperature=0.4,
            max_tokens=11000
        )
        
    def run(self, input_prompt: dict) -> str:
        """
        Ejecuta el planificador para asistir en la redacción de ensayos.
        
        Args:
            input_prompt: Dict con información sobre el tema y tipo de ensayo
            
        Returns:
            str: El resultado final de la asistencia integral para ensayos
        """
        user_input = input_prompt.get("input", str(input_prompt))
        return super().run(user_input=user_input)
