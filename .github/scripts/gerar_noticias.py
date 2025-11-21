import json
import requests
import os

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_news():
    print("Iniciando coleta Newsdata.io...")

    base_url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "country": "br",
        "language": "pt",
        "category": "top",
        "page": 0
    }

    # construir URL manualmente
    url = base_url + "?" + "&".join(f"{k}={v}" for k, v in params.items())

    print("GET", url)

    response = requests.get(url)

    # API retornou erro 4xx ou 5xx
    if response.status_code != 200:
        print("❌ Erro da API:", response.status_code, response.text)
        return []

    data = response.json()

    # se "results" não for lista → devolveu erro interno
    results = data.get("results", [])
    if not isinstance(results, list):
        print("⚠️ API devolveu formato inesperado:", results)
        return []

    return results


def normalize(results):
    noticias = []

    for r in results:

        # se a API devolveu string, número, None... ignorar
        if not isinstance(r, dict):
            print("⚠️ Item ignorado (não é objeto):", r)
            continue

        noticias.append({
            "titulo": r.get("title") or "Sem título",
            "descricao": r.get("description") or "",
            "imagem": r.get("image_url") or "",
            "fonte": r.get("source_id") or "",
            "link": r.get("link") or "",
            "data": r.get("pubDate") or ""
        })

    return noticias


def save_json(noticias):
    try:
        with open("noticias.json", "w", encoding="utf-8") as f:
            json.dump(noticias, f, ensure_ascii=False, indent=4)

        print("✔ noticias.json atualizado com sucesso!")

    except Exception as e:
        print("❌ Erro ao salvar noticias.json:", e)


def main():
    if not NEWS_API_KEY:
        print("❌ ERRO: NEWSDATA_API_KEY não encontrado nos secrets!")
        return

    results = fetch_news()
    if not results:
        print("⚠ Nenhuma notícia válida encontrada.")
        save_json([])  # grava arquivo vazio para evitar erros no site
        return

    noticias = normalize(results)
    save_json(noticias)


if __name__ == "__main__":
    main()
