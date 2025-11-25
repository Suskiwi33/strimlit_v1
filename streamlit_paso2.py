import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖", layout="wide")

st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# ----------------------------
# Crear columnas: chat (80%) + menú derecha (20%)
# ----------------------------
col_chat, col_menu = st.columns([4, 1])


# ----------------------------
# MENÚ DE CONFIGURACIÓN (DERECHA)
# ----------------------------
with col_menu:
    st.markdown("### ⚙️ Configuración")

    # Selección de modelo
    modelo_seleccionado = st.selectbox(
        "Modelo:",
        ["gemini-2.5-flash", "gemini-2.0-pro", "gemini-1.5-flash"]
    )

    # ============================
    # 1.2 – Modo creativo / preciso
    # ============================
    modo = st.radio("Modo:", ["Preciso", "Creativo"])

    if modo == "Preciso":
        temperatura = 0.2
    else:
        temperatura = 0.9

    # ============================
    # 1.1 – Max tokens
    # ============================
    max_tokens = st.number_input(
        "Tokens máximos:",
        min_value=50, max_value=4000, value=512
    )

    # ============================
    # 1.4 – Usar memoria (todo historial)
    # ============================
    usar_memoria = st.checkbox("Activar memoria", value=True)

    # ============================
    # 2.2 – Mostrar / ocultar historial
    # ============================
    mostrar_historial = st.checkbox("Mostrar historial", value=True)

    # ============================
    # 2.3 – Tamaño de letra del chat
    # ============================
    font_size = st.slider("Tamaño de letra:", 12, 24, 16)

    # Botón limpiar conversación
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()


# ----------------------------
# Inicializar historial
# ----------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Crear modelo dinámicamente
chat_model = ChatGoogleGenerativeAI(
    model=modelo_seleccionado,
    temperature=temperatura,
    max_output_tokens=max_tokens
)


# ----------------------------
# CHAT (IZQUIERDA)
# ----------------------------
with col_chat:

    # CSS dinámico: tamaño de letra
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

    # Mostrar historial (si activado)
    if mostrar_historial:
        for msg in st.session_state.mensajes:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            with st.chat_message(role):
                st.markdown(msg.content)

    # Input del usuario
    pregunta = st.chat_input("Escribe tu mensaje:")

    if pregunta:
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(pregunta)

        # Guardar o no según memoria activada
        if usar_memoria:
            st.session_state.mensajes.append(HumanMessage(content=pregunta))
        else:
            # Solo se envía el último mensaje sin historial
            temp_historial = [HumanMessage(content=pregunta)]

        # Obtener respuesta
        respuesta = chat_model.invoke(
            st.session_state.mensajes if usar_memoria else temp_historial
        )

        # Mostrar respuesta
        with st.chat_message("assistant"):
            st.markdown(respuesta.content)

        # Guardar respuesta solo si memoria activada
        if usar_memoria:
            st.session_state.mensajes.append(respuesta)
