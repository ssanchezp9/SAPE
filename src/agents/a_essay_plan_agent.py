from src.agents.base_agent import BaseAgent
from src.agents.prompts.agents_prompt import ESSAY_PLAN_AGENT_PROMPT

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class EssayPlanAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="EssayPlanAgent",
            goal="Crear planes detallados para ensayos académicos con estructura argumentativa sólida y organización lógica.",
            prompt_template=ESSAY_PLAN_AGENT_PROMPT,
        )
