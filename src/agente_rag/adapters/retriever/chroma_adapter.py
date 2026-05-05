import chromadb
from typing import List
from agente_rag.domain.entities import Chunk
from agente_rag.domain.ports import RetrieverPort

class ChromaRetriever:
    def __init__(self, path: str, collection_name: str, embed_fn):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_collection(name=collection_name)
        self.embed_fn = embed_fn

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        query_embedding = self.embed_fn(query)
        # Pedimos a Chroma que nos dé las distancias
        results = self.collection.query(
            query_embeddings=[query_embedding], 
            n_results=k
        )
        
        chunks = []
        for i in range(len(results['documents'][0])):
            distance = results['distances'][0][i]
            # Convertimos distancia a score de similitud (1 - distancia)[cite: 5]
            score = round(1.0 - distance, 4) 
            
            chunks.append(Chunk(
                text=results['documents'][0][i],
                source=results['metadatas'][0][i]['source'],
                score=score  # <--- YA NO ES NULL[cite: 5]
            ))
        return chunks