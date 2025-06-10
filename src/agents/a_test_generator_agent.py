from src.agents.base_agent import BaseAgent
from src.agents.prompts.agents_prompt import TEST_GENERATOR_AGENT_PROMPT

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class TestGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TestGeneratorAgent",
            goal="Generar tests y exámenes educativos personalizados con diferentes tipos de preguntas y niveles de dificultad.",
            prompt_template=TEST_GENERATOR_AGENT_PROMPT,
        )
