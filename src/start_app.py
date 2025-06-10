# start_app.py
"""
Módulo de inicialización para el sistema SAPE.
Contiene toda la lógica de inicialización y configuración del SwarmMaster y sus componentes.
"""

from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI

# Importar todos los agentes
from src.agents.a_it_rag_agent import RagAgent
from src.agents.a_it_resumidor import ResumidorAgent
from src.agents.a_concept_map_agent import ConceptMapAgent
from src.agents.a_essay_plan_agent import EssayPlanAgent
from src.agents.a_lesson_plan_agent import LessonPlanAgent
from src.agents.a_study_guide_agent import StudyGuideAgent
from src.agents.a_test_generator_agent import TestGeneratorAgent
from src.agents.base_agent import BaseAgent

# Importar todos los planners
from src.agents.pn_simple_resume_planner import SimpleResumePlanner
from src.agents.pn_detailed_study_guide_planner import DetailedStudyGuidePlanner
from src.agents.pn_lesson_with_evaluation_planner import LessonWithEvaluationPlanner
from src.agents.pn_multi_format_review_planner import MultiFormatReviewPlanner
from src.agents.pn_essay_writing_assistant_planner import EssayWritingAssistantPlanner
from src.agents.base_planner import BasePlanner

# Importar modelos y prompts
from src.models.plan import SelectedPlan, PlanEvaluation
from src.agents.prompts.swarm_master_prompt import SWARM_MASTER_PROMPT, PLAN_EVALUATION_PROMPT

# Importar utilidades de memoria
from src.utils.memory.conversation_memory import ConversationMemory

# Importar configuración de logging
from src.utils.logger import logging_config

logger = logging_config.get_logger(__name__)


