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

## ¿En qué partes os ha ayudado?

Sed específicos. Ejemplos de declaración honesta:

- **Depuración de SSL/TLS**: Gemini en Antigravity nos guio para modificar el cliente `httpx` en `poligpt_llm.py` y saltar el error de certificado autofirmado de la UPV.
- **Estructura del Benchmark**: Usamos Claude Opus y Gemini para adaptar el paso del `backend_override` a lo largo de `pipeline.py` y `config.py`, logrando que el script lance los modelos locales y de PoliGPT de forma orquestada.
- **Arquitectura Hexagonal**: Le dimos a Claude Opus el esquema del enunciado y él redactó gran parte de la estructura base, refactorizando el `consultar.py` monolítico a la separación de dominio, puertos y adaptadores.
- **Análisis de Resultados**: Gemini en Antigravity analizó nuestro `benchmark.json` y nos redactó el borrador comparativo destacando por qué `gemma3:27b` es el mejor.
- **NO usado para**: la grabación del vídeo final ni la redacción completa del informe final, que escribimos y revisamos nosotros.

## Compromiso

Hemos leído y entendido todo el código que hemos entregado. En la presentación
oral en directo seremos capaces de defender cualquier línea que el profesor
nos señale. Si no podemos defender una decisión, asumimos que la nota baja.

Firma (digital, escribiendo el nombre): Álvaro Marrès, David Bayona, Manuel Pérez.
