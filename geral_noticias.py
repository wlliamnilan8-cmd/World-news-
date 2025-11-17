import requests
import json
import os
import sys

API_KEY = os.getenv("NEWSAPI_KEY")

if not API_KEY:
    print("ERRO: A variável de ambiente NEWSAPI_KEY não foi encontrada.")
    print("Configure sua API KEY nos Secrets do GitHub.")
    sys.exit(1)

url = (
    "https://newsapi.org/v2/top-headlines?"
    "language=pt&country=br&pageSize=200&apiKey=" + API_KEY
)

resp = requests.get(url)

if resp.status_code != 200:
    print("ERRO NA API:", resp.text)
    sys.exit(1)

dados = resp.json()
artigos = dados.get("articles", [])

noticias_formatadas = []
for a in artigos:
    noticias_formatadas.append({
        "titulo": a.get("title", "Sem título"),
        "descricao": a.get("description", "Sem descrição"),
        "imagem": a.get("urlToImage", "https://via.placeholder.com/800x400"),
        "link": a.get("url", "#")
    })

with open("noticias.json", "w", encoding="utf-8") as arq:
    json.dump(noticias_formatadas, arq, ensure_ascii=False, indent=4)

print("✔️ Arquivo noticias.json atualizado com", len(noticias_formatadas), "notícias.")
