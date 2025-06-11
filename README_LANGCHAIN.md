# 📚 Integración de LangChain y Gestión de Agentes con LangGraph

Este documento detalla cómo se emplean las funcionalidades de LangChain en el proyecto y la forma en la que se coordina el sistema multi‑agente mediante LangGraph.

## 1. Estructura de Agentes

Los agentes del sistema heredan de `BaseAgent`, que encapsula la lógica común para interactuar con el modelo de lenguaje y la memoria de conversación. El método `run` prepara los mensajes, incorpora el historial reciente y guarda cada turno en la memoria:

```python
# src/agents/base_agent.py
... (ver líneas 32‑84)
```

Los agentes especializados (por ejemplo `ConceptMapAgent`, `LessonPlanAgent`, etc.) simplemente proporcionan un `prompt_template` y un objetivo.

Para agentes que necesitan invocar herramientas externas se extiende `BaseToolCallingAgent`. Esta clase utiliza `create_tool_calling_agent` y `AgentExecutor` de LangChain para manejar la ejecución de herramientas declaradas mediante `BaseTool`:

```python
# src/agents/base_tool_calling_agent.py
... (ver líneas 24‑39 y 66‑97)
```

## 2. Planificadores

Los distintos planificadores heredan de `BasePlanner`. Esta clase usa `ChatOpenAI` combinado con `with_structured_output` para generar un plan estructurado (`Plan`) con los pasos a realizar. Después ejecuta secuencialmente cada paso delegándolo al agente correspondiente:

```python
# src/agents/base_planner.py
... (ver líneas 36‑88 y 138‑173)
```

Cada planificador concreto define su objetivo y los agentes que lo componen. La orquestación garantiza que todos ellos compartan la misma memoria de conversación cuando esta se encuentra habilitada.

## 3. Coordinación con LangGraph

El componente de alto nivel es `SwarmMaster`, encargado de seleccionar el planificador adecuado y mantener un registro centralizado de la conversación. Se apoya en la inicialización definida en `start_app.py` y utiliza elementos de LangGraph como `StateGraph` para estructurar el flujo de ejecución:

```python
# src/agents/swarm_master.py
... (ver líneas 1‑34 y 52‑83)
```

Aunque el grafo se mantiene simple, esta integración permite ampliar el sistema con flujos más complejos si fuese necesario.

## 4. Inicialización de Componentes

El módulo `start_app.py` construye todos los agentes, planificadores y modelos LLM. También configura la memoria y genera mapas de acceso rápido para las invocaciones posteriores.

La función `initialize_swarm_master` devuelve un diccionario con todos estos elementos listos para ser usados por `SwarmMaster`.

Con esta arquitectura, LangChain se emplea para la gestión de prompts, herramientas y planes, mientras que LangGraph proporciona el marco para coordinar a los agentes de manera modular.

