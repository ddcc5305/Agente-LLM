"""Evaluación con RAGAs + métricas propias (Banda 8).

Evalúa las 4 métricas RAGAs exigidas:
  - faithfulness
  - answer_relevancy
  - context_precision
  - context_recall

Más 2 métricas propias:
  - source_coverage: % de fuentes esperadas presentes en la respuesta
  - rejection_accuracy: % de preguntas fuera de ámbito correctamente rechazadas

Uso:
    python evaluacion/eval_ragas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

REPO_ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_FILE = REPO_ROOT / "benchmark" / "preguntas.json"
OUTPUT_FILE = REPO_ROOT / "evaluacion" / "ragas_results.json"

REJECTION_PHRASE = "No tengo esa información en mis fuentes"


def run_pipeline(questions: list[dict]) -> list[dict]:
    """Ejecuta el pipeline RAG sobre las preguntas y recoge datos para RAGAs."""
    from agente_rag.pipeline import answer

    dataset_rows = []
    for q in questions:
        res = answer(q["pregunta"])
        contexts = [c["text"] for c in res.get("chunks", [])]
        dataset_rows.append({
            "question": q["pregunta"],
            "answer": res["respuesta"],
            "contexts": contexts,
            "ground_truth": q.get("ground_truth", ""),
            "fuentes_esperadas": q.get("fuentes_esperadas", []),
            "fuentes_devueltas": res.get("fuentes", []),
            "categoria": q.get("categoria", ""),
        })
    return dataset_rows


def evaluate_ragas(dataset_rows: list[dict]) -> dict:
    """Evalúa con las 4 métricas RAGAs."""
    try:
        import warnings
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        
        from ragas import evaluate
        from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
        from datasets import Dataset
        from ragas.run_config import RunConfig

        eval_data = {
            "question": [r["question"] for r in dataset_rows],
            "answer": [r["answer"] for r in dataset_rows],
            "contexts": [r["contexts"] for r in dataset_rows],
            "ground_truth": [r["ground_truth"] for r in dataset_rows],
        }

        from langchain_ollama import ChatOllama, OllamaEmbeddings
        
        # Usamos Ollama local para evaluar con temperatura 0 para mayor consistencia
        evaluator_llm = ChatOllama(model="gemma3:4b", temperature=0.0)
        evaluator_embeddings = OllamaEmbeddings(model="nomic-embed-text")

        dataset = Dataset.from_dict(eval_data)
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
            run_config=RunConfig(max_workers=1, timeout=60, max_retries=1)
        )
        df = result.to_pandas()
        scores = {}
        for key in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
            if key in df.columns:
                # Calculamos la media ignorando valores nulos (NaN)
                val = df[key].mean()
                import pandas as pd
                scores[key] = float(val) if pd.notna(val) else None
            else:
                print(f"[eval_ragas] Advertencia: Métrica '{key}' no se generó (posible fallo de Timeout).")
                scores[key] = None
        
        return scores

    except Exception as exc:
        import traceback
        print(f"[eval_ragas] Error con RAGAs: {exc}")
        print(traceback.format_exc())
        print("[eval_ragas] Calculando métricas manualmente como fallback...")
        return {"error": str(exc), "nota": "Ejecutar con Ollama activo y modelo cargado"}


def evaluate_custom_metrics(dataset_rows: list[dict]) -> dict:
    """Calcula las 2 métricas propias."""

    # Métrica 1: Source Coverage (cobertura de fuentes)
    source_scores = []
    for r in dataset_rows:
        esperadas = set(r["fuentes_esperadas"])
        devueltas = set(r["fuentes_devueltas"])
        if esperadas:
            coverage = len(esperadas & devueltas) / len(esperadas)
            source_scores.append(coverage)

    source_coverage = sum(source_scores) / len(source_scores) if source_scores else 0.0

    # Métrica 2: Rejection Accuracy (precisión de rechazo)
    fuera_ambito = [r for r in dataset_rows if r["categoria"] == "fuera_de_ambito"]
    if fuera_ambito:
        rechazadas_ok = sum(
            1 for r in fuera_ambito
            if REJECTION_PHRASE.lower() in r["answer"].lower()
        )
        rejection_accuracy = rechazadas_ok / len(fuera_ambito)
    else:
        rejection_accuracy = 0.0

    return {
        "source_coverage": round(source_coverage, 4),
        "rejection_accuracy": round(rejection_accuracy, 4),
        "source_coverage_detail": {
            "descripcion": "Proporción de fuentes esperadas que aparecen en las fuentes devueltas",
            "total_preguntas_evaluadas": len(source_scores),
            "scores": source_scores,
        },
        "rejection_accuracy_detail": {
            "descripcion": "Proporción de preguntas fuera de ámbito rechazadas correctamente con la frase literal",
            "total_fuera_ambito": len(fuera_ambito),
            "rechazadas_correctamente": sum(1 for r in fuera_ambito if REJECTION_PHRASE.lower() in r["answer"].lower()),
        },
    }


def main() -> int:
    if not QUESTIONS_FILE.exists():
        print(f"No existe {QUESTIONS_FILE}", file=sys.stderr)
        return 1

    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    print(f"[eval_ragas] {len(questions)} preguntas")

    # 1. Ejecutar pipeline
    print("[eval_ragas] Ejecutando pipeline...")
    dataset_rows = run_pipeline(questions)

    # 2. RAGAs
    print("[eval_ragas] Evaluando con RAGAs...")
    ragas_results = evaluate_ragas(dataset_rows)

    # 3. Métricas propias
    print("[eval_ragas] Calculando métricas propias...")
    custom_results = evaluate_custom_metrics(dataset_rows)

    # 4. Guardar todo
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "ragas": ragas_results,
        "metricas_propias": custom_results,
        "datos_crudos": dataset_rows,
    }
    OUTPUT_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"[eval_ragas] Resultados guardados en {OUTPUT_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
