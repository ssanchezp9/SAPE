from src.agents.base_agent import BaseAgent
from src.agents.prompts.agents_prompt import CONCEPT_MAP_AGENT_PROMPT

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class ConceptMapAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ConceptMapAgent",
            goal="Crear mapas conceptuales claros que visualicen las relaciones entre ideas y conceptos educativos.",
            prompt_template=CONCEPT_MAP_AGENT_PROMPT,
        )
