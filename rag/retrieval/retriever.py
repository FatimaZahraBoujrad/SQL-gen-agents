# retriever.py

import chromadb
from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(self, persist_path="chroma_store", collection_name="kpi_docs"):
        print("🔍 Loading local embedding model...")
        self.embedder = SentenceTransformer("./rag/model/all-MiniLM-L6-v2-local")

        # Connect to Chroma persistent DB
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_collection(name=collection_name)

    def query(self, query_text: str, top_k: int = 5, where_clause: dict = None):
        print(f"\n🔍 Query: {query_text}")
        query_embedding = self.embedder.encode([query_text]).tolist()

        # Run the vector similarity query + optional metadata filter
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where=where_clause or None  # e.g. {"report": "Sales Report August"}
        )

        # Format results
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        scores = results.get("distances", [[]])[0]  # cosine similarity (lower = better)

        formatted = []
        for doc, meta, score in zip(documents, metadatas, scores):
            formatted.append({
                "text": doc,
                "metadata": meta,
                "score": score
            })

        return formatted
