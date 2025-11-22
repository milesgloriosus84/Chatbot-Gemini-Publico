import streamlit as st
import os 
from google import generativeai

# --- 1. CONFIGURACIÓN DE LA LLAVE API ---
# ¡AQUÍ DEBES PEGAR TU CLAVE API REAL ENTRE LAS COMILLAS!
API_KEY = os.environ.get("GEMINI_API_KEY")

# --- 2. CONFIGURACIÓN DE LA APLICACIÓN WEB (STREAMLIT) ---
# Verifica si la clave fue cargada
if not API_KEY or API_KEY == "TU_CLAVE_API_DE_GOOGLE":
    st.set_page_config(page_title="Error", layout="centered")
    st.title("🤖 Mi Asistente IA con Gemini")
    st.error("🚨 ERROR: Por favor, reemplaza 'TU_CLAVE_API_DE_GOOGLE' por tu clave API real en el código de main.py.")
else:
    # Inicializa el cliente de Google Gemini
    generativeai.configure(api_key=API_KEY)

    # El resto del código Streamlit
    st.set_page_config(page_title="Mi Asistente IA Personalizado", layout="centered")
    st.title("🤖 Mi Asistente IA con Gemini")
    st.markdown("---")
    
    # --- 3. CREACIÓN DEL CHAT ---
    
    # Inicializa el historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "model", "content": "¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?"})

    # Muestra los mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Captura la entrada del usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("model"):
            with st.spinner("Pensando..."):
                try:
                    # Llama al modelo de Google Gemini, usando el historial para memoria
                    response = generativeai.generate_content(
                        model='gemini-2.5-flash',
                        contents=st.session_state.messages 
                    )
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"⚠️ Hubo un error al contactar con la IA. Error: {e}"

            st.markdown(ai_response)
        
        st.session_state.messages.append({"role": "model", "content": ai_response})