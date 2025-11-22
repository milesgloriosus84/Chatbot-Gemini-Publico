import streamlit as st
import os
import google.generativeai as genai  # ← CORRECTO

# --- 1. CONFIGURACIÓN DE LA LLAVE API ---
API_KEY = os.environ.get("GEMINI_API_KEY")

# --- 2. CONFIGURACIÓN DE LA APLICACIÓN WEB ---
if not API_KEY:
    st.set_page_config(page_title="Error", layout="centered")
    st.title("🤖 Mi Asistente IA con Gemini")
    st.error("🚨 ERROR: La clave API (GEMINI_API_KEY) no está configurada.")
else:
    # Configura la API de Gemini
    genai.configure(api_key=API_KEY)

    # Carga el modelo correctamente
    model = genai.GenerativeModel("gemini-1.5-flash")  # ← MODELO REAL

    # Configuración de la página
    st.set_page_config(page_title="Mi Asistente IA", layout="centered")
    st.title("🤖 Mi Asistente IA con Gemini")
    st.markdown("---")

    # --- 3. SISTEMA DE CHAT ---
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

    # Capturar entrada
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("model"):
            with st.spinner("Pensando..."):
                try:
                    # Llamada correcta al modelo
                    response = model.generate_content(
                        st.session_state.messages
                    )
                    ai_response = response.text

                except Exception as e:
                    ai_response = f"⚠️ Hubo un error al contactar con la IA:\n\n**{e}**"

            st.markdown(ai_response)

        # Guardar respuesta en historial
        st.session_state.messages.append({"role": "model", "content": ai_response})
