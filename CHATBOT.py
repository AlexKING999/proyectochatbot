import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Chatbot ISTA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Updated Design) ---
st.markdown("""
<style>
    /* Colores institucionales mejorados */
    :root {
        --primary-blue: #2563eb;     /* Azul más claro y vibrante */
        --secondary-blue: #1e40af;   /* Azul medio */
        --dark-blue: #1e3a8a;        /* Azul oscuro */
        --accent-yellow: #fbbf24;    /* Amarillo institucional */
        --bright-yellow: #f59e0b;    /* Amarillo más intenso */
        --light-bg: #f8fafc;         /* Fondo claro */
        --white: #ffffff;
        --text-dark: #1e293b;
        --border-light: #e2e8f0;
    }

    /* Fondo principal con gradiente institucional */
    .stApp {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 50%, var(--accent-yellow) 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    /* Overlay para el fondo */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(248, 250, 252, 0.95);
        z-index: -1;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--secondary-blue) 50%, var(--accent-yellow) 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.3);
        border: 2px solid var(--accent-yellow);
    }
    
    .main-header h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 10px;
        font-size: 2.2rem;
    }
    
    /* Contenedor del logo */
    .header-logo-container {
        text-align: center;
        padding: 25px;
        margin-bottom: 25px;
        background: var(--white);
        border-radius: 15px;
        box-shadow: 0 6px 25px rgba(37, 99, 235, 0.15);
        border: 3px solid var(--accent-yellow);
    }
    
    /* Contenedor del video */
    .video-container {
        text-align: center;
        padding: 25px;
        background: var(--white);
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 6px 25px rgba(37, 99, 235, 0.15);
        border: 2px solid var(--border-light);
    }
    
    /* NUEVO: Contenedor principal del chat centralizado */
    .chat-main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* NUEVO: Área de conversación con scroll */
    .chat-conversation-area {
        background: var(--white);
        border-radius: 15px;
        border: 3px solid var(--accent-yellow);
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.2);
        margin-bottom: 20px;
        overflow: hidden;
    }
    
    .chat-header {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-yellow) 100%);
        color: white;
        padding: 15px 25px;
        font-weight: bold;
        font-size: 1.1rem;
        border-bottom: 2px solid var(--bright-yellow);
    }
    
    .chat-messages-container {
        height: 400px;
        overflow-y: auto;
        padding: 20px;
        background: var(--light-bg);
        scrollbar-width: thin;
        scrollbar-color: var(--accent-yellow) var(--border-light);
    }
    
    /* Webkit scrollbar styling */
    .chat-messages-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-messages-container::-webkit-scrollbar-track {
        background: var(--border-light);
        border-radius: 4px;
    }
    
    .chat-messages-container::-webkit-scrollbar-thumb {
        background: var(--accent-yellow);
        border-radius: 4px;
    }
    
    .chat-messages-container::-webkit-scrollbar-thumb:hover {
        background: var(--bright-yellow);
    }
    
    /* NUEVO: Área de controles del chat */
    .chat-controls-area {
        background: var(--white);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid var(--primary-blue);
        box-shadow: 0 6px 25px rgba(37, 99, 235, 0.15);
    }
    
    /* Mensajes del bot mejorados */
    .bot-message {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(251, 191, 36, 0.1) 100%);
        padding: 18px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid var(--primary-blue);
        box-shadow: 0 3px 15px rgba(37, 99, 235, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Mensajes del usuario mejorados */
    .user-message {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(255, 255, 255, 0.95) 100%);
        padding: 18px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: right;
        border-right: 5px solid var(--accent-yellow);
        box-shadow: 0 3px 15px rgba(251, 191, 36, 0.2);
        animation: slideInRight 0.3s ease-out;
    }
    
    /* Animaciones */
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Botones mejorados */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        border: 2px solid var(--accent-yellow);
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--dark-blue) 100%);
        border-color: var(--bright-yellow);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }
    
    /* Cajas de información */
    .info-box {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(251, 191, 36, 0.08) 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid var(--accent-yellow);
        margin: 20px 0;
        box-shadow: 0 6px 25px rgba(37, 99, 235, 0.1);
    }
    
    /* Títulos */
    h1, h2, h3, h4 {
        color: var(--dark-blue);
    }
    
    /* Sidebar personalizada */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--white) 0%, var(--light-bg) 100%);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-yellow) 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 40px;
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.3);
    }
    
    /* Formularios */
    .stTextInput > div > div > input {
        border: 2px solid var(--border-light);
        border-radius: 8px;
        padding: 10px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
    }
    
    /* Alertas de Streamlit */
    .stInfo {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(251, 191, 36, 0.1) 100%);
        border: 2px solid var(--accent-yellow);
        border-radius: 10px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .chat-main-container {
            padding: 0 10px;
        }
        
        .chat-messages-container {
            height: 300px;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_career_data():
    data = {
        'Carreras': ['TECNOLOGIA SUPERIOR EN BIG DATA', 'TECNOLOGIA SUPERIOR EN CIBERSEGURIDAD', 'TECNOLOGÍA SUPERIOR EN TRIBUTACIÓN', 'TECNOLOGÍA SUPERIOR EN PRODUCCIÓN Y REALIZACIÓN AUDIOVISUAL', 'TECNOLOGÍA SUPERIOR EN SEGURIDAD Y PREVENCIÓN DE RIESGOS LABORALES', 'TECNOLOGÍA SUPERIOR EN GESTIÓN DEL PATRIMONIO HISTÓRICO CULTURAL', 'TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE', 'ENTRENAMIENTO DEPORTIVO CON NIVEL EQUIVALENTE A TECNOLOGÍA SUPERIOR', 'TECNOLOGÍA SUPERIOR EN METALMECÁNICA', 'TECNOLOGÍA SUPERIOR EN MANTENIMIENTO ELÉCTRICO Y CONTROL INDUSTRIAL', 'TECNOLOGÍA SUPERIOR EN MECATRÓNICA', 'TECNOLOGÍA SUPERIOR EN ADMINISTRACIÓN DE INFRAESTRUCTURA Y PLATAFORMAS TECNOLÓGICAS', 'TECNOLOGÍA SUPERIOR EN CONTABILIDAD'],
        'Modalidad': ['Presencial', 'Presencial', 'Presencial', 'Presencial', 'Presencial', 'Presencial', 'Presencial', 'Presencial', 'Duales', 'Duales', 'Duales', 'Híbridas', 'En línea'],
        'Duracion': ['4 Niveles', '4 Niveles', '5 Niveles', '5 Niveles', '5 Semestres', '4 Niveles', '5 Niveles', '5 Niveles', '4 Niveles', '4 Niveles', '5 Niveles', '4 Niveles', '4 Ciclos Académicos'],
        'Jornada': ['Matutina', 'Vespertina', 'Matutina', 'Matutina', 'Matutina-Vespertina', 'Vespertina', 'Matutina', 'Matutina', 'Matutina', 'Vespertina', 'Vespertina-Nocturna', 'Matutina', 'Nocturna'],
        'Año': ['2 años', '2 años', '2,5 años', '2,5 años', '2,5 años', '2 años', '2,5 años', '2,5 años', '2 años', '2 años', '2,5 años', '2 años', '2 años'],
        'titulo_al_obtener': ['Tecnólogo/a Superior en Big Data', 'Tecnología Superior en Tributación', 'Tecnólogo/a Superior en Ciberseguridad', 'Productor y Realizador Audiovisual con nivel equivalente a Tecnología Superior', 'Tecnólogo/a Superior en Seguridad y Prevención de Riesgos Laborales', 'Tecnólogo/a Superior en Gestión del Patrimonio Histórico', 'Tecnólogo/a Superior en Desarrollo de Software', 'Entrenador/a Deportivo con Nivel Equivalente a Tecnología Superior', 'Tecnólogo/a Superior en Metalmecánica', 'Tecnología Superior en Mantenimiento Eléctrico y Control Industrial', 'Tecnólogo/a Superior en Mecatrónica', 'Tecnólogo/a Superior en Administración de Infraestructura y Plataformas Tecnológicas', 'Tecnólogo Superior en Contabilidad']
    }
    return pd.DataFrame(data)

# --- Session State Initialization ---
def initialize_state():
    if 'conversation_state' not in st.session_state:
        st.session_state.conversation_state = 'inicio'
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_career' not in st.session_state:
        st.session_state.selected_career = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

initialize_state()

# --- Helper Functions ---
def add_message(sender, message):
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({'sender': sender, 'message': message, 'timestamp': timestamp})

def display_chat():
    messages_html = ""
    for chat in st.session_state.chat_history:
        css_class = "bot-message" if chat['sender'] == 'bot' else "user-message"
        icon = "🤖" if chat['sender'] == 'bot' else "👤"
        name = "Asistente ISTA" if chat['sender'] == 'bot' else "Tú"
        messages_html += f"""
        <div class="{css_class}">
            {icon} <strong style="color: var(--dark-blue);">{name}</strong> 
            <span style="color: #64748b; font-size: 0.85rem;">- {chat['timestamp']}</span><br><br>
            {chat['message']}
        </div>
        """
    
    st.markdown(f"""
    <div class="chat-messages-container">
        {messages_html}
    </div>
    """, unsafe_allow_html=True)

def show_enrollment_info():
    st.markdown("""
    <div class="info-box">
        <h3 style="color: var(--dark-blue);">📋 Proceso de Matrícula - ISTA</h3>
        <p><strong>Requisitos generales:</strong></p>
        <ul>
            <li>Título de bachiller en Ciencias o su equivalente</li>
            <li>Cédula de identidad y certificado de votación</li>
            <li>Certificado médico</li>
            <li>2 fotos tamaño carnet</li>
        </ul>
        <p><strong>📅 Fechas importantes:</strong> Consulta nuestro cronograma académico</p>
        <p><strong>💰 Costo:</strong> ¡Completamente GRATUITO!</p>
    </div>
    """, unsafe_allow_html=True)

# --- UI Layout ---
df_careers = load_career_data()

# Header: Logo y Video
st.markdown('<div class="header-logo-container">', unsafe_allow_html=True)
st.image("https://www.tecazuay.edu.ec/wp-content/uploads/2023/07/LOGO-RECTANGULAR_SIN-FONDO.png", width=500)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="video-container">
    <h3 style="color: var(--dark-blue);">🎬 Conoce más sobre ISTA</h3>
    <iframe src="https://www.facebook.com/plugins/video.php?height=314&href=https%3A%2F%2Fwww.facebook.com%2Fshare%2Fv%2F1BWufsCwHj%2F&show_text=false&width=560&t=0" 
            width="100%" height="300" style="border:none;overflow:hidden;border-radius:10px;" 
            scrolling="no" frameborder="0" allowfullscreen="true" 
            allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share">
    </iframe>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎓 Chatbot - Instituto Tecnológico del Azuay</h1>
    <p style="font-size: 18px; margin: 0;">Tu asistente virtual para información sobre matrículas e inscripciones</p>
</div>
""", unsafe_allow_html=True)

