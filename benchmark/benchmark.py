"""Benchmark reproducible con 4 modelos (Banda 7).

Itera sobre cada par (modelo, pregunta) y guarda resultados en
benchmark/benchmark.json y benchmark/benchmark.md.

Uso:
    python benchmark/benchmark.py
    python benchmark/benchmark.py --modelos gemma3:4b,qwen2.5:3b
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agente_rag.pipeline import answer  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_FILE = REPO_ROOT / "benchmark" / "preguntas.json"
OUTPUT_JSON = REPO_ROOT / "benchmark" / "benchmark.json"
OUTPUT_MD = REPO_ROOT / "benchmark" / "benchmark.md"

# Modelos a evaluar: 2 locales + 2 PoliGPT
DEFAULT_MODELS = [
    {"alias": "gemma3:4b", "servidor": "ollama_local", "backend": "ollama"},
    {"alias": "qwen2.5:3b", "servidor": "ollama_local", "backend": "ollama"},
    {"alias": "poligpt", "servidor": "poligpt", "backend": "poligpt"},
    {"alias": "poligpt-2", "servidor": "poligpt", "backend": "poligpt"},
]


def run_benchmark(models: list[dict], questions: list[dict]) -> list[dict]:
    results = []

    for model in models:
        print(f"\n{'='*60}")
        print(f"  Modelo: {model['alias']} ({model['servidor']})")
        print(f"{'='*60}")

        for i, q in enumerate(questions, 1):
            t0 = time.time()
            try:
                res = answer(
                    q["pregunta"],
                    model_override=model["alias"],
                )
                error = None
            except Exception as exc:
                res = {"respuesta": "", "fuentes": [], "chunks": [], "metricas": {}, "trazas": []}
                error = str(exc)
            elapsed = time.time() - t0

            metricas = res.get("metricas", {})
            print(f"  [{i}/{len(questions)}] ({elapsed:.1f}s) {q['pregunta'][:50]}...")

            results.append({
                "modelo": model["alias"],
                "servidor": model["servidor"],
                "id": q.get("id", f"q{i}"),
                "pregunta": q["pregunta"],
                "categoria": q.get("categoria", ""),
                "fuentes_esperadas": q.get("fuentes_esperadas", []),
                "respuesta": res["respuesta"],
                "fuentes": res["fuentes"],
                "metricas": {
                    "prompt_tokens": metricas.get("prompt_tokens", 0),
                    "output_tokens": metricas.get("output_tokens", 0),
                    "tokens_per_sec": metricas.get("tokens_per_sec", 0),
                    "latencia_s": metricas.get("latencia_s", round(elapsed, 2)),
                },
                "error": error,
            })

    return results


def generate_markdown(results: list[dict], questions: list[dict]) -> str:
    """Genera benchmark.md con tabla legible e interpretación."""
    lines = [
        "# Benchmark — Comparativa de 4 modelos",
        "",
        f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Preguntas: {len(questions)}",
        "",
        "## Tabla de resultados",
        "",
        "| Modelo | Pregunta | Tokens IN | Tokens OUT | Tok/s | Latencia (s) | Acierto |",
        "|--------|----------|-----------|------------|-------|-------------|---------|",
    ]

    for r in results:
        m = r["metricas"]
        # Acierto subjetivo: comprobar si las fuentes esperadas están en las devueltas
        esperadas = set(r["fuentes_esperadas"])
        devueltas = set(r["fuentes"])
        if not esperadas:
            acierto = "N/A (fuera ámbito)" if "fuera" in r.get("categoria", "") else "—"
        elif esperadas & devueltas:
            acierto = "✓"
        else:
            acierto = "✗"

        lines.append(
            f"| {r['modelo']} | {r['id']} | {m['prompt_tokens']} | "
            f"{m['output_tokens']} | {m['tokens_per_sec']} | "
            f"{m['latencia_s']} | {acierto} |"
        )

    lines.extend([
        "",
        "## Resumen por modelo",
        "",
    ])

    # Agrupar por modelo
    modelos = {}
    for r in results:
        modelos.setdefault(r["modelo"], []).append(r)

    for modelo, runs in modelos.items():
        avg_latencia = sum(r["metricas"]["latencia_s"] for r in runs) / len(runs)
        avg_tps = sum(r["metricas"]["tokens_per_sec"] for r in runs) / len(runs)
        lines.append(f"### {modelo}")
        lines.append(f"- Latencia media: {avg_latencia:.2f}s")
        lines.append(f"- Tokens/s medio: {avg_tps:.1f}")
        lines.append(f"- Total preguntas: {len(runs)}")
        lines.append("")

    lines.extend([
        "## Interpretación",
        "",
        "<!-- RELLENAR: Añadir análisis textual de los resultados del benchmark -->",
        "<!-- Discutir: qué modelo rinde mejor, tradeoffs velocidad/calidad, etc. -->",
        "",
    ])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark de modelos LLM")
    parser.add_argument("--modelos", type=str, default=None,
                        help="Lista de modelos separados por coma (ej: gemma3:4b,qwen2.5:3b)")
    args = parser.parse_args()

    if not QUESTIONS_FILE.exists():
        print(f"No existe {QUESTIONS_FILE}", file=sys.stderr)
        return 1

    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))

    if args.modelos:
        models = [{"alias": m.strip(), "servidor": "ollama_local", "backend": "ollama"}
                  for m in args.modelos.split(",")]
    else:
        models = DEFAULT_MODELS

    print(f"[benchmark] {len(questions)} preguntas × {len(models)} modelos")
    results = run_benchmark(models, questions)

    # Guardar JSON
    OUTPUT_JSON.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n[benchmark] JSON → {OUTPUT_JSON}")

    # Guardar Markdown
    md = generate_markdown(results, questions)
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"[benchmark] MD   → {OUTPUT_MD}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
