
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')


# JSON-Datei laden
with open("FrageAntwortListe.json", "r", encoding="utf-8") as file:
    data = json.load(file)
import json
from nltk.tokenize import word_tokenize

def run():
    # Tags auf Kleinbuchstaben setzen
    for entry in data:
        entry["Tags"] = entry["Tags"].lower()

    # Benutzereingabe
    frage = input("Geben Sie Ihre Frage ein: ").strip()
    tokens_data = word_tokenize(frage.lower())

    found = False
    for entry in data:
        tags = entry["Tags"]
        for token in tokens_data:
            if token in tags:
                print("\nAntwort:", entry["Antwort"])
                print("Quelle:", entry["Quelle"], "\n")
                found = True
                break  # Innere Schleife verlassen
        if found:
            break  # Äußere Schleife verlassen, wenn Treffer gefunden

    if not found:
        print("Keine passende Antwort gefunden.")
