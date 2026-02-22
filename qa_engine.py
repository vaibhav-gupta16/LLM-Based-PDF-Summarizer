import os
import numpy as np
import faiss
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
embedder = SentenceTransformer("all-MiniLM-L6-v2")


class QAEngine:
    def __init__(self, chunks: list):
        self.chunks = chunks
        self.index = None
        self._build_index()

    def _build_index(self):
        embeddings = embedder.encode(self.chunks, show_progress_bar=False)
        embeddings = np.array(embeddings).astype("float32")
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 5) -> str:
        query_emb = embedder.encode([query]).astype("float32")
        _, indices = self.index.search(query_emb, top_k)
        relevant = [self.chunks[i] for i in indices[0] if i < len(self.chunks)]
        return "\n\n".join(relevant)

    def answer(self, question: str) -> str:
        context = self.retrieve(question)
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Answer the question using only the provided context. If the answer is not in the context, say so."
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {question}"
                    }
                ],
                max_tokens=400,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"