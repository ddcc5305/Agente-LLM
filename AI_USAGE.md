# AI_USAGE.md — uso honesto de asistentes de IA

> Plantilla obligatoria. Rellenadla con la verdad. **No penaliza usar IA**;
> penaliza mentir sobre el uso (ver enunciado §6 y rúbrica).

## ¿Qué herramientas habéis usado?

- [ ] ChatGPT (GPT-4 / GPT-5 / o3 / ...)
- [X] Claude (Opus)
- [ ] GitHub Copilot
- [ ] Cursor / Windsurf / IDE con asistente integrado
- [X] Gemini (Antigravity)
- [ ] Ollama local con modelos abiertos
- [ ] Otras: ...

## Detalle por herramienta y fichero

### Claude (Opus)

| Tarea | Ficheros modificados | Revisado y Validado por nosotros |
|---|---|---|
| Diseño y estructura de la arquitectura hexagonal | `src/agente_rag/domain/entities.py`, `ports.py`, `chatbot_service.py` | **Sí (Funcional).** Planteamos el diseño de puertos y adaptadores. Claude generó el esqueleto y la lógica del servicio. Validamos que el pipeline funcionara correctamente conectando el flujo de datos. |
| Implementación de los adaptadores de infraestructura | `adapters/llm/`, `adapters/embedder/`, `adapters/retriever/` | **Sí (Funcional).** Delegamos en Claude la escritura de la lógica de conexión con las APIs de ChromaDB, FAISS y los clientes de Ollama. Nosotros nos encargamos de verificar mediante pruebas de consulta que la base de conocimientos se cargaba y respondía. |
| Creación de tests unitarios | `tests/test_chatbot_service.py`, `test_contract.py` | **Sí (Funcional).** Claude generó los mocks y fakes de los puertos. Nosotros ejecutamos la suite de tests para asegurar que el contrato y los servicios no rompían el flujo básico. |

### Gemini (Antigravity)

| Tarea | Ficheros modificados | Revisado y Validado por nosotros |
|---|---|---|
| Resolución de errores de SSL y conectividad con PoliGPT | `adapters/llm/poligpt_llm.py` | **Sí (Funcional).** Delegamos en Gemini la solución técnica del error de SSL con PoliGPT (inyección del cliente httpx sin verificación). Comprobamos que el modelo respondía a las preguntas tras aplicar la solución. |
| Automatización del script de benchmark y formato | `pipeline.py`, `config.py`, `benchmark/` | **Sí (Funcional).** Gemini estructuró el script para automatizar la ejecución sobre los 4 modelos de forma consecutiva. Nosotros nos encargamos de ejecutar el benchmark, medir los tiempos de respuesta y analizar visualmente las respuestas en el markdown generado. |
| Detección de fallos y corrección de la documentación | `INFORME.md`, `README.md`, `GRUPO.md` | **Sí (Funcional).** Utilizamos Gemini para auditar que cumplíamos con la rúbrica (como añadir el diagrama Mermaid de la arquitectura, el renombrado de directorios a `base_conocimiento` y estructurar la sección de limitaciones). |

### Algunos scripts han sido revisados a nivel de línea de código (podriamos habernos dejado algo por revisar, pero hemos revisado todo lo que pudimos)

- **Lógica de inicialización de FAISS y ChromaDB:** Las llamadas a las clases internas de vectorización y persistencia en disco de `chromadb` y `faiss` fueron implementadas directamente por las IAs según los parámetros de configuración y no las hemos modificado línea a línea, limitándonos a comprobar que creaban las carpetas de base de datos correctamente.
- **Implementación interna de los fakes de test:** Toda la simulación del comportamiento de los modelos y recuperadores fakes (`FakeLLM`, `FakeRetriever`) en los tests unitarios fue generada de manera automática por Claude para acelerar las validaciones.
- **Detalle de bajo nivel del Text-to-Speech (Hugging Face):** La lógica de generación y procesado de arrays de audio en la UI con `facebook/mms-tts-spa` fue escrita por la IA; nosotros validamos su correcto funcionamiento interactuando con el reproductor de audio del frontend.

## Compromiso

Hemos leído y entendido el flujo lógico y la arquitectura del código que hemos entregado. Aunque nos hemos apoyado fuertemente en asistentes de IA para la codificación y depuración, conocemos la función de cada capa (Dominio, Puertos, Adaptadores) y seremos capaces de defender el funcionamiento del sistema en la presentación oral.

Firma (digital, escribiendo el nombre): Álvaro Marrès, David Bayona, Manuel Pérez.
