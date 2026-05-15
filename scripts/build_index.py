"""Construye el índice vectorial desde corpus/.

Usa los adapters de la arquitectura hexagonal (embedder + retriever).
Ejecución: python scripts/build_index.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agente_rag.chunker import load_corpus, split_documents
from agente_rag.config import SETTINGS, _build_embedder, _build_retriever


def main() -> int:
    print(f"[build_index] corpus_dir       = {SETTINGS.corpus_dir}")
    print(f"[build_index] retriever        = {SETTINGS.retriever_backend}")
    print(f"[build_index] embedder         = {SETTINGS.embedder_backend}")
    print(f"[build_index] collection       = {SETTINGS.collection_name}")

    docs = load_corpus(SETTINGS.corpus_dir)
    print(f"[build_index] {len(docs)} documentos cargados.")

    chunks = split_documents(docs)
    print(f"[build_index] {len(chunks)} chunks generados.")

    # Instanciar adapters
    embedder = _build_embedder()
    retriever = _build_retriever(embedder.embed)

    # Resetear colección existente
    if hasattr(retriever, "reset_collection"):
        retriever.reset_collection()
        print("[build_index] Colección reseteada.")

    # Generar embeddings
    print("[build_index] Generando embeddings...")
    t0 = time.time()
    embeddings = []
    for i, chunk in enumerate(chunks):
        embeddings.append(embedder.embed(chunk.text))
        if (i + 1) % 20 == 0:
            print(f"  [{i + 1}/{len(chunks)}] embeddings generados...")

    print(f"[build_index] Embeddings en {time.time() - t0:.1f}s")

    # Indexar
    t1 = time.time()
    n = retriever.add_documents(
        ids=[c.id for c in chunks],
        embeddings=embeddings,
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "chunk_index": c.chunk_index} for c in chunks],
    )
    print(f"[build_index] {n} chunks indexados en {time.time() - t1:.1f}s.")
    print(f"[build_index] Total: {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
