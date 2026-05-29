# Decisiones de arquitectura

> Por qué hemos tomado cada decisión técnica. No describe *qué* hace cada
> fichero (eso está en el README), sino el *por qué* detrás.

## 1. Por qué arquitectura hexagonal

Desde el inicio optamos por la arquitectura hexagonal (ports & adapters) para
aspirar al 10. La ventaja principal: el dominio (`domain/`) no sabe si detrás
hay Ollama, PoliGPT o un fake. Esto nos permite:

- **Cambiar de LLM** con una línea en `.env` (y lo demostramos en el benchmark
  con 4 modelos distintos).
- **Testear el dominio sin red**: `test_chatbot_service.py` usa `FakeLLM` +
  `FakeRetriever` y corre en milisegundos.
- **Añadir backends** sin tocar la lógica: FAISS, sentence-transformers o
  PoliGPT son adapters independientes.

La estructura sigue el modelo propuesto en el manual técnico §8:

- `domain/ports.py` — interfaces (`LLMPort`, `EmbedderPort`, `RetrieverPort`, `VectorStorePort`).
- `domain/entities.py` — dataclasses puras (`Question`, `Answer`, `Chunk`, `GenerationResult`).
- `domain/chatbot_service.py` — lógica RAG que solo depende de ports y entities.
- `adapters/` — implementaciones concretas intercambiables.
- `config.py` — composition root, único módulo que importa adapters concretos.

## 2. Por qué ChromaDB persistente

El examinador clona, indexa una vez y luego hace múltiples preguntas. Con
`PersistentClient(path=...)` el segundo arranque tarda < 2s en lugar de
re-embedar todo el base_conocimiento (~30-60s). El directorio `data/chroma/` está en
`.gitignore` y se regenera con `python scripts/build_index.py`.

## 3. Por qué `nomic-embed-text`

Un único endpoint Ollama para LLM y embeddings. Una sola dependencia
(`requests`), un solo timeout. Como alternativa implementamos un adapter de
`sentence-transformers` (`st_embedder.py`) que funciona sin Ollama.

## 4. Por qué chunk_size=500 / overlap=100

El sweet spot para texto en español según el Colab de la asignatura: un chunk
típico es un párrafo o medio, suficiente para distinguir temas por contexto.
Documentos con formato Q:/A: (como `15_desayunos_100_preguntas.txt`) se
benefician de no cortar entre pregunta y respuesta.

## 5. Por qué `score = 1 - distance`

ChromaDB devuelve distancias (más bajo = más cercano), pero el contrato y el
lenguaje natural esperan scores (más alto = mejor). Hacemos la conversión una
sola vez en el adapter (`chroma_adapter.py`) para que el dominio razone
siempre en "score".

## 6. Por qué `verify_ssl=False` contra UPV

El endpoint PoliGPT de la UPV usa certificado autofirmado. Con `verify=True`
falla el handshake. El default en `.env.example` es `VERIFY_SSL=true` y solo
se desactiva para PoliGPT dentro de la red UPV.

## 7. Por qué los tests no llaman a Ollama

1. **Reproducibilidad**: no depender de la red.
2. **Velocidad**: milisegundos vs. segundos por llamada al LLM.
3. **Cobertura del contrato**: verificar la forma del JSON, no el contenido.

La validación E2E con Ollama real se hace con `scripts/run_eval.py` y el
benchmark (`benchmark/benchmark.py`).

## 8. Dificultades encontradas

- **SSL con PoliGPT**: el certificado autofirmado nos dio problemas con
  `httpx` (que usa la librería de OpenAI por debajo). Tuvimos que pasar
  `verify=False` al cliente.
- **Benchmark con PoliGPT**: las latencias son mucho más variables que con
  Ollama local. `gpt-oss-120b` en particular oscilaba entre 16s y 70s por
  pregunta.
- **Coherencia del chunking**: documentos con formato Q:/A: perdían contexto
  si el splitter cortaba entre pregunta y respuesta.
