"""Adapter Retriever con FAISS — segunda implementación del RetrieverPort.

Demuestra la intercambiabilidad de la arquitectura hexagonal:
cambiar de ChromaDB a FAISS = 1 línea en config.py.
"""

import json
from pathlib import Path
from typing import List

import faiss
import numpy as np

from agente_rag.domain.entities import Chunk


class FAISSRetriever:
    """Retriever semántico usando FAISS (Facebook AI Similarity Search)."""

    def __init__(self, index_path: str, embed_fn, dim: int = 768):
        self.index_path = Path(index_path)
        self.embed_fn = embed_fn
        self.dim = dim
        self.index = None
        self.metadatas: list[dict] = []
        self.documents: list[str] = []
        self._load_or_create()

    def _load_or_create(self):
        meta_path = self.index_path / "faiss_meta.json"
        idx_path = self.index_path / "faiss.index"

        if idx_path.exists() and meta_path.exists():
            self.index = faiss.read_index(str(idx_path))
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            self.metadatas = data["metadatas"]
            self.documents = data["documents"]
        else:
            self.index = faiss.IndexFlatIP(self.dim)  # Inner product (coseno tras normalizar)

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        if self.index is None or self.index.ntotal == 0:
            return []

        q_emb = np.array([self.embed_fn(query)], dtype=np.float32)
        faiss.normalize_L2(q_emb)

        k = min(k, self.index.ntotal)
        scores, indices = self.index.search(q_emb, k)

        chunks = []
        for i, idx in enumerate(indices[0]):
            if idx < 0:
                continue
            chunks.append(Chunk(
                text=self.documents[idx],
                source=self.metadatas[idx]["source"],
                score=round(float(scores[0][i]), 4),
            ))
        return chunks

    # --- VectorStorePort ---

    def add_documents(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> int:
        vecs = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(vecs)
        self.index.add(vecs)
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)
        self._save()
        return self.index.ntotal

    def reset_collection(self) -> None:
        self.index = faiss.IndexFlatIP(self.dim)
        self.metadatas = []
        self.documents = []
        idx_path = self.index_path / "faiss.index"
        meta_path = self.index_path / "faiss_meta.json"
        if idx_path.exists():
            idx_path.unlink()
        if meta_path.exists():
            meta_path.unlink()

    def _save(self):
        self.index_path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path / "faiss.index"))
        (self.index_path / "faiss_meta.json").write_text(
            json.dumps({"metadatas": self.metadatas, "documents": self.documents},
                       ensure_ascii=False),
            encoding="utf-8",
        )