class SwarmMasterInitializer:
    """
    Clase responsable de la inicialización y configuración del SwarmMaster.
    Centraliza toda la lógica de setup y configuración.
    """
    
    def __init__(self):
        self.logger = logger
        
    def create_agents(self) -> List[BaseAgent]:
        """
        Crea y configura todos los agentes disponibles en el sistema.
        
        Returns:
            List[BaseAgent]: Lista de agentes configurados
        """
        agents = []
          # Agente RAG para búsquedas y consultas (optimizado para multi-agente)
        rag_agent = RagAgent(use_multiagent_mode=True)
        agents.append(rag_agent)
        self.logger.info("Agente RAG creado (modo multi-agente optimizado)")
        
        # Agente resumidor para crear resúmenes
        resumidor_agent = ResumidorAgent()
        agents.append(resumidor_agent)
        self.logger.info("Agente Resumidor creado")
        
        # Agente para crear mapas conceptuales
        concept_map_agent = ConceptMapAgent()
        agents.append(concept_map_agent)
        self.logger.info("Agente de Mapas Conceptuales creado")
        
        # Agente para crear planes de ensayos
        essay_plan_agent = EssayPlanAgent()
        agents.append(essay_plan_agent)
        self.logger.info("Agente de Planes de Ensayo creado")
        
        # Agente para crear planes de lecciones
        lesson_plan_agent = LessonPlanAgent()
        agents.append(lesson_plan_agent)
        self.logger.info("Agente de Planes de Lección creado")

        # Agente para crear guías de estudio
        study_guide_agent = StudyGuideAgent()
        agents.append(study_guide_agent)
        self.logger.info("Agente de Guías de Estudio creado")
          
        # Agente para generar pruebas y exámenes
        test_generator_agent = TestGeneratorAgent()
        agents.append(test_generator_agent)
        self.logger.info("Agente Generador de Pruebas creado")
        
        self.logger.info(f"Se crearon {len(agents)} agentes exitosamente")
        return agents
    
    def create_planners(self, agents: List[BaseAgent]) -> List[BasePlanner]:
        """
        Crea y configura todos los planificadores disponibles en el sistema.
        Cada planner recibe solo los agentes que realmente necesita.
        
        Args:
            agents: Lista de agentes disponibles
            
        Returns:
            List[BasePlanner]: Lista de planificadores configurados
        """
        planners = []
        
        # Crear un diccionario para acceder rápidamente a los agentes por nombre
        agent_map = {agent.name: agent for agent in agents}
        
        # Obtener agentes específicos por nombre
        rag_agent = agent_map["RagAgent"]
        resumidor_agent = agent_map["ResumidorAgent"]
        concept_map_agent = agent_map["ConceptMapAgent"]
        essay_plan_agent = agent_map["EssayPlanAgent"]
        lesson_plan_agent = agent_map["LessonPlanAgent"]
        study_guide_agent = agent_map["StudyGuideAgent"]
        test_generator_agent = agent_map["TestGeneratorAgent"]        # Planificador simple para resúmenes - solo usa ResumidorAgent
        simple_resume_planner = SimpleResumePlanner(agents=[resumidor_agent])
        planners.append(simple_resume_planner)
        self.logger.info("Planificador Simple de Resúmenes creado")
        
        # Planificador para guías de estudio detalladas - RAG + Resumidor + StudyGuide
        detailed_study_guide_planner = DetailedStudyGuidePlanner(agents=[rag_agent, resumidor_agent, study_guide_agent])
        planners.append(detailed_study_guide_planner)
        self.logger.info("Planificador de Guías de Estudio Detalladas creado")
        
        # Planificador para lecciones con evaluación - RAG + LessonPlan + TestGenerator
        lesson_with_evaluation_planner = LessonWithEvaluationPlanner(agents=[rag_agent, lesson_plan_agent, test_generator_agent])
        planners.append(lesson_with_evaluation_planner)
        self.logger.info("Planificador de Lecciones con Evaluación creado")
        
        # Planificador para material de repaso multiformato - RAG + StudyGuide + ConceptMap
        multi_format_review_planner = MultiFormatReviewPlanner(agents=[rag_agent, study_guide_agent, concept_map_agent])
        planners.append(multi_format_review_planner)
        self.logger.info("Planificador de Repaso Multiformato creado")
        
        # Planificador integral para ensayos - RAG + Resumidor + ConceptMap + EssayPlan
        essay_writing_assistant_planner = EssayWritingAssistantPlanner(agents=[rag_agent, resumidor_agent, concept_map_agent, essay_plan_agent])
        planners.append(essay_writing_assistant_planner)
        self.logger.info("Planificador Asistente de Ensayos creado")
        
        self.logger.info(f"Se crearon {len(planners)} planificadores exitosamente")
        return planners
    
    def create_llm_models(self) -> Dict[str, ChatOpenAI]:
        """
        Crea y configura los modelos de lenguaje necesarios.
        
        Returns:
            Dict[str, ChatOpenAI]: Diccionario con los modelos configurados
        """
        models = {}
        
        # Modelo para selección de planificadores
        models['selector'] = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.2
        ).with_structured_output(SelectedPlan)
        self.logger.info("Modelo selector de planificadores creado")
        
        # Modelo para evaluación de planes
        models['evaluator'] = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.1
        ).with_structured_output(PlanEvaluation)
        self.logger.info("Modelo evaluador de planes creado")
        
        return models
    
    def setup_memory_system(self) -> ConversationMemory:
        """
        Configura el sistema de memoria básico.
        
        Returns:
            ConversationMemory: Objeto de memoria de conversación configurado
        """
        current_memory = ConversationMemory()
        
        self.logger.info("Sistema de memoria básico configurado")
        return current_memory
    
    def setup_agents_memory(self, agents: List[BaseAgent], memory: ConversationMemory):
        """
        Configura la memoria en todos los agentes.
        
        Args:
            agents: Lista de agentes a configurar
            memory: Objeto de memoria de conversación
        """
        if memory:
            for agent in agents:
                agent.set_memory(memory)
            self.logger.info("Memoria configurada en todos los agentes")
    
    def create_agent_and_planner_maps(self, agents: List[BaseAgent], planners: List[BasePlanner]) -> tuple:
        """
        Crea diccionarios de mapeo para acceso rápido a agentes y planificadores.
        
        Args:
            agents: Lista de agentes
            planners: Lista de planificadores
            
        Returns:
            tuple: (agent_map, planner_map)
        """
        agent_map = {agent.name: agent for agent in agents}
        planner_map = {planner.name: planner for planner in planners}
        
        self.logger.info(f"Maps creados: {len(agent_map)} agentes, {len(planner_map)} planificadores")
        return agent_map, planner_map
    
    def initialize_swarm_master_components(self) -> Dict:
        """
        Inicializa todos los componentes necesarios para el SwarmMaster.
        
        Returns:
            Dict: Diccionario con todos los componentes inicializados
        """
        self.logger.info("Iniciando inicialización de componentes del SwarmMaster")
        
        # 1. Crear agentes
        agents = self.create_agents()
        
        # 2. Crear planificadores (sin memoria, el SwarmMaster manejará esto)
        planners = self.create_planners(agents)
        
        # 3. Crear modelos de lenguaje
        llm_models = self.create_llm_models()
        
        # 4. Crear mapas de acceso rápido
        agent_map, planner_map = self.create_agent_and_planner_maps(agents, planners)
        
        components = {
            'agents': agents,
            'planners': planners,
            'agent_map': agent_map,
            'planner_map': planner_map,
            'llm_selector': llm_models['selector'],
            'llm_evaluator': llm_models['evaluator'],
            'system_prompt': SWARM_MASTER_PROMPT
        }
        
        self.logger.info("Inicialización de componentes del SwarmMaster completada exitosamente")
        return components


def initialize_swarm_master() -> Dict:
    """
    Función de conveniencia para inicializar todos los componentes del SwarmMaster.
    
    Returns:
        Dict: Diccionario con todos los componentes inicializados
    """
    initializer = SwarmMasterInitializer()
    return initializer.initialize_swarm_master_components()
