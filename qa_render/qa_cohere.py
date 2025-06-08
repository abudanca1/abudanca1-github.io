import cohere
import wikipediaapi
from numpy import dot
from numpy.linalg import norm
import os

def run(user_input):
    # 🔐 API-Key sicher aus Environment Variable laden
   API_KEY = "ZVbygf99raWTemslyvWjio9G4BvcP4XLgvxmFOox"
   co = cohere.Client(API_KEY)
   topics = ["Stadtumbau", "Bauplanungsrecht", "Stadterneuerung", "Städtebauförderung"]
   
   def cosine_sim(a, b):
        return dot(a, b) / (norm(a) * norm(b))

    # Wikipedia API initialisieren
    wiki = wikipediaapi.Wikipedia(
        user_agent="MultiQABot/1.0 (you@example.com)",
        language="de"
    )

    paragraphs = []
    paragraph_topics = []

    # 🔍 Wikipedia-Absätze sammeln
    for topic in topics:
        page = wiki.page(topic)
        if page.exists():
            text = page.text
            paras = [p.strip() for p in text.split("\n") if len(p.strip()) > 100]
            paragraphs.extend(paras)
            paragraph_topics.extend([topic] * len(paras))

    if not paragraphs:
        return " Keine Wikipedia-Inhalte gefunden."

    # Embeddings der Absätze
    embed_response = co.embed(
        texts=paragraphs,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )
    chunk_embeddings = embed_response.embeddings

    # Embedding der Frage
    frage_embedding = co.embed(
        texts=[user_input],
        model="embed-multilingual-v3.0",
        input_type="search_query"
    ).embeddings[0]

    # Ähnlichster Absatz
    scores = [cosine_sim(frage_embedding, chunk) for chunk in chunk_embeddings]
    best_index = scores.index(max(scores))
    bester_chunk = paragraphs[best_index]
    quelle = paragraph_topics[best_index]

    # Antwort generieren
    response = co.generate(
        model="command-r-plus",
        prompt=f"Beantworte die Frage auf Basis des Kontexts.\n\nKontext:\n{bester_chunk}\n\nFrage: {user_input}\nAntwort:",
        max_tokens=200,
        temperature=0.7,
    )

    antwort = response.generations[0].text.strip()

    return f"{antwort}\n\n Quelle: {quelle}"