# Layout principal con chat centralizado
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="chat-main-container">', unsafe_allow_html=True)
    
    # Área de conversación con scroll
    st.markdown("""
    <div class="chat-conversation-area">
        <div class="chat-header">
            💬 Conversación con el Asistente ISTA
        </div>
    """, unsafe_allow_html=True)
    
    # Mostrar mensajes si existen
    if st.session_state.chat_history:
        display_chat()
    else:
        st.markdown("""
        <div class="chat-messages-container">
            <div class="bot-message">
                🤖 <strong style="color: var(--dark-blue);">Asistente ISTA</strong><br><br>
                ¡Hola! 👋 Soy tu asistente virtual del ISTA. ¿En qué puedo ayudarte hoy?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Área de controles
    st.markdown('<div class="chat-controls-area">', unsafe_allow_html=True)
    
    # --- Lógica del Chatbot ---
    state = st.session_state.conversation_state

    if state == 'inicio':
        if not st.session_state.chat_history:
            add_message('bot', "¡Hola! 👋 Soy tu asistente virtual del ISTA. ¿En qué puedo ayudarte hoy?")
        
        st.subheader("🎯 Selecciona una opción:")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📚 Ver Carreras Disponibles", use_container_width=True):
                add_message('user', 'Quiero ver las carreras disponibles')
                st.session_state.conversation_state = 'carreras'
                st.rerun()
            if st.button("📋 Proceso de Matrícula", use_container_width=True):
                add_message('user', 'Quiero info sobre matrícula')
                st.session_state.conversation_state = 'matricula'
                st.rerun()
        
        with col_b:
            if st.button("🕐 Horarios y Modalidades", use_container_width=True):
                add_message('user', 'Quiero ver horarios y modalidades')
                st.session_state.conversation_state = 'horarios'
                st.rerun()
            if st.button("📞 Información de Contacto", use_container_width=True):
                add_message('user', 'Necesito info de contacto')
                st.session_state.conversation_state = 'contacto'
                st.rerun()

    elif state == 'carreras':
        add_message('bot', 'Aquí tienes nuestras carreras. Selecciona una para más detalles:')
        st.subheader("🎯 Selecciona una carrera:")
        
        modalidades = df_careers['Modalidad'].unique()
        for modalidad in modalidades:
            st.markdown(f"### 📌 {modalidad.upper()}")
            carreras_modalidad = df_careers[df_careers['Modalidad'] == modalidad]
            
            cols = st.columns(2)
            for idx, (_, row) in enumerate(carreras_modalidad.iterrows()):
                col_idx = idx % 2
                with cols[col_idx]:
                    if st.button(f"{row['Carreras']}", key=f"career_{row.name}", use_container_width=True):
                        st.session_state.selected_career = row.name
                        add_message('user', f'Quiero información sobre: {row["Carreras"]}')
                        st.session_state.conversation_state = 'detalle_carrera'
                        st.rerun()
            st.markdown("---")
        
        if st.button("↩️ Volver al menú principal", use_container_width=True):
            st.session_state.conversation_state = 'inicio'
            st.rerun()

    elif state == 'detalle_carrera':
        if st.session_state.selected_career is not None:
            career_info = df_careers.iloc[st.session_state.selected_career]
            details = f"""
            **{career_info['Carreras']}**<br><br>
            📍 **Modalidad:** {career_info['Modalidad']}<br>
            ⏱️ **Duración:** {career_info['Duracion']} ({career_info['Año']})<br>
            🕐 **Jornada:** {career_info['Jornada']}<br>
            🎓 **Título:** {career_info['titulo_al_obtener']}<br><br>
            ¿Te interesa esta carrera? ¿Quieres proceder con la pre-inscripción?
            """
            add_message('bot', details)
            st.session_state.conversation_state = 'decision_carrera'
            st.rerun()

    elif state == 'decision_carrera':
        st.subheader("¿Qué te gustaría hacer ahora?")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("✅ Sí, Pre-inscripción", use_container_width=True):
                add_message('user', 'Sí, me interesa. Quiero hacer la pre-inscripción.')
                st.session_state.conversation_state = 'preinscripcion'
                st.rerun()
        
        with col_b:
            if st.button("🔍 Ver otra carrera", use_container_width=True):
                add_message('user', 'Quiero ver otra carrera.')
                st.session_state.conversation_state = 'carreras'
                st.rerun()
        
        with col_c:
            if st.button("↩️ Menú principal", use_container_width=True):
                add_message('user', 'Volver al menú principal.')
                st.session_state.conversation_state = 'inicio'
                st.rerun()

    elif state == 'preinscripcion':
        add_message('bot', '¡Perfecto! Para la pre-inscripción necesito algunos datos básicos:')
        st.subheader("📝 Formulario de Pre-inscripción")
        
        career_info = df_careers.iloc[st.session_state.selected_career]
        st.info(f"**Carrera seleccionada:** {career_info['Carreras']}")
        
        with st.form("preinscripcion_form"):
            nombre = st.text_input("Nombre completo *")
            cedula = st.text_input("Número de cédula *")
            email = st.text_input("Correo electrónico *")
            telefono = st.text_input("Teléfono *")
            
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                submit = st.form_submit_button("📤 Enviar Pre-inscripción", use_container_width=True)
            
            if submit:
                if all([nombre, cedula, email, telefono]):
                    st.session_state.user_data = {
                        'nombre': nombre, 
                        'email': email, 
                        'carrera': career_info['Carreras']
                    }
                    add_message('user', f'Datos enviados: {nombre}, {email}')
                    st.session_state.conversation_state = 'confirmacion'
                    st.rerun()
                else:
                    st.error("⚠️ Por favor completa todos los campos obligatorios (*)")
        
        if st.button("↩️ Volver", use_container_width=True):
            st.session_state.conversation_state = 'decision_carrera'
            st.rerun()

    elif state == 'confirmacion':
        user_data = st.session_state.user_data
        msg = f"""
        ✅ **¡Pre-inscripción Exitosa!**<br><br>
        Hola **{user_data['nombre']}**, hemos registrado tu pre-inscripción para:<br>
        📚 **{user_data['carrera']}**<br><br>
        Recibirás un correo de confirmación en **{user_data['email']}** con los próximos pasos.<br><br>
        ¡Gracias por elegir el ISTA! 🎓
        """
        add_message('bot', msg)
        st.session_state.conversation_state = 'final'
        st.rerun()
        
    elif state in ['matricula', 'horarios', 'contacto']:
        if state == 'matricula':
            add_message('bot', 'Aquí tienes información sobre nuestro proceso de matrícula:')
            show_enrollment_info()
        elif state == 'horarios':
            add_message('bot', 'Aquí tienes información sobre nuestros horarios y modalidades:')
            st.subheader("🕐 Horarios por Modalidad")
            for modalidad in df_careers['Modalidad'].unique():
                st.markdown(f"### {modalidad}")
                modalidad_data = df_careers[df_careers['Modalidad'] == modalidad]
                for _, row in modalidad_data.iterrows():
                    st.write(f"• **{row['Carreras']}** - Jornada: {row['Jornada']}")
        elif state == 'contacto':
            add_message('bot', 'Aquí tienes nuestra información de contacto:')
            st.markdown("""
            <div class="info-box">
                <h3>📞 Contacto ISTA</h3>
                <p><strong>📍 Ubicación:</strong> Parque Industrial, Cuenca, Ecuador</p>
                <p><strong>📞 Teléfono:</strong> +593 99 536 3076</p>
                <p><strong>✉️ Email:</strong> secretaria@tecazuay.edu.ec</p>
                <p><strong>🌐 Web:</strong> tecazuay.edu.ec</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.session_state.conversation_state = 'final'
        st.rerun()

    elif state == 'final':
        st.subheader("¿Necesitas algo más?")
        if st.button("🏠 Volver al menú principal", use_container_width=True):
            st.session_state.conversation_state = 'inicio'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # Cierre chat-controls-area
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre chat-main-container

# --- Sidebar ---
with col2:
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-yellow) 100%); border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3>🎓 ISTA</h3>
        <p style="margin: 0;">Instituto Tecnológico del Azuay</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.info("""
    🎯 **Instituto Superior Universitario**
    
    ✅ **Totalmente GRATUITO**
    
    📚 **16 carreras disponibles**
    - Técnicas y Tecnológicas
    
    🏛️ **Regidos por SENESCYT**
    
    🚀 **¡LA DECISIÓN QUE TRANSFORMARÁ TU FUTURO!**
    """)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(251, 191, 36, 0.1) 100%); padding: 15px; border-radius: 10px; border: 2px solid var(--accent-yellow);">
        <h4 style="color: var(--dark-blue); margin-top: 0;">📋 Modalidades de Formación</h4>
        <ul style="margin-bottom: 0;">
            <li><strong>Presencial:</strong> Clases en campus</li>
            <li><strong>Dual:</strong> Empresa + Instituto</li>
            <li><strong>Híbrida:</strong> Online + Presencial</li>
            <li><strong>En línea:</strong> 100% virtual</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("""
    <div style="background: var(--white); padding: 15px; border-radius: 10px; border: 2px solid var(--primary-blue); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.1);">
        <h4 style="color: var(--dark-blue); margin-top: 0;">📞 Contacto</h4>
        <p style="margin: 5px 0;"><strong>📍 Ubicación:</strong><br>Parque Industrial, Cuenca, Ecuador</p>
        <p style="margin: 5px 0;"><strong>📞 Teléfono:</strong><br>+593 99 536 3076</p>
        <p style="margin: 5px 0;"><strong>✉️ Email:</strong><br>secretaria@tecazuay.edu.ec</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, var(--accent-yellow) 0%, var(--bright-yellow) 100%); padding: 15px; border-radius: 10px; color: white;">
        <h4 style="margin-top: 0;">🌐 Redes Sociales</h4>
        <p style="margin: 5px 0;">🌐 <a href="http://tecazuay.edu.ec" style="color: white; text-decoration: none;"><strong>tecazuay.edu.ec</strong></a></p>
        <p style="margin: 5px 0;">📸 <a href="https://www.instagram.com/tecdelazuay" style="color: white; text-decoration: none;"><strong>@tecdelazuay</strong></a></p>
        <p style="margin: 5px 0;">❌ <a href="https://x.com/TecAzuay" style="color: white; text-decoration: none;"><strong>@TecAzuay</strong></a></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 Reiniciar Conversación", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Footer ---
st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <h3 style="margin-top: 0; color: white;">🎓 Instituto Tecnológico del Azuay</h3>
    <p style="font-size: 1.1rem; margin: 10px 0;"><strong>Chatbot de Admisiones - Tu futuro comienza aquí</strong></p>
    <p style="margin: 0; opacity: 0.9;">Desarrollado con 💛 para estudiantes del ISTA</p>
</div>
""", unsafe_allow_html=True)