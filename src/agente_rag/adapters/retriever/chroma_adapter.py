"""Adapter Retriever + VectorStore → ChromaDB persistente.

Implementa RetrieverPort (búsqueda) y VectorStorePort (indexación).
Métrica coseno: score = 1 - distance → más alto = mejor.
"""

from typing import List

import chromadb

from agente_rag.domain.entities import Chunk


class ChromaRetriever:
    """Retriever semántico usando ChromaDB en disco."""

    def __init__(self, path: str, collection_name: str, embed_fn):
        self.path = path
        self.collection_name = collection_name
        self.embed_fn = embed_fn
        self.client = chromadb.PersistentClient(path=path)
        # Intentar abrir colección existente; si no existe, crear con coseno
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except Exception:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},
            )

    # --- RetrieverPort ---

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        if self.collection.count() == 0:
            return []

        query_embedding = self.embed_fn(query)
        k = min(k, self.collection.count())
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )

        chunks = []
        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            score = round(1.0 - distance, 4)
            chunks.append(Chunk(
                text=results["documents"][0][i],
                source=results["metadatas"][0][i]["source"],
                score=score,
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
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
        return self.collection.count()

    def reset_collection(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self.client.create_collection(
            self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )