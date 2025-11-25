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
# SIDEBAR: Configuración del modelo
# ----------------------------
st.sidebar.title("⚙️ Configuración")

# Selector de modelo
modelo_seleccionado = st.sidebar.selectbox(
    "Modelo:",
    ["gemini-2.5-flash", "gemini-2.0-pro", "gemini-1.5-flash"]
)

# Slider de temperatura
temperatura = st.sidebar.slider(
    "Temperatura:", 0.0, 1.0, 0.7, 0.1
)

# Botón para limpiar conversación
if st.sidebar.button("🗑️ Limpiar conversación"):
    st.session_state.mensajes = []
    st.rerun()  # Recargar la app


# ----------------------------
# Inicializar historial
# ----------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Crear modelo dinámicamente con los parámetros del sidebar
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura
)

# ----------------------------
# Mostrar mensajes previos
# ----------------------------
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# ----------------------------
# Input del usuario
# ----------------------------
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Guardarlo en memoria
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    # Obtener respuesta del modelo
    respuesta = chat_model.invoke(st.session_state.mensajes)

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    # Guardar respuesta en el historial
    st.session_state.mensajes.append(respuesta)
