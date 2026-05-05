import streamlit as st
import torch
from transformers import pipeline
from consultar import consultar

st.set_page_config(page_title="DNI Valencia - Asistente", page_icon="🤖")
st.title("🤖 Asistente DNI Valencia")

# --- Extra: Hugging Face TTS (Voz) ---
@st.cache_resource
def load_tts():
    # Modelo ligero de Facebook para español
    return pipeline("text-to-speech", model="facebook/mms-tts-spa")

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
        # Llamada a la lógica hexagonal[cite: 3, 5]
        with st.spinner("Consultando fuentes oficiales..."):
            res = consultar(prompt)
            
        st.markdown(res["respuesta"])
        
        # Mostrar fuentes (Banda 6)[cite: 2]
        if res.get("fuentes"):
            st.caption(f"Fuentes: {', '.join(res['fuentes'])}")
        
        # Generar voz (Extra Hugging Face)[cite: 2]
        speak(res["respuesta"])

    st.session_state.messages.append({"role": "assistant", "content": res["respuesta"]})