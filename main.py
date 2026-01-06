from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
import spacy
import os
import sqlite3

# Incarcam modelul NLP
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

# Fișierele statice
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_PATH = "sneakeri.db"

def get_products_from_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sneakeri")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_path = os.path.join(os.getcwd(), "static", "index.html")
    with open(html_path, encoding="utf-8") as f:
        template = Template(f.read())
    return HTMLResponse(content=template.render(), status_code=200)

@app.get("/chat/")
def chat(query: str):
    common_responses = {
        "salut": "Bună! Cu ce pot ajuta?",
        "help": "Pot căuta sneakeri după: brand, model, culoare, mărime, preț sau disponibilitate",
        "mulțumesc": "Cu plăcere! Mai pot ajuta cu ceva?"
    }

    for pattern, response in common_responses.items():
        if pattern in query.lower():
            return {"response": response}

    query = query.lower()
    products = get_products_from_db()

    def remove_diacritics(text):
        diacritics = {'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't'}
        return ''.join(diacritics.get(c, c) for c in text)

    query_no_diacritics = remove_diacritics(query)
    doc = nlp(query)

    brand = next((b["brand"] for b in products
                  if remove_diacritics(b["brand"].lower()) in query_no_diacritics), None)

    model = next((m["model"] for m in products
                  if remove_diacritics(m["model"].lower()) in query_no_diacritics), None)

    colors = list({p["culoare"] for p in products})
    color = next((c for c in colors if remove_diacritics(c.lower()) in query_no_diacritics), None)

    size = None
    for token in doc:
        if token.text.isdigit():
            size = token.text
            break

    price_max = None
    for token in doc:
        if token.like_num:
            value = int(token.text)
            if any(w in query for w in ["lei", "ron", "sub", "maxim"]):
                price_max = value
                break

    check_stock = any(word in query for word in ["stoc", "disponibil", "stock", "disponibilitate", "exista"])

    filtered = products

    if brand:
        filtered = [p for p in filtered if p["brand"].lower() == brand.lower()]

    if model:
        filtered = [p for p in filtered if model.lower() in p["model"].lower()]

    if color:
        filtered = [p for p in filtered if remove_diacritics(color.lower()) in remove_diacritics(p["culoare"].lower())]

    if size:
        filtered = [p for p in filtered if size in p["marime"]]

    if price_max:
        filtered = [p for p in filtered if p["pret"] <= price_max]

    if check_stock:
        filtered = [p for p in filtered if p["stoc"] > 0]

    if not filtered:
        crit = []
        if brand: crit.append(f"brand: {brand}")
        if model: crit.append(f"model: {model}")
        if color: crit.append(f"culoare: {color}")
        if size: crit.append(f"mărime: {size}")
        if price_max: crit.append(f"preț maxim: {price_max} RON")

        return {
            "response": f"Nu am găsit produse cu {', '.join(crit)}...",
            "detalii": [f"Branduri disponibile: {', '.join(set(p['brand'] for p in products))}"]
        }

    product_list = []
    for p in filtered:
        stock_msg = "✅ Disponibil" if p["stoc"] > 0 else "❌ Stoc epuizat"
        product_list.append(
            f"{p['brand']} {p['model']} ({p['culoare']}) - {p['pret']} RON - {stock_msg}"
            f"{' - Mărimi: ' + p['marime'] if not size else ''}"
        )

    return {
        "response": f"Am găsit {len(filtered)} produse care corespund căutării tale:",
        "detalii": product_list
    }
