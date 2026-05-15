# Métricas propias — Banda 8

## 1. Source Coverage (Cobertura de fuentes)

**Definición**: Proporción de fuentes esperadas que aparecen efectivamente en las fuentes devueltas por el agente.

**Fórmula**:
```
source_coverage = |fuentes_esperadas ∩ fuentes_devueltas| / |fuentes_esperadas|
```

**Justificación**: En el dominio de DNI Valencia, es crítico que el agente cite las fuentes correctas. Un agente que responde bien pero cita fuentes incorrectas genera desconfianza. Esta métrica complementa el `context_recall` de RAGAs midiendo si las fuentes citadas son las que realmente contienen la información relevante.

**Rango**: [0, 1] donde 1 = todas las fuentes esperadas están citadas.

**Resultados**:
- **Cobertura de fuentes (Source Coverage)**: **77.78%** (0.7778)
- De 12 preguntas dentro del ámbito, el agente incluyó el 77.78% de las fuentes correctas en sus respuestas.

---

## 2. Rejection Accuracy (Precisión de rechazo)

**Definición**: Proporción de preguntas fuera de ámbito que el agente rechaza correctamente usando la frase literal "No tengo esa información en mis fuentes".

**Fórmula**:
```
rejection_accuracy = preguntas_rechazadas_correctamente / total_preguntas_fuera_de_ambito
```

**Justificación**: Para la asociación DNI Valencia, es especialmente importante que el agente **no invente información** sobre horarios, ubicaciones o actividades que no estén en el corpus. Un voluntario que recibe información falsa sobre un horario de desayuno podría acudir al lugar equivocado. Esta métrica mide directamente la fiabilidad del prompt anti-alucinación.

**Rango**: [0, 1] donde 1 = todas las preguntas fuera de ámbito se rechazan correctamente.

**Resultados**:
- **Precisión de rechazo (Rejection Accuracy)**: **100%** (1.0)
- De 3 preguntas fuera de ámbito (ej. recetas de paella o alquiler en Valencia), el agente rechazó correctamente las 3 usando la frase anti-alucinación exacta.
