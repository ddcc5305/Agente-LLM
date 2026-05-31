# Benchmark — Comparativa de 4 modelos

Set fijo de **15 preguntas** para evaluar el agente sobre el corpus DNI Valencia.
Cubre cuatro categorías:

| Categoría | Cuántas | Para qué |
|---|---|---|
| Factual directa | 5 | Pregunta directa sobre proyectos, filosofía o datos de DNI. |
| Logística práctica | 4 | Horarios, ubicaciones, cómo participar. |
| Síntesis multi-doc | 3 | Requiere combinar información de varios archivos del corpus. |
| Fuera de ámbito | 3 | Deben rechazarse con la frase literal `No tengo esa información en mis fuentes`. |

## Modelos evaluados

| Modelo | Servidor | Tipo |
|---|---|---|
| `gemma3:4b` | Ollama Local | Modelo local ligero |
| `qwen2.5:3b` | Ollama Local | Modelo local rápido |
| `gemma3:27b` | PoliGPT (UPV) | Modelo grande en servidor |
| `gpt-oss-120b` | PoliGPT (UPV) | Modelo gigante en servidor |

## Archivos

- `preguntas.json` — Las 15 preguntas del set de evaluación.
- `benchmark.py` — Script que ejecuta las preguntas contra los 4 modelos y genera los resultados.
- `benchmark.json` — Resultados crudos estructurados (respuestas, tokens, latencia).
- `benchmark.md` — Tabla legible con resultados y análisis interpretativo.
- `runs/` — Ejecuciones históricas individuales.

## Ejecutar

```bash
python benchmark/benchmark.py
```

Los resultados se guardan automáticamente en `benchmark/benchmark.json` y se genera `benchmark/benchmark.md` con la tabla comparativa.

## Resultados resumidos

| Modelo | Latencia Media | Tok/s | Aciertos (de 12) | Rechazos (de 3) |
|---|---|---|---|---|
| qwen2.5:3b | 5.38 s | 72.9 | 11/12 | 3/3 |
| gemma3:4b | 10.95 s | 25.6 | 11/12 | 3/3 |
| gemma3:27b | **2.63 s** | 25.3 | 11/12 | 3/3 |
| gpt-oss-120b | 40.00 s | 11.1 | 11/12 | 3/3 |

Ver `benchmark.md` para el detalle completo por pregunta y la interpretación de los resultados.
