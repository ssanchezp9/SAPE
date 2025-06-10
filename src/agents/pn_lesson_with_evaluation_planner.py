from src.agents.base_planner import BasePlanner
from src.agents.base_agent import BaseAgent
from src.models.plan import Plan
from src.agents.prompts.lesson_with_evaluation_planner_prompt import LESSON_WITH_EVALUATION_PLANNER_PROMPT
from typing import Dict, List, Optional

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class LessonWithEvaluationPlanner(BasePlanner):
    """
    Planificador para crear lecciones completas con evaluación integrada.
    
    Capacidades:
    - Investigación de contenido educativo (RagAgent)
    - Estructuración pedagógica de la lección (LessonPlanAgent)
    - Creación de evaluaciones alineadas (TestGeneratorAgent)
    """

    def __init__(self, agents: List[BaseAgent]):        super().__init__(
            name="LessonWithEvaluationPlanner",
            goal="Crear lecciones completas con contenido pedagógico y evaluación integrada",
            system_prompt=LESSON_WITH_EVALUATION_PLANNER_PROMPT,
            agents=agents,
            temperature=0.4,
            max_tokens=10000
        )
        
    def run(self, input_prompt: dict) -> str:
        """
        Ejecuta el planificador para crear lecciones con evaluación.
        
        Args:
            input_prompt: Dict con información sobre el tema y nivel de la lección
            
        Returns:
            str: El resultado final de la lección con evaluación ejecutada
        """
        user_input = input_prompt.get("input", str(input_prompt))
        return super().run(user_input=user_input)
