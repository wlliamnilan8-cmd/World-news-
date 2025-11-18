import requests
import json
import os

API_KEY = os.getenv("NEWSAPI_KEY")

# Fontes permitidas no plano gratuito
fontes = "globo,uol,exame,info-money,techcrunch"

url = f"https://newsapi.org/v2/top-headlines?sources={fontes}&pageSize=100&apiKey={API_KEY}"

resp = requests.get(url)
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

print("Arquivo noticias.json atualizado com sucesso!")
