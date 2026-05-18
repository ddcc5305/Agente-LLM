# Benchmark — Comparativa de 4 modelos

Fecha: 2026-05-18 12:48
Preguntas: 15

## Tabla de resultados

| Modelo | Pregunta | Tokens IN | Tokens OUT | Tok/s | Latencia (s) | Acierto |
|--------|----------|-----------|------------|-------|-------------|---------|
| gemma3:4b | q1 | 1556 | 58 | 30.32 | 11.08 | ✓ |
| gemma3:4b | q2 | 1640 | 133 | 30.08 | 8.19 | ✓ |
| gemma3:4b | q3 | 1621 | 176 | 30.08 | 9.88 | ✗ |
| gemma3:4b | q4 | 1855 | 171 | 6.75 | 32.37 | ✓ |
| gemma3:4b | q5 | 1828 | 47 | 6.63 | 14.01 | ✓ |
| gemma3:4b | q6 | 1653 | 103 | 6.94 | 21.3 | ✓ |
| gemma3:4b | q7 | 1614 | 29 | 6.42 | 10.89 | ✓ |
| gemma3:4b | q8 | 2009 | 61 | 32.34 | 6.59 | ✓ |
| gemma3:4b | q9 | 1905 | 80 | 30.54 | 6.37 | ✓ |
| gemma3:4b | q10 | 1893 | 341 | 32.37 | 14.42 | ✓ |
| gemma3:4b | q11 | 1231 | 46 | 35.31 | 4.61 | ✓ |
| gemma3:4b | q12 | 1768 | 314 | 32.91 | 13.36 | ✓ |
| gemma3:4b | q13 | 1639 | 9 | 37.67 | 3.76 | N/A (fuera ámbito) |
| gemma3:4b | q14 | 1729 | 9 | 37.4 | 3.72 | N/A (fuera ámbito) |
| gemma3:4b | q15 | 1618 | 9 | 27.74 | 3.69 | N/A (fuera ámbito) |
| qwen2.5:3b | q1 | 1707 | 91 | 71.23 | 7.82 | ✓ |
| qwen2.5:3b | q2 | 1797 | 138 | 72.0 | 4.94 | ✓ |
| qwen2.5:3b | q3 | 1778 | 334 | 71.46 | 8.11 | ✗ |
| qwen2.5:3b | q4 | 2040 | 133 | 71.11 | 5.14 | ✓ |
| qwen2.5:3b | q5 | 2008 | 169 | 71.27 | 5.73 | ✓ |
| qwen2.5:3b | q6 | 1822 | 76 | 72.54 | 4.25 | ✓ |
| qwen2.5:3b | q7 | 1757 | 24 | 74.5 | 3.4 | ✓ |
| qwen2.5:3b | q8 | 2194 | 208 | 70.74 | 6.47 | ✓ |
| qwen2.5:3b | q9 | 2058 | 231 | 71.06 | 6.7 | ✓ |
| qwen2.5:3b | q10 | 2110 | 190 | 70.88 | 6.25 | ✓ |
| qwen2.5:3b | q11 | 1361 | 198 | 71.4 | 5.84 | ✓ |
| qwen2.5:3b | q12 | 1923 | 206 | 71.15 | 6.23 | ✓ |
| qwen2.5:3b | q13 | 1821 | 10 | 79.24 | 3.21 | N/A (fuera ámbito) |
| qwen2.5:3b | q14 | 1894 | 20 | 75.16 | 3.44 | N/A (fuera ámbito) |
| qwen2.5:3b | q15 | 1809 | 10 | 79.95 | 3.2 | N/A (fuera ámbito) |
| gpt-oss-120b | q1 | 1491 | 257 | 9.52 | 26.98 | ✓ |
| gpt-oss-120b | q2 | 1618 | 536 | 15.36 | 34.89 | ✓ |
| gpt-oss-120b | q3 | 1565 | 552 | 7.83 | 70.49 | ✗ |
| gpt-oss-120b | q4 | 1808 | 294 | 10.15 | 28.95 | ✓ |
| gpt-oss-120b | q5 | 1800 | 890 | 15.81 | 56.31 | ✓ |
| gpt-oss-120b | q6 | 1631 | 646 | 40.02 | 16.14 | ✓ |
| gpt-oss-120b | q7 | 1556 | 151 | 2.43 | 62.13 | ✓ |
| gpt-oss-120b | q8 | 1932 | 192 | 11.48 | 16.73 | ✓ |
| gpt-oss-120b | q9 | 1832 | 394 | 8.57 | 45.97 | ✓ |
| gpt-oss-120b | q10 | 1836 | 486 | 11.7 | 41.55 | ✓ |
| gpt-oss-120b | q11 | 1192 | 469 | 13.24 | 35.42 | ✓ |
| gpt-oss-120b | q12 | 1721 | 745 | 10.97 | 67.94 | ✓ |
| gpt-oss-120b | q13 | 1581 | 101 | 2.26 | 44.79 | N/A (fuera ámbito) |
| gpt-oss-120b | q14 | 1670 | 84 | 3.31 | 25.39 | N/A (fuera ámbito) |
| gpt-oss-120b | q15 | 1557 | 83 | 3.16 | 26.26 | N/A (fuera ámbito) |
| gemma3:27b | q1 | 1556 | 77 | 24.71 | 3.12 | ✓ |
| gemma3:27b | q2 | 1640 | 141 | 39.16 | 3.6 | ✓ |
| gemma3:27b | q3 | 1621 | 9 | 6.32 | 1.42 | ✗ |
| gemma3:27b | q4 | 1855 | 41 | 20.1 | 2.04 | ✓ |
| gemma3:27b | q5 | 1828 | 133 | 38.23 | 3.48 | ✓ |
| gemma3:27b | q6 | 1653 | 68 | 28.95 | 2.35 | ✓ |
| gemma3:27b | q7 | 1614 | 38 | 20.49 | 1.85 | ✓ |
| gemma3:27b | q8 | 2009 | 84 | 30.27 | 2.77 | ✓ |
| gemma3:27b | q9 | 1905 | 80 | 30.49 | 2.62 | ✓ |
| gemma3:27b | q10 | 1893 | 153 | 39.59 | 3.86 | ✓ |
| gemma3:27b | q11 | 1231 | 106 | 37.46 | 2.83 | ✓ |
| gemma3:27b | q12 | 1768 | 230 | 44.83 | 5.13 | ✓ |
| gemma3:27b | q13 | 1639 | 9 | 6.05 | 1.49 | N/A (fuera ámbito) |
| gemma3:27b | q14 | 1729 | 9 | 6.33 | 1.42 | N/A (fuera ámbito) |
| gemma3:27b | q15 | 1618 | 9 | 6.28 | 1.43 | N/A (fuera ámbito) |

## Resumen por modelo

### gemma3:4b
- Latencia media: 10.95s
- Tokens/s medio: 25.6
- Total preguntas: 15

### qwen2.5:3b
- Latencia media: 5.38s
- Tokens/s medio: 72.9
- Total preguntas: 15

### gpt-oss-120b
- Latencia media: 40.00s
- Tokens/s medio: 11.1
- Total preguntas: 15

### gemma3:27b
- Latencia media: 2.63s
- Tokens/s medio: 25.3
- Total preguntas: 15

## Interpretación

<!-- RELLENAR: Añadir análisis textual de los resultados del benchmark -->
<!-- Discutir: qué modelo rinde mejor, tradeoffs velocidad/calidad, etc. -->
