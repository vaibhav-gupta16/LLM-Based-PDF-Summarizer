import os
import re
from collections import Counter

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if token not in STOP_WORDS and len(token) > 1
    ]


class QAEngine:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.chunk_tokens = [Counter(tokenize(chunk)) for chunk in chunks]

    def retrieve(self, query: str, top_k: int = 5) -> str:
        query_tokens = tokenize(query)
        if not query_tokens:
            return "\n\n".join(self.chunks[:top_k])

        scored_chunks = []
        unique_query_tokens = set(query_tokens)

        for chunk, chunk_token_counts in zip(self.chunks, self.chunk_tokens):
            overlap_score = sum(chunk_token_counts[token] for token in unique_query_tokens)
            phrase_bonus = sum(
                3 for token in unique_query_tokens if f" {token} " in f" {chunk.lower()} "
            )
            score = overlap_score + phrase_bonus
            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda item: item[0], reverse=True)
        relevant_chunks = [chunk for _, chunk in scored_chunks[:top_k]]

        if not relevant_chunks:
            relevant_chunks = self.chunks[:top_k]

        return "\n\n".join(relevant_chunks)

    def answer(self, question: str) -> str:
        context = self.retrieve(question)
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. Answer the question using only "
                            "the provided context. If the answer is not in the context, say so."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {question}",
                    },
                ],
                max_tokens=400,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
