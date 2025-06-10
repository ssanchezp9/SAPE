from src.agents.base_agent import BaseAgent
from src.agents.prompts.agents_prompt import LESSON_PLAN_AGENT_PROMPT

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class LessonPlanAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="LessonPlanAgent",
            goal="Diseñar planes de clase estructurados y pedagógicamente efectivos para educadores de todos los niveles.",
            prompt_template=LESSON_PLAN_AGENT_PROMPT,
        )
