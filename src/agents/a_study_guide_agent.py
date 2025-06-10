from src.agents.base_agent import BaseAgent
from src.agents.prompts.agents_prompt import STUDY_GUIDE_AGENT_PROMPT

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class StudyGuideAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="StudyGuideAgent",
            goal="Crear guías de estudio completas y estructuradas que faciliten el aprendizaje y la preparación para exámenes.",
            prompt_template=STUDY_GUIDE_AGENT_PROMPT,
        )
