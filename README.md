# Agente RAG — Asistente Inteligente DNI Valencia

> Práctica de **Inteligencia Artificial** (3º GTI, UPV).
> Agente RAG con arquitectura hexagonal que responde preguntas sobre la
> asociación de voluntariado **Damos Nuestra Ilusión (DNI)** Valencia.

## Descripción

Sistema RAG (Retrieval-Augmented Generation) que:

1. **Indexa** 16 documentos `.txt` sobre la asociación DNI (FAQ, proyectos, logística, etc.).
2. **Recupera** los fragmentos más relevantes ante cada pregunta (retrieval semántico con ChromaDB).
3. **Genera** respuestas fundamentadas citando las fuentes, sin inventar información.
4. **Rechaza** preguntas fuera de ámbito con la frase literal: *"No tengo esa información en mis fuentes"*.

## Arranque rápido

```bash
# 1. Clonar y crear entorno virtual
git clone <este-repo>
cd Agente-LLM
python -m venv .venv
.venv\Scripts\activate     
pip install -r requirements.txt

# 2. Tener Ollama corriendo con los modelos necesarios
ollama pull gemma3:4b
ollama pull nomic-embed-text

# 3. Copiar y configurar variables de entorno
copy .env.example .env     

# 4. Construir el índice
python scripts/build_index.py

# 5. Lanzar una consulta
python consultar.py "¿Qué es DNI Valencia?"
```

Salida esperada:

```json
{
  "respuesta": "DNI (Damos Nuestra Ilusión) es una asociación juvenil de voluntariado...",
  "fuentes": ["01_faq_dni.txt", "04_filosofia_dni.txt"],
  "chunks": [{"source": "01_faq_dni.txt", "text": "...", "score": 0.89}],
  "metricas": {"prompt_tokens": 1556, "output_tokens": 58, "tokens_per_sec": 30.3, "latencia_s": 11.1, "modelo": "gemma3:4b"}
}
```

## Arquitectura

El proyecto sigue una **arquitectura hexagonal** (ports & adapters):

```
Agente-LLM/
├── consultar.py              # Contrato §9 opción A (punto de entrada)
├── api.py                    # Contrato §9 opción B (POST /query, FastAPI)
├── features.json             # Declaración de bandas y extras
├── GRUPO.md / AI_USAGE.md    # Documentación obligatoria
├── base_conocimiento/        # 16 .txt del corpus DNI (no modificar)
├── src/agente_rag/
│   ├── domain/
│   │   ├── entities.py       # Question, Answer, Chunk, GenerationResult
│   │   ├── ports.py          # LLMPort, EmbedderPort, RetrieverPort, VectorStorePort
│   │   └── chatbot_service.py # Lógica RAG pura (sin imports externos)
│   ├── adapters/
│   │   ├── llm/              # OllamaLLM, PoliGPTLLM, FakeLLM
│   │   ├── embedder/         # OllamaEmbedder, STEmbedder, FakeEmbedder
│   │   ├── retriever/        # ChromaRetriever, FAISSRetriever, FakeRetriever
│   │   └── web/              # Streamlit UI (frontend)
│   ├── config.py             # Composition root (ensambla adapters)
│   ├── pipeline.py           # Traduce dominio → contrato del corrector
│   └── chunker.py            # Carga y trocea el corpus
├── scripts/
│   ├── build_index.py        # Construye índice ChromaDB persistente
│   └── run_eval.py           # Evaluación rápida
├── benchmark/                # Comparativa de 4 modelos (banda 7)
├── evaluacion/               # RAGAs + métricas propias (banda 8)
├── tests/                    # pytest sin dependencia de red
└── docs/                     # Documentación técnica
```

## Bandas implementadas

- **Banda 5** ✓ — Pipeline RAG completo con prompt anti-alucinación.
- **Banda 6** ✓ — Cada respuesta cita el archivo fuente del corpus.
- **Banda 7** ✓ — Benchmark con 4 modelos (gemma3:4b, qwen2.5:3b, gpt-oss-120b, gemma3:27b). Métricas de tokens y latencia.
- **Banda 8** ✓ — Evaluación RAGAs (faithfulness, answer_relevancy, context_precision, context_recall) + 2 métricas propias (Source Coverage, Rejection Accuracy).
- **Banda 10** ✓ — Arquitectura hexagonal con ports & adapters. Tests del dominio sin red.

## Extras

- **Frontend** (+1.5) — Interfaz Streamlit con chat interactivo.
- **Hugging Face** (+1.5) — TTS integrado con `facebook/mms-tts-spa` para leer las respuestas en voz.

## Tests

```bash
pytest -q
```

Los tests **no llaman a Ollama**: usan `FakeLLM` y `FakeRetriever` para verificar
que el contrato de salida se respeta y que el dominio funciona correctamente sin red.

## Intercambiabilidad de adapters

Cambiar de adapter = cambiar 1 línea en `.env`:

```bash
LLM_BACKEND=poligpt       # cambia Ollama → PoliGPT
RETRIEVER_BACKEND=faiss   # cambia ChromaDB → FAISS
EMBEDDER_BACKEND=st       # cambia Ollama embeddings → sentence-transformers
```

El dominio no se entera del cambio.

## Diagrama de capas

```
┌──────────────────────────────────────────────────────────┐
│                     ADAPTERS (entrada)                   │
│   consultar.py │ api.py (FastAPI) │ streamlit_ui.py      │
├──────────────────────────────────────────────────────────┤
│                    DOMINIO PURO                          │
│   ChatbotService  │  Question, Answer, Chunk             │
│   (chatbot_service.py, entities.py)                      │
│   Solo importa ports.py — sin dependencias externas      │
├──────────────────────────────────────────────────────────┤
│                 PORTS (interfaces)                        │
│   LLMPort │ EmbedderPort │ RetrieverPort │ VectorStorePort│
├──────────────────────────────────────────────────────────┤
│                   ADAPTERS (salida)                       │
│   OllamaLLM    │ PoliGPTLLM   │ FakeLLM                 │
│   OllamaEmbed  │ STEmbedder   │ FakeEmbedder             │
│   ChromaRetr   │ FAISSRetr    │ FakeRetriever            │
└──────────────────────────────────────────────────────────┘
```

## Créditos

Práctica de Inteligencia Artificial — Universitat Politècnica de València, 2026.
Profesores: Vicente Rivas Monferrer & Juan M. Alberola.
