#!/usr/bin/env python3
import requests
import json
import os
import sys

API_KEY = os.getenv("NEWSDATA_API_KEY")
if not API_KEY:
    print("ERRO: variável NEWSDATA_API_KEY não encontrada.", file=sys.stderr)
    sys.exit(1)

URL = "https://newsdata.io/api/1/news"
params = {
    "apikey": API_KEY,
    "country": "br",
    "language": "pt",
    "category": "top",
    "page": 0,
    "page_size": 100
}

def fetch_all():
    # Some endpoints support pagination; loop until done (safe)
    all_results = []
    page = 0
    while True:
        params["page"] = page
        resp = requests.get(URL, params=params, timeout=30)
        print("GET", resp.url, "→", resp.status_code)
        try:
            data = resp.json()
        except Exception as e:
            print("ERRO ao ler JSON:", e)
            print("Resposta bruta:", resp.text[:1000])
            return None

        results = data.get("results") or []
        if not results:
            break

        all_results.extend(results)
        # stop if less than page_size
        if len(results) < params["page_size"]:
            break
        page += 1
        # safety limit
        if page > 5:
            break

    return all_results

def normalize(results):
    out = []
    for r in results:
        out.append({
            "titulo": r.get("title") or r.get("title_noFormatting") or "Sem título",
            "descricao": r.get("description") or r.get("summary") or "",
            "imagem": r.get("image_url") or r.get("image") or "https://via.placeholder.com/800x400",
            "link": r.get("link") or r.get("url") or r.get("source_id") or "#",
            # tentar pegar categoria se existir
            "categoria": (r.get("category") or (r.get("categories") and r.get("categories")[0]) or "outros").lower()
        })
    return out

def save_json(data):
    with open("noticias.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("Iniciando coleta Newsdata.io...")
    results = fetch_all()
    if results is None:
        print("Falha na coleta.", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("Nenhum resultado retornado pela API.")
        save_json([])
        return

    dados = normalize(results)
    save_json(dados)
    print("noticias.json atualizado: ", len(dados), "notícias")

if __name__ == "__main__":
    main()
