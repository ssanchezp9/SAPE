from src.agents.base_agent import BaseAgent
from src.agents.prompts.agents_prompt import RESUMIDOR_AGENT_PROMPT

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

class ResumidorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ResumidorAgent",
            goal ="Tu objetivo es resumir informacion que te proporcionan.",
            prompt_template=RESUMIDOR_AGENT_PROMPT,
            )

