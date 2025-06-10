# 🎓 SAPE - Sistema Avanzado de Planificación Educativa

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Descripción

**SAPE** es un sistema inteligente de planificación educativa que utiliza agentes de IA especializados y técnicas RAG (Retrieval-Augmented Generation) para crear contenido educativo personalizado y de alta calidad.

### 🎯 Características Principales

- **🤖 Sistema Multi-Agente**: Agentes especializados en diferentes tareas educativas
- **📚 RAG Educativo**: Base de conocimientos con documentos específicos por materia y nivel
- **🎨 Múltiples Formatos**: Resúmenes, guías de estudio, lecciones, mapas conceptuales
- **🎓 Adaptación por Niveles**: Contenido desde Primaria hasta Bachillerato
- **💬 Interfaz Intuitiva**: Chat web con Gradio y API REST
- **📊 Planificación Inteligente**: Coordinación automática de agentes según la tarea

## 🏗️ Arquitectura del Sistema

### 🤖 Agentes Especializados

| Agente | Función | Especialización |
|--------|---------|----------------|
| **RagAgent** | Búsqueda de información | Recuperación inteligente de contenido educativo |
| **StudyGuideAgent** | Guías de estudio | Estructuración pedagógica de contenidos |
| **LessonPlanAgent** | Planes de clase | Diseño de lecciones con objetivos y actividades |
| **TestGeneratorAgent** | Evaluaciones | Creación de pruebas y ejercicios |
| **ConceptMapAgent** | Mapas conceptuales | Representación visual de conocimientos |
| **EssayPlanAgent** | Planes de ensayo | Estructuración de textos académicos |
| **ResumidorAgent** | Síntesis | Resúmenes y síntesis de información |

### 📋 Planificadores Multi-Agente

| Planificador | Agentes Utilizados | Objetivo |
|--------------|-------------------|----------|
| **DetailedStudyGuidePlanner** | RAG + Resumidor + StudyGuide | Guías exhaustivas de estudio |
| **LessonWithEvaluationPlanner** | RAG + LessonPlan + TestGenerator | Lecciones con evaluación |
| **MultiFormatReviewPlanner** | RAG + StudyGuide + ConceptMap | Material de repaso multiformato |
| **EssayWritingAssistantPlanner** | RAG + Resumidor + ConceptMap + EssayPlan | Asistencia integral para ensayos |
| **SimpleResumePlanner** | Resumidor | Resúmenes directos y concisos |

## 📚 Base de Conocimientos

El sistema incluye documentos educativos organizados por:

### 🎒 **Primaria**
- Ortografía (5º)
- Fracciones matemáticas (6º)
- Ecosistemas (6º)
- Edad Media (5º)
- Present Simple inglés (6º)

### 🏫 **ESO**
- Ecuaciones matemáticas (2º)
- Sintaxis lengua (3º)
- Física y química (2º)
- Biología celular (1º)
- Revolución Francesa (4º)

### 🎓 **Bachillerato**
- Comentario de texto (1º)
- Derivadas matemáticas (2º)
- Cinemática física (1º)
- Enlaces químicos (2º)
- Filosofía de Sócrates (1º)

## 🚀 Instalación y Configuración

### 📋 Prerrequisitos

- Python 3.8 o superior
- PostgreSQL con extensión pgvector
- API Key de OpenAI

### 🔧 Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd UAX_SAPE_API
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env con:
OPENAI_API_KEY=tu_api_key_de_openai
DATABASE_URL=postgresql://usuario:password@localhost:5432/sape_db
```

5. **Configurar base de datos**
```bash
# Crear base de datos PostgreSQL con pgvector
python ingest.py  # Procesar documentos educativos
```

## 🎮 Uso del Sistema

### 🖥️ Interfaz Web (Gradio)

```bash
python gradio_chat.py
```
Accede a `http://localhost:7860` para la interfaz de chat interactiva.

### 🔌 API REST

```bash
python api_server.py
```
API disponible en `http://localhost:8000`

#### Endpoints principales:

```bash
POST /chat
{
  "message": "Crear guía de estudio sobre ecuaciones para 2º ESO",
  "conversation_id": "optional"
}
```

### 🚀 Inicio Rápido (Windows)

```bash
# Ejecutar todos los servicios
inicio_rapido.bat

# Solo chat
iniciar_sape.bat
```

## 💡 Ejemplos de Uso

### 📖 Crear Guía de Estudio
```
"Crear una guía completa sobre derivadas para Bachillerato 2º usando tema12_mates_derivadas_bach2.docx"
```

### 🎓 Lección con Evaluación
```
"Diseñar una lección sobre fracciones para 6º Primaria con ejercicios de evaluación"
```

### 🎨 Material Multiformato
```
"Crear material de repaso sobre la Revolución Francesa: guía textual + mapa conceptual"
```

### ✍️ Asistencia para Ensayos
```
"Ayudar a escribir ensayo sobre la filosofía de Sócrates con investigación y estructura"
```

## 🛠️ Configuración Avanzada

### ⚙️ Parámetros del LLM

Los agentes y planificadores permiten configuración centralizada:

```python
# Ejemplo de configuración personalizada
planner = DetailedStudyGuidePlanner(
    agents=agents,
    temperature=0.4,
    max_tokens=12000,
    model="gpt-4o-mini"
)
```

### 📊 Métricas de Rendimiento

- **Tokens promedio por respuesta**: 3000-8000
- **Tiempo de respuesta**: 15-45 segundos
- **Agentes coordinados**: 2-4 por consulta compleja

## 📁 Estructura del Proyecto

```
UAX_SAPE_API/
├── src/
│   ├── agents/           # Agentes especializados
│   │   ├── base_agent.py
│   │   ├── base_planner.py
│   │   ├── a_*.py        # Agentes individuales
│   │   ├── pn_*.py       # Planificadores
│   │   └── prompts/      # Prompts especializados
│   ├── models/           # Modelos de datos
│   └── utils/            # Utilidades (DB, logging, RAG)
├── gradio_chat.py        # Interfaz web
├── api_server.py         # Servidor API
├── ingest.py            # Procesador de documentos
├── requirements.txt     # Dependencias
└── README.md           # Documentación
```

## 🔧 Desarrollo

### 🧪 Ejecutar Tests
```bash
python -m pytest tests/
```

### 📝 Añadir Nuevos Documentos
1. Colocar archivos .docx en `DOCUMENTOS_RAG/`
2. Ejecutar `python ingest.py`
3. Documentos procesados automáticamente

### 🤖 Crear Nuevo Agente
```python
from src.agents.base_agent import BaseAgent

class MiNuevoAgente(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MiNuevoAgente",
            goal="Objetivo específico",
            prompt_template="Prompt especializado"
        )
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**SAPE Development Team**
- 📧 Email: [contacto@sape.edu]
- 🌐 Website: [https://sape.edu]

## 🙏 Agradecimientos

- OpenAI por GPT-4
- LangChain por el framework de agentes
- Gradio por la interfaz de usuario
- PostgreSQL y pgvector por la base de datos vectorial

---

⭐ **¡Dale una estrella si este proyecto te resulta útil!** ⭐
