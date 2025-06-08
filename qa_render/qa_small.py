import json



import nltk
from nltk.tokenize import word_tokenize
import os

# Nur punkt wird benötigt
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

# JSON laden
json_path = os.path.join(os.path.dirname(__file__), "FrageAntwortListe.json")
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

def run(user_input):
    frage = user_input.strip()
    tokens_data = word_tokenize(frage.lower())

    for entry in data:
        entry["Tags"] = entry["Tags"].lower()

    for entry in data:
        tags = entry["Tags"]
        for token in tokens_data:
            if token in tags:
                antwort = entry["Antwort"]
                quelle = entry["Quelle"]
                return f"{antwort}\n\n Quelle: {quelle}"

    return "Keine passende Antwort gefunden."
