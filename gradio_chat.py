"""
Interfaz de chat simple con Gradio para interactuar con la plataforma SAPE
"""

import gradio as gr
import requests
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL del API server (ajustar si es necesario)
API_URL = "http://localhost:8000"

# Variable global para almacenar el ID de conversación
conversation_id = None

def send_suggested_prompt(prompt):
    """
    Función que envía un prompt sugerido al chat
    """
    return prompt

def chat_with_sape(message, history):
    """
    Función que maneja el chat con la plataforma SAPE
    """
    global conversation_id
    
    try:
        # Preparar la petición
        payload = {
            "message": message,
            "conversation_id": conversation_id
        }
        
        # Hacer la petición al API
        response = requests.post(f"{API_URL}/chat", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            conversation_id = result["conversation_id"]
            bot_response = result["response"]
            
            # Agregar el mensaje del usuario y la respuesta del bot al historial
            history.append([message, bot_response])
            
            logger.info(f"Chat exitoso en conversación: {conversation_id}")
            return history, ""
            
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            history.append([message, f"❌ Error: {error_msg}"])
            logger.error(f"Error en API: {error_msg}")
            return history, ""
            
    except requests.exceptions.ConnectionError:
        error_msg = "No se puede conectar con el servidor. ¿Está ejecutándose el API server?"
        history.append([message, f"❌ {error_msg}"])
        logger.error(error_msg)
        return history, ""
        
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        history.append([message, f"❌ {error_msg}"])
        logger.error(f"Error inesperado: {e}")
        return history, ""

def clear_chat():
    """
    Función para limpiar el chat e iniciar una nueva conversación
    """
    global conversation_id
    conversation_id = None
    logger.info("Chat limpiado, nueva conversación iniciada")
    return [], ""

# Crear la interfaz con Gradio
with gr.Blocks(
    title="SAPE Chat",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 800px !important;
        margin: auto !important;
    }
    """
) as demo:
      # Título y descripción
    gr.Markdown(
        """
        # 💬 Chat con SAPE
        
        Interfaz simple para conversar con la plataforma SAPE.
        Escribe tu mensaje y presiona Enter o haz clic en Enviar.
        
        ## 📚 Prompts Sugeridos por Categoría
        Haz clic en cualquier sugerencia para enviarla automáticamente.
        """
    )
    
    # Prompts sugeridos organizados por categoría
    with gr.Tabs():
        # Tab para Resúmenes Simples
        with gr.TabItem("📄 Resúmenes"):
            gr.Markdown("### Resúmenes directos y concisos")
            with gr.Row():
                resume_btn1 = gr.Button("🔢 Ecuaciones matemáticas 2º ESO", size="sm")
                resume_btn2 = gr.Button("🏰 Revolución Francesa 4º ESO", size="sm")
            with gr.Row():
                resume_btn3 = gr.Button("🧬 La célula - Biología 1º ESO", size="sm")
                resume_btn4 = gr.Button("⚛️ Estados de la materia 2º ESO", size="sm")
        
        # Tab para Primaria
        with gr.TabItem("🎒 Primaria"):
            gr.Markdown("### Contenidos específicos de Primaria")
            with gr.Row():
                primary_btn1 = gr.Button("✍️ Ortografía 5º Primaria", size="sm")
                primary_btn2 = gr.Button("🔢 Fracciones 6º Primaria", size="sm")
            with gr.Row():
                primary_btn3 = gr.Button("🌿 Ecosistemas 6º Primaria", size="sm")
                primary_btn4 = gr.Button("🏰 Edad Media 5º Primaria", size="sm")
            with gr.Row():
                primary_btn5 = gr.Button("🇬🇧 Present Simple 6º Primaria", size="sm")
        
        # Tab para Guías de Estudio Detalladas
        with gr.TabItem("📖 Guías de Estudio"):
            gr.Markdown("### Guías completas con investigación y síntesis")
            with gr.Row():
                guide_btn1 = gr.Button("🧮 Derivadas - Matemáticas Bach 2º", size="sm")
                guide_btn2 = gr.Button("⚗️ Enlaces químicos Bach 2º", size="sm")
            with gr.Row():
                guide_btn3 = gr.Button("🏛️ Filosofía de Sócrates Bach 1º", size="sm")
                guide_btn4 = gr.Button("� Cinemática - Física Bach 1º", size="sm")
        
        # Tab para Lecciones con Evaluación
        with gr.TabItem("🎓 Lecciones + Evaluación"):
            gr.Markdown("### Lecciones completas con actividades de evaluación")
            with gr.Row():
                lesson_btn1 = gr.Button("� Fracciones 6º Primaria + ejercicios", size="sm")
                lesson_btn2 = gr.Button("� Ecosistemas 6º Primaria + actividades", size="sm")
            with gr.Row():
                lesson_btn3 = gr.Button("🇬🇧 Present Simple 6º Primaria + práctica", size="sm")
                lesson_btn4 = gr.Button("✍️ Ortografía 5º Primaria + dictados", size="sm")
        
        # Tab para Material Multiformato
        with gr.TabItem("🎨 Repaso Multiformato"):
            gr.Markdown("### Material visual y textual complementario")
            with gr.Row():
                multi_btn1 = gr.Button("📝 Sintaxis 3º ESO - Guía + esquemas", size="sm")
                multi_btn2 = gr.Button("� Edad Media 5º Primaria - Visual", size="sm")
            with gr.Row():
                multi_btn3 = gr.Button("📖 Comentario texto Bach 1º - Método", size="sm")
                multi_btn4 = gr.Button("🌍 Ecosistemas - Mapas conceptuales", size="sm")
        
        # Tab para Asistente de Ensayos
        with gr.TabItem("✍️ Asistente de Ensayos"):
            gr.Markdown("### Ayuda integral para redacción académica")
            with gr.Row():
                essay_btn1 = gr.Button("� Ensayo: Filosofía de Sócrates", size="sm")
                essay_btn2 = gr.Button("�️ Análisis: Revolución Francesa", size="sm")
            with gr.Row():
                essay_btn3 = gr.Button("🔬 Redacción científica: La célula", size="sm")
                essay_btn4 = gr.Button("📝 Comentario de texto literario", size="sm")
    
    # Componente de chat
    chatbot = gr.Chatbot(
        label="Conversación",
        height=500,
        show_label=False,
        avatar_images=("👤", "🤖"),
        bubble_full_width=False
    )
    
    # Entrada de texto
    msg = gr.Textbox(
        label="Tu mensaje",
        placeholder="Escribe tu mensaje aquí...",
        lines=1,
        max_lines=3,
        show_label=False
    )
    
    # Botones
    with gr.Row():
        send_btn = gr.Button("📤 Enviar", variant="primary")
        clear_btn = gr.Button("🗑️ Limpiar Chat", variant="secondary")
    
    # Estado de la conversación
    gr.Markdown("---")
    with gr.Row():
        status = gr.Markdown("🟡 **Estado:** Listo para chatear")
    
    # Configurar eventos
    msg.submit(
        fn=chat_with_sape,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )
    
    send_btn.click(
        fn=chat_with_sape,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )    
    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot, msg]
    )      # Configurar eventos para botones de prompts sugeridos
    # Resúmenes    resume_btn1.click(fn=lambda: "Crear un resumen completo sobre ecuaciones matemáticas para 2º ESO basado en el tema2_mates_ecuaciones_eso2.docx. Incluye tipos de ecuaciones, métodos de resolución y ejemplos prácticos.", outputs=msg)
    resume_btn2.click(fn=lambda: "Resumir la Revolución Francesa para 4º ESO usando el contenido de tema10_ghist_revfrancesa_eso4.docx. Incluye causas, etapas principales, personajes clave y consecuencias.", outputs=msg)
    resume_btn3.click(fn=lambda: "Crear un resumen sobre la célula para 1º ESO basado en tema9_biogeo_celula_eso1.docx. Incluye tipos celulares, orgánulos y funciones básicas.", outputs=msg)
    resume_btn4.click(fn=lambda: "Resumir los estados de la materia para 2º ESO usando tema8_fyq_materia_eso2.docx. Incluye propiedades, cambios de estado y ejemplos cotidianos.", outputs=msg)
    
    # Primaria
    primary_btn1.click(fn=lambda: "Crear una guía completa sobre ortografía para 5º Primaria basado en tema1_lengua_ortografia_primaria5.docx. Incluye reglas ortográficas principales, ejemplos y ejercicios prácticos.", outputs=msg)
    primary_btn2.click(fn=lambda: "Diseñar una lección sobre fracciones para 6º Primaria basado en tema2_mates_fracciones_primaria6.docx. Incluye conceptos básicos, tipos de fracciones, operaciones y ejercicios resueltos.", outputs=msg)
    primary_btn3.click(fn=lambda: "Crear material educativo sobre ecosistemas para 6º Primaria basado en tema3_cnat_ecosistemas_primaria6.docx. Incluye componentes, tipos de ecosistemas, cadenas alimentarias y ejemplos.", outputs=msg)
    primary_btn4.click(fn=lambda: "Desarrollar contenido sobre la Edad Media para 5º Primaria basado en tema4_csoc_edadmedia_primaria5.docx. Incluye características, sociedad feudal, castillos y legado histórico.", outputs=msg)
    primary_btn5.click(fn=lambda: "Crear lección sobre el Present Simple para 6º Primaria basado en tema5_ingles_present_primaria6.docx. Incluye estructura, uso, vocabulario y ejercicios prácticos.", outputs=msg)
    # Guías de Estudio
    guide_btn1.click(fn=lambda: "Crear una guía de estudio completa sobre derivadas para Bachillerato 2º usando tema12_mates_derivadas_bach2.docx. Incluye conceptos, reglas de derivación, aplicaciones y ejercicios resueltos paso a paso.", outputs=msg)
    guide_btn2.click(fn=lambda: "Desarrollar una guía detallada sobre enlaces químicos para Bachillerato 2º basada en tema14_quimica_enlace_bach2.docx. Incluye tipos de enlaces, propiedades, ejemplos y ejercicios prácticos.", outputs=msg)
    guide_btn3.click(fn=lambda: "Crear guía de estudio sobre la filosofía de Sócrates para Bachillerato 1º usando tema15_filo_socrates_bach1.docx. Incluye biografía, método socrático, ideas principales y su influencia.", outputs=msg)
    guide_btn4.click(fn=lambda: "Guía completa de cinemática para Bachillerato 1º basada en tema13_fisica_cinematica_bach1.docx. Incluye conceptos, ecuaciones, tipos de movimiento y resolución de problemas.", outputs=msg)
      # Lecciones con Evaluación
    lesson_btn1.click(fn=lambda: "Diseñar una lección completa sobre fracciones para 6º Primaria usando tema2_mates_fracciones_primaria6.docx. Incluye conceptos, operaciones, problemas prácticos y evaluación con ejercicios.", outputs=msg)
    lesson_btn2.click(fn=lambda: "Crear lección sobre ecosistemas para 6º Primaria basada en tema3_cnat_ecosistemas_primaria6.docx. Incluye tipos, componentes, cadenas alimentarias y actividades de evaluación.", outputs=msg)
    lesson_btn3.click(fn=lambda: "Lección de Present Simple para 6º Primaria usando tema5_ingles_present_primaria6.docx. Incluye formación, usos, vocabulario y ejercicios de práctica evaluativos.", outputs=msg)
    lesson_btn4.click(fn=lambda: "Lección de ortografía para 5º Primaria basada en tema1_lengua_ortografia_primaria5.docx. Incluye reglas ortográficas, ejemplos y dictados de evaluación.", outputs=msg)
      # Material Multiformato
    multi_btn1.click(fn=lambda: "Crear material de repaso sobre sintaxis para 3º ESO usando tema6_lengua_sintaxis_eso3.docx. Incluye guía textual estructurada + esquemas visuales de análisis sintáctico con ejemplos.", outputs=msg)
    multi_btn2.click(fn=lambda: "Desarrollar material completo sobre la Edad Media para 5º Primaria basado en tema4_csoc_edadmedia_primaria5.docx. Incluye guía de estudio + mapa conceptual visual de sociedad feudal.", outputs=msg)
    multi_btn3.click(fn=lambda: "Material de comentario de texto para Bachillerato 1º usando tema11_lengua_comentario_bach1.docx. Incluye metodología textual + esquemas visuales del proceso de análisis.", outputs=msg)
    multi_btn4.click(fn=lambda: "Crear material diverso sobre ecosistemas usando tema3_cnat_ecosistemas_primaria6.docx. Incluye guía con características + mapa conceptual con cadenas alimentarias.", outputs=msg)
      # Asistente de Ensayos
    essay_btn1.click(fn=lambda: "Asistir en la redacción de un ensayo sobre la filosofía de Sócrates para Bachillerato usando tema15_filo_socrates_bach1.docx. Incluye investigación, argumentos principales, estructura y plan de redacción.", outputs=msg)
    essay_btn2.click(fn=lambda: "Ayudar a escribir ensayo sobre la Revolución Francesa usando tema10_ghist_revfrancesa_eso4.docx. Incluye análisis de causas, desarrollo histórico y estructura argumentativa.", outputs=msg)
    essay_btn3.click(fn=lambda: "Asistir en redacción científica sobre la célula usando tema9_biogeo_celula_eso1.docx. Incluye investigación de estructuras, organización de ideas y metodología científica.", outputs=msg)
    essay_btn4.click(fn=lambda: "Ayuda para comentario de texto literario usando tema11_lengua_comentario_bach1.docx. Incluye metodología de análisis, estructura del comentario y técnicas de redacción.", outputs=msg)
    
    
if __name__ == "__main__":
    print("🚀 Iniciando interfaz de chat SAPE...")
    print("📝 Asegúrate de que el API server esté ejecutándose en http://localhost:8000")
    print("🌐 La interfaz se abrirá en tu navegador...")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True
    )
