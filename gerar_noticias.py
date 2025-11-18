import requests
import json
import os

API_KEY = os.getenv("NEWSDATA_API_KEY")

URL = "https://newsdata.io/api/1/news"

params = {
    "apikey": API_KEY,
    "country": "br",
    "language": "pt",
    "category": "top"
}

def main():
    print("Usando API KEY:", API_KEY)

    resp = requests.get(URL, params=params)
    print("Status Code:", resp.status_code)

    # Mostrar parte da resposta para debug
    print("Resposta da API (primeiros 200 chars):")
    print(resp.text[:200])

    # Converter resposta para JSON
    try:
        data = resp.json()
    except Exception as e:
        print("ERRO AO LER JSON DA API:", e)
        print("Resposta completa:")
        print(resp.text)
        return

    if "results" not in data:
        print("API retornou erro ou formato inesperado:")
        print(data)
        return

    with open("noticias.json", "w", encoding="utf-8") as f:
        json.dump(data["results"], f, indent=4, ensure_ascii=False)

    print("noticias.json atualizado com sucesso!")

if __name__ == "__main__":
    main()
