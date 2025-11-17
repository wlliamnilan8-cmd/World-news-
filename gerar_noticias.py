import requests
import json
import datetime
import os

API_KEY = os.getenv("NEWSAPI_KEY")
URL = f"https://newsapi.org/v2/top-headlines?language=pt&apiKey={API_KEY}"

ARQUIVO = "noticias.json"

def carregar_existente():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def gerar():
    print("📡 Buscando notícias reais...")
    r = requests.get(URL)

    if r.status_code != 200:
        print("❌ ERRO:", r.text)
        return

    dados = r.json()
    artigos = dados.get("articles", [])

    noticias_antigas = carregar_existente()
    novas = []

    for a in artigos:
        novas.append({
            "titulo": a.get("title", "Sem título"),
            "descricao": a.get("description", "Sem descrição"),
            "imagem": a.get("urlToImage", "https://via.placeholder.com/800x400?text=Sem+Imagem"),
            "fonte": a.get("source", {}).get("name", ""),
            "data": datetime.datetime.utcnow().isoformat() + "Z"
        })

    tudo = novas + noticias_antigas  # mantém antigas e adiciona novas

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tudo, f, indent=4, ensure_ascii=False)

    print(f"🎉 {len(novas)} novas notícias adicionadas!")

gerar()
