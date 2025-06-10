from src.agents.base_planner import BasePlanner
from src.agents.base_agent import BaseAgent
from src.models.plan import Plan
from src.agents.prompts.multi_format_review_planner_prompt import MULTI_FORMAT_REVIEW_PLANNER_PROMPT
from typing import Dict, List, Optional

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class MultiFormatReviewPlanner(BasePlanner):
    """
    Planificador para crear material de repaso en múltiples formatos.
    
    Capacidades:
    - Investigación de contenido (RagAgent)
    - Creación de guías textuales (StudyGuideAgent)
    - Generación de mapas conceptuales visuales (ConceptMapAgent)
    """

    def __init__(self, agents: List[BaseAgent]):        super().__init__(
            name="MultiFormatReviewPlanner",
            goal="Crear material de repaso complementario en formatos textual y visual",
            system_prompt=MULTI_FORMAT_REVIEW_PLANNER_PROMPT,
            agents=agents,
            temperature=0.4,
            max_tokens=9000
        )
        
    def run(self, input_prompt: dict) -> str:
        """
        Ejecuta el planificador para crear material de repaso multiformato.
        
        Args:
            input_prompt: Dict con información sobre el tema de repaso
            
        Returns:
            str: El resultado final del material de repaso en múltiples formatos
        """
        user_input = input_prompt.get("input", str(input_prompt))
        return super().run(user_input=user_input)
