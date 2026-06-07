import sys
from pathlib import Path

# Añadimos las rutas al sys.path para poder importar correctamente
_file_path = Path(__file__).resolve()
sys.path.insert(0, str(_file_path.parents[3]))  # añade 'src'
sys.path.insert(0, str(_file_path.parents[4]))  # añade la raíz del proyecto

import streamlit as st
import torch
from transformers import pipeline
from agente_rag.pipeline import answer as consultar

st.set_page_config(page_title="DNI Valencia - Asistente", page_icon="🤖")
st.title("🤖 Asistente DNI Valencia")

# --- Extra: Hugging Face TTS (Voz) ---
@st.cache_resource
def load_tts():
    # Este modelo es el que menos RAM consume (aprox 150MB)
    model_id = "facebook/mms-tts-spa"
    
    # Forzamos el uso de CPU si tu gráfica (GPU) está llena con Ollama
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    pipe = pipeline("text-to-speech", model=model_id, device=device)
    return pipe

tts_pipe = load_tts()

def speak(text):
    # Genera el audio a partir del texto de la respuesta
    output = tts_pipe(text)
    st.audio(output["audio"], sample_rate=output["sampling_rate"])

# --- Interfaz de Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿A qué hora son los desayunos?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Llamada a la lógica hexagonal
        with st.spinner("Consultando fuentes oficiales..."):
            res = consultar(prompt)
            
        st.markdown(res["respuesta"])
        
        # Mostrar fuentes (Banda 6)
        if res.get("fuentes"):
            st.caption(f"Fuentes: {', '.join(res['fuentes'])}")
        
        # Generar voz (Extra Hugging Face)
        speak(res["respuesta"])

    st.session_state.messages.append({"role": "assistant", "content": res["respuesta"]})