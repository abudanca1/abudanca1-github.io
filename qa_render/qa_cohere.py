import cohere
import wikipediaapi
from numpy import dot
from numpy.linalg import norm


def run():
    API_KEY = "ZVbygf99raWTemslyvWjio9G4BvcP4XLgvxmFOox"
    co = cohere.Client(API_KEY)
    
    topics = ["Stadtumbau", "Bauplanungsrecht", "Stadterneuerung", "Städtebauförderung"]
    
    def cosine_sim(a, b):
        return dot(a, b) / (norm(a) * norm(b))

    # Wikipedia-Schnittstelle initialisieren
    wiki = wikipediaapi.Wikipedia(
        user_agent="MultiQABot/1.0 (you@example.com)",
        language="de"
    )

    paragraphs = []
    paragraph_topics = []

    # 🔍 1. Wikipedia-Absätze sammeln
    for topic in topics:
        page = wiki.page(topic)
        if page.exists():
            text = page.text
            paras = [p.strip() for p in text.split("\n") if len(p.strip()) > 100]
            paragraphs.extend(paras)
            paragraph_topics.extend([topic] * len(paras))
            print(f" '{topic}': {len(paras)} Absätze geladen.")
        else:
            print(f" '{topic}' nicht gefunden.")

    if not paragraphs:
        print(" Keine Inhalte geladen. Abbruch.")
        return

    # 🧠 2. Embeddings der Absätze
    embed_response = co.embed(
        texts=paragraphs,
        model="embed-multilingual-v3.0",
        input_type="search_document"
    )
    chunk_embeddings = embed_response.embeddings

    #  3. Frage stellen
    frage = input("\n Deine Frage: ").strip()
    frage_embedding = co.embed(
        texts=[frage],
        model="embed-multilingual-v3.0",
        input_type="search_query"
    ).embeddings[0]

    # 🔍 4. Semantisch ähnlichsten Absatz finden
    scores = [cosine_sim(frage_embedding, chunk) for chunk in chunk_embeddings]
    best_index = scores.index(max(scores))
    bester_chunk = paragraphs[best_index]
    quelle = paragraph_topics[best_index]

    # 🧾 5. Ausgabe + Cohere-Generierung
    print(f"\n📄 Relevanter Abschnitt aus: {quelle}")
    print(bester_chunk[:500] + "...")

    response = co.generate(
        model="command-r-plus",
        prompt=f"Answer the question based on the following context.\n\nContext:\n{bester_chunk}\n\nQuestion: {frage}\nAnswer:",
        max_tokens=200,
        temperature=0.7,
    )

    print("\n💬 Antwort:")
    print(response.generations[0].text.strip())

# Nur wenn du willst, dass es beim Laden automatisch läuft:

