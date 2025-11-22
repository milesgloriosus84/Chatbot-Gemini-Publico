import streamlit as st
import os
import google.generativeai as genai

# ---------------------------------------------------------
# FUNCIÓN PARA CONVERTIR MENSAJES AL FORMATO QUE GEMINI USA
# ---------------------------------------------------------
def convert_messages(messages):
    converted = []
    for msg in messages:
        converted.append({
            "role": msg["role"],
            "parts": [
                {"text": msg["content"]}
            ]
        })
    return converted


# ---------------------------
# 1. CONFIGURACIÓN DE LA API
# ---------------------------
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.set_page_config(page_title="Error", layout="centered")
    st.title("🤖 Mi Asistente IA con Gemini")
    st.error("🚨 ERROR: La clave API (GEMINI_API_KEY) no está configurada o es inválida.")
else:
    genai.configure(api_key=API_KEY)

    # Cargar modelo correcto
    model = genai.GenerativeModel("gemini-1.5-flash")

    # ---------------------------
    # 2. INTERFAZ DE LA WEB
    # ---------------------------
    st.set_page_config(page_title="Mi Asistente IA", layout="centered")
    st.title("🤖 Mi Asistente IA con Gemini")
    st.markdown("---")

    # ---------------------------
    # 3. SISTEMA DE MENSAJES
    # ---------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "model",
            "content": "¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?"
        })

    # Mostrar historial
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------------------
    # 4. CAPTURAR PREGUNTA DEL USUARIO
    # ---------------------------
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):

        # Añadir a historial
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("model"):
            with st.spinner("Pensando..."):

                try:
                    # Llamada CORRECTA a Gemini usando formato válido
                    formatted_history = convert_messages(st.session_state.messages)

                    response = model.generate_content(formatted_history)
                    ai_response = response.text

                except Exception as e:
                    ai_response = f"⚠️ Error al contactar con la IA:\n\n{e}"

            st.markdown(ai_response)

        # Guardar respuesta
        st.session_state.messages.append({"role": "model", "content": ai_response})
