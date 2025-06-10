from src.agents.base_planner import BasePlanner
from src.agents.base_agent import BaseAgent
from src.models.plan import Plan
from src.agents.prompts.detailed_study_guide_planner_prompt import DETAILED_STUDY_GUIDE_PLANNER_PROMPT
from typing import Dict, List, Optional

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class DetailedStudyGuidePlanner(BasePlanner):
    """
    Planificador para crear guías de estudio muy completas y detalladas.
    
    Capacidades:
    - Investigación exhaustiva del tema (RagAgent)
    - Síntesis y resumen de información clave (ResumidorAgent)
    - Organización estructurada en guía de estudio (StudyGuideAgent)
    """

    def __init__(self, agents: List[BaseAgent]):        super().__init__(
            name="DetailedStudyGuidePlanner",
            goal="Crear guías de estudio exhaustivas combinando investigación, síntesis y organización educativa",
            system_prompt=DETAILED_STUDY_GUIDE_PLANNER_PROMPT,
            agents=agents,
            temperature=0.4,
            max_tokens=12000
        )
        
    def run(self, input_prompt: dict) -> str:
        """
        Ejecuta el planificador para crear guías de estudio detalladas.
        
        Args:
            input_prompt: Dict con información sobre el tema de estudio
            
        Returns:
            str: El resultado final de la guía de estudio ejecutada
        """
        user_input = input_prompt.get("input", str(input_prompt))
        return super().run(user_input=user_input)
