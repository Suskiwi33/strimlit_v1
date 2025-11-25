import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")

st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")


# ----------------------------
# SIDEBAR CONFIGURACIÓN
# ----------------------------
st.sidebar.title("⚙️ Configuración")

# Selección de modelo
modelo_seleccionado = st.sidebar.selectbox(
    "Modelo:",
    ["gemini-2.5-flash", "gemini-2.0-pro", "gemini-1.5-flash"]
)

# 1.2 – Modo creativo / preciso
modo = st.sidebar.radio("Modo:", ["Preciso", "Creativo"])
temperatura = 0.2 if modo == "Preciso" else 0.9

# Slider de temperatura
temperatura = st.sidebar.slider(
    "Temperatura:", 0.0, 1.0, 0.7, 0.1
)

# 1.1 – Max tokens
max_tokens = st.sidebar.number_input(
    "Tokens máximos:",
    min_value=50, max_value=4000, value=512
)

# 1.4 – Activar memoria
usar_memoria = st.sidebar.checkbox("Activar memoria", value=True)

# 2.2 – Mostrar historial
mostrar_historial = st.sidebar.checkbox("Mostrar historial", value=True)

# 2.3 – Tamaño de letra
font_size = st.sidebar.slider("Tamaño de letra:", 12, 24, 16)

# Botón para limpiar conversación
if st.sidebar.button("🗑️ Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()


# ----------------------------
# Inicializar historial
# ----------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Crear modelo con configuración dinámica
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura,
    max_output_tokens=max_tokens
)


# ----------------------------
# CSS dinámico del tamaño de texto
# ----------------------------
st.markdown(
    f"""
    <style>
    .stChatMessage p {{
        font-size: {font_size}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ----------------------------
# Mostrar historial (si está activado)
# ----------------------------
if mostrar_historial:
    for msg in st.session_state.mensajes:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(msg.content)


# ----------------------------
# Input del Chat
# ----------------------------
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Guardar si hay memoria activada
    if usar_memoria:
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        mensajes_para_enviar = st.session_state.mensajes
    else:
        mensajes_para_enviar = [HumanMessage(content=pregunta)]

    # Obtener respuesta del modelo
    respuesta = chat_model.invoke(mensajes_para_enviar)

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    # Guardar respuesta solo si hay memoria
    if usar_memoria:
        st.session_state.mensajes.append(respuesta)
