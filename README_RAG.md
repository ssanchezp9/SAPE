# 🛠️ Herramientas RAG y Métodos de Consulta

Este documento describe las herramientas de recuperación de información utilizadas en SAPE y cómo se integran en el agente RAG.

## 1. Ingesta de Documentos

La clase `DocumentIngestor` se encarga de procesar archivos y almacenarlos en la base de datos vectorial `pgvector`. Utiliza `OpenAIEmbeddings` para generar los vectores y `RecursiveCharacterTextSplitter` para dividir los textos.

```python
# src/utils/rag/document_ingestor.py
... (ver líneas 18‑46 y 48‑67)
```

El método `ingest` admite metadatos opcionales que permiten filtrar por asignatura, tema o nivel educativo.

## 2. Búsqueda en la Base de Conocimientos

Dentro de `a_it_rag_agent.py` se definen dos herramientas con el decorador `@tool` de LangChain:

- **`search_knowledge_base`**: realiza una búsqueda por similitud y filtra los resultados según un umbral de relevancia.
- **`search_by_metadata_filter`**: permite añadir filtros de metadata como asignatura, tema o curso.

```python
# src/agents/a_it_rag_agent.py
... (ver líneas 11‑50 y 74‑142)
```

Ambas funciones devuelven un texto formateado con las fuentes encontradas. Estas herramientas se registran en `RagAgent`, una subclase de `BaseToolCallingAgent` que puede invocarlas durante la conversación:

```python
# src/agents/a_it_rag_agent.py
... (ver líneas 144‑157)
```

## 3. Uso desde los Planificadores

Los planificadores que requieren investigación delegan en `RagAgent` las consultas necesarias. De esta forma, el resto de agentes recibe la información relevante ya filtrada y puede centrarse en generar el contenido solicitado.

Al compartir la misma memoria de conversación, los resultados recuperados quedan disponibles para pasos posteriores del plan.

