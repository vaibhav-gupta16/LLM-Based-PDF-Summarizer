import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def summarize_chunk(chunk: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text clearly and concisely."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in 3-5 sentences:\n\n{chunk}"
                }
            ],
            max_tokens=300,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        return ""


def generate_summary(chunks: list) -> str:
    summaries = []
    print(f"Processing {len(chunks)} chunks...")

    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 50:
            continue
        print(f"Chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk[:3000])
        if summary:
            summaries.append(summary)
        time.sleep(0.5)  # small delay to respect rate limits

    if not summaries:
        return "⚠️ Could not generate summary."

    # Final consolidation pass
    merged = " ".join(summaries)
    print("Generating final consolidated summary...")
    final = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Consolidate the following partial summaries into one coherent, well-structured summary."
            },
            {
                "role": "user",
                "content": f"Consolidate these summaries into a single comprehensive summary:\n\n{merged[:6000]}"
            }
        ],
        max_tokens=800,
        temperature=0.3
    )
    return final.choices[0].message.content.strip()