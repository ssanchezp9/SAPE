from src.agents.base_tool_calling_agent import BaseToolCallingAgent
from langchain_core.tools import tool
from src.agents.prompts.agents_prompt import RAG_AGENT_PROMPT
from src.agents.prompts.rag_agent_multiagent_prompt import RAG_AGENT_MULTIAGENT_PROMPT
from src.utils.rag.document_ingestor import DocumentIngestor
from typing import List, Dict, Any

from src.utils.logger import logging_config
logger = logging_config.get_logger(__name__)

@tool
def search_knowledge_base(query: str, num_results: int = 8, similarity_threshold: float = 0.7) -> str:
    """
    Búsqueda RAG en la base de conocimientos.
    
    Args:
        query (str): La consulta para buscar información relevante.
        num_results (int): Número máximo de chunks a recuperar (default: 8)
        similarity_threshold (float): Umbral mínimo de similaridad (default: 0.7)
        
    Returns:
        str: Los chunks más relevantes encontrados.
    """
    try:
        logger.info(f"🔍 Búsqueda RAG para: '{query}'")
        
        ingestor = DocumentIngestor()
        results = ingestor.vectorstore.similarity_search_with_score(query=query, k=num_results)
        
        if not results:
            return "No se encontraron documentos relevantes para la consulta."
        
        # Filtrar por umbral de similaridad
        filtered_results = []
        for doc, score in results:
            similarity = 1 - score if score <= 1 else 1 / (1 + score)
            if similarity >= similarity_threshold:
                filtered_results.append((doc, similarity))
        
        if not filtered_results:
            # Fallback con umbral más bajo
            for doc, score in results[:3]:
                similarity = 1 - score if score <= 1 else 1 / (1 + score)
                filtered_results.append((doc, similarity))
        
        return _format_results(filtered_results, query)
        
    except Exception as e:
        logger.error(f"❌ Error en búsqueda RAG: {str(e)}")
        return f"Error al buscar información: {str(e)}"

def _format_results(results: List, query: str) -> str:
    """Formatea los resultados de búsqueda de manera simple."""
    if not results:
        return "No se encontraron documentos relevantes."
    
    header = f"🔍 Resultados para: '{query}'\n{'='*50}\n"
    formatted_chunks = [header]
    
    for i, (doc, similarity) in enumerate(results, 1):
        chunk_text = f"""
📄 RESULTADO #{i}
Relevancia: {similarity:.1%}

{doc.page_content}

📚 Fuente: {doc.metadata.get('source', 'No especificada') if doc.metadata else 'No especificada'}
{'-'*50}
"""
        formatted_chunks.append(chunk_text)
    
    return "\n".join(formatted_chunks)

@tool
def search_by_metadata_filter(
    query: str,
    asignatura: str = None,
    tema: str = None,
    nivel: str = None,
    curso: str = None,
    num_results: int = 5
) -> str:
    """
    Búsqueda RAG con filtros de metadata.
    
    Args:
        query (str): La consulta de búsqueda
        asignatura (str): Filtrar por asignatura específica
        tema (str): Filtrar por tema específico
        nivel (str): Filtrar por nivel educativo
        curso (str): Filtrar por curso
        num_results (int): Número de resultados a retornar
        
    Returns:
        str: Resultados filtrados por metadata.
    """
    try:
        logger.info(f"🎯 Búsqueda con filtros - Query: '{query}'")
        
        ingestor = DocumentIngestor()
        
        # Construir filtro de metadata
        metadata_filter = {}
        if asignatura:
            metadata_filter["asignatura"] = asignatura
        if tema:
            metadata_filter["tema"] = tema
        if nivel:
            metadata_filter["nivel"] = nivel
        if curso:
            metadata_filter["curso"] = curso
        
        # Realizar búsqueda
        try:
            if metadata_filter:
                results = ingestor.vectorstore.similarity_search_with_score(
                    query=query, k=num_results, filter=metadata_filter
                )
            else:
                results = ingestor.vectorstore.similarity_search_with_score(
                    query=query, k=num_results
                )
        except Exception:
            # Fallback a búsqueda normal
            results = ingestor.vectorstore.similarity_search_with_score(
                query=query, k=num_results
            )
        
        if not results:
            return f"No se encontraron documentos para '{query}' con los filtros aplicados."
        
        # Convertir a formato de similaridad
        formatted_results = []
        for doc, score in results:
            similarity = 1 - score if score <= 1 else 1 / (1 + score)
            formatted_results.append((doc, similarity))
        
        return _format_results(formatted_results, query)
        
    except Exception as e:
        logger.error(f"❌ Error en búsqueda filtrada: {str(e)}")
        return f"Error en búsqueda filtrada: {str(e)}"

class RagAgent(BaseToolCallingAgent):
    def __init__(self, use_multiagent_mode: bool = False):
        # Seleccionar prompt según contexto
        prompt = RAG_AGENT_MULTIAGENT_PROMPT if use_multiagent_mode else RAG_AGENT_PROMPT
        goal = ("Buscar información factual básica de forma rápida y concisa" 
                if use_multiagent_mode else 
                "Tu objetivo es buscar en la base de conocimientos información que solicite el usuario usando técnicas de RAG.")
        
        super().__init__(
            name="RagAgent",
            goal=goal,
            prompt_template=prompt,
            tools=[search_knowledge_base, search_by_metadata_filter]
        )