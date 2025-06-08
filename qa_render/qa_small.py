import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

# Sicherstellen, dass Ressourcen verfügbar sind (einmal pro Serverstart)
nltk.download('punkt')
nltk.download('stopwords')

# Pfad zur JSON-Datei anpassen, falls nötig
json_path = os.path.join(os.path.dirname(__file__), "FrageAntwortListe.json")

# JSON-Datei laden
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Hauptfunktion
def run(user_input):
    frage = user_input.strip()
    tokens_data = word_tokenize(frage.lower())

    # Alle Tags zu Kleinbuchstaben
    for entry in data:
        entry["Tags"] = entry["Tags"].lower()

    for entry in data:
        tags = entry["Tags"]
        for token in tokens_data:
            if token in tags:
                antwort = entry["Antwort"]
                quelle = entry["Quelle"]
                return f"{antwort}\n\n📄 Quelle: {quelle}"

    return "Keine passende Antwort gefunden."
