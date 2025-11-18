import requests
import json
import os

# Pega a API KEY do Secrets do GitHub
API_KEY = os.getenv("NEWSDATA_API_KEY")

URL = "https://newsdata.io/api/1/news"

params = {
    "apikey": API_KEY,
    "country": "br",
    "language": "pt",
    "category": "top",
}

def main():
    print("=== INICIANDO COLETA DE NOTÍCIAS ===")
    print("API KEY usada:", API_KEY)

    # Fazer requisição
    resp = requests.get(URL, params=params)
    print("Status Code:", resp.status_code)

    # Mostrar parte da resposta bruta
    print("Resposta parcial da API:")
    print(resp.text[:300])

    # Tentar converter para JSON
    try:
        data = resp.json()
    except Exception as e:
        print("ERRO AO CONVERTER PARA JSON:", e)
        print("Resposta completa da API:")
        print(resp.text)
        return

    # Conferir se veio "results"
    if "results" not in data:
        print("A API NÃO RETORNOU 'results'. Resposta recebida:")
        print(data)
        return

    # Salvar notícias no arquivo
    try:
        with open("noticias.json", "w", encoding="utf-8") as f:
            json.dump(data["results"], f, indent=4, ensure_ascii=False)
        print("✔ noticias.json atualizado com sucesso!")
    except Exception as e:
        print("ERRO AO SALVAR noticias.json:", e)

    print("=== FINALIZADO ===")


if __name__ == "__main__":
    main()
