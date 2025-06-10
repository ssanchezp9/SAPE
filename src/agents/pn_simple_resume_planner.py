from src.agents.base_planner import BasePlanner
from src.agents.base_agent import BaseAgent
from src.models.plan import Plan
from src.agents.prompts.simple_resume_planner_prompt import SIMPLE_RESUME_PLANNER_PROMPT
from typing import Dict, List, Optional

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class SimpleResumePlanner(BasePlanner):
    """
    Planificador simple para crear resúmenes usando solo el agente resumidor.
    
    Capacidades:
    - Creación directa de resúmenes sin búsqueda previa
    - Procesamiento eficiente para contenido ya disponible
    - Resúmenes concisos y estructurados
    """

    def __init__(self, agents: List[BaseAgent]):        super().__init__(
            name="SimpleResumePlanner",
            goal="Crear resúmenes directos y eficientes usando solo el agente resumidor",
            system_prompt=SIMPLE_RESUME_PLANNER_PROMPT,
            agents=agents,
            temperature=0.4,
            max_tokens=6000
        )
        
    def run(self, input_prompt: dict) -> str:
        """
        Ejecuta el planificador para crear resúmenes simples.
        
        Args:
            input_prompt: Dict con información sobre el contenido a resumir
            
        Returns:
            str: El resultado final del resumen ejecutado
        """
        user_input = input_prompt.get("input", str(input_prompt))
        return super().run(user_input=user_input)
