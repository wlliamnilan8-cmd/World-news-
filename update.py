import feedparser
import requests
import os
from datetime import datetime

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://rss.cnn.com/rss/edition_world.rss"
]

HTML_HEAD = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>World News</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<header><h1>World News</h1></header>
<div class="news-container">
"""

HTML_FOOT = """
</div>
<footer>&copy; 2025 World News - Atualizado automaticamente</footer>
</body>
</html>
"""

def baixar_imagem(url, index):
    try:
        img_data = requests.get(url, timeout=5).content
        img_name = f"image_{index}.jpg"
        with open(img_name, "wb") as f:
            f.write(img_data)
        return img_name
    except:
        return None

def gerar_resumo(texto):
    texto = texto.replace("\n", " ")
    return texto[:200] + "..."

def gerar_site():
    html = HTML_HEAD
    noticias = []
    
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        noticias.extend(feed.entries)
    
    for i, item in enumerate(noticias[:15]):
        titulo = item.get("title", "Sem título")
        link = item.get("link", "#")
        resumo = gerar_resumo(item.get("summary", "Notícia sem descrição."))
        
        imagem_url = None
        if "media_content" in item:
            imagem_url = item.media_content[0]["url"]
        elif "links" in item:
            for l in item.links:
                if l.get("type") and "image" in l["type"]:
                    imagem_url = l["href"]

        img_file = baixar_imagem(imagem_url, i) if imagem_url else None
        
        html += "<div class='news-card'>"
        if img_file:
            html += f"<img src='{img_file}' alt='image'>"
        
        html += f"""
        <div class='news-content'>
            <h2>{titulo}</h2>
            <p>{resumo}</p>
            <a href="{link}" target="_blank">Leia mais</a>
        </div>
        </div>
        """

    html += HTML_FOOT

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✔ Site atualizado com sucesso!")

if __name__ == "__main__":
    gerar_site()
