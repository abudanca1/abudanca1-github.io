from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import importlib
import qa_cohere
import qa_small
import nltk

# NLTK-Ressourcen beim Start herunterladen
nltk.download('punkt')
nltk.download('stopwords')

# Module neu laden (optional, z.B. für Live-Reload in Dev)
importlib.reload(qa_cohere)
importlib.reload(qa_small)

# FastAPI-Anwendung
app = FastAPI()

# Verzeichnis für HTML-Templates
templates = Jinja2Templates(directory="templates")

# GET: Formular anzeigen
@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("qa.html", {"request": request, "result": None})

# POST: Anfrage verarbeiten
@app.post("/", response_class=HTMLResponse)
def form_post(request: Request, user_input: str = Form(...)):
    try:
        result = qa_cohere.run(user_input)
        method = "Version 1 (Cohere)"
        source = "Quelle: Wikipedia"
    except Exception as e:
        result = qa_small.run(user_input)
        method = "Version 2 (lokal)"
        source = "Kein Wikipedia-Zugriff"

    return templates.TemplateResponse("qa.html", {
        "request": request,
        "result": result,
        "method": method,
        "source": source
    })
