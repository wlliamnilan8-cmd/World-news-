import json
import requests
import os

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_news():
    print("Iniciando coleta Newsdata.io...")

    url = (
        "https://newsdata.io/api/1/news"
        f"?apikey={NEWS_API_KEY}&country=br&language=pt&category=top"
    )

    print("GET", url)

    try:
        response = requests.get(url)
    except Exception as e:
        print("❌ Erro ao conectar à API:", e)
        return []

    if response.status_code != 200:
        print("❌ API retornou erro:", response.status_code, response.text)
        return []

    data = response.json()

    # "results" pode ser qualquer coisa → garantir lista
    results = data.get("results", [])
    if not isinstance(results, list):
        print("⚠️ 'results' não é lista:", results)
        return []

    return results


def normalize(results):
    noticias = []

    for r in results:

        # ignorar qualquer item inválido
        if not isinstance(r, dict):
            print("⚠️ Ignorando item inválido:", r)
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

        print("✔ noticias.json salvo com sucesso!")

    except Exception as e:
        print("❌ Erro ao salvar noticias.json:", e)


def main():
    if not NEWS_API_KEY:
        print("❌ ERRO: NEWSDATA_API_KEY não existe nos secrets!")
        return

    results = fetch_news()
    noticias = normalize(results)
    save_json(noticias)


if __name__ == "__main__":
    main()
