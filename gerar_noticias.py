#!/usr/bin/env python3
# gerar_noticias.py
# Gera index.html a partir de index_template.html usando feeds RSS

import feedparser
import html
import re
import time

# --- CONFIGURAÇÃO ---
FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.reuters.com/reuters/worldNews",
    "https://apnews.com/apf-intlnews?format=xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
]

MAX_PER_FEED = 4   # notícias por fonte (ajuste se quiser)
TOTAL_MAX = 20     # limite total diário
TEMPLATE_FILE = "index_template.html"
OUTPUT_FILE = "index.html"

# --- FUNÇÕES AUXILIARES ---
def clean_html(raw):
    if not raw:
        return ""
    text = re.sub(r'<[^>]+>', '', raw)
    return html.unescape(text).strip()

def short_summary(entry):
    candidates = []
    if 'summary' in entry and entry.summary:
        candidates.append(clean_html(entry.summary))
    if 'description' in entry and entry.description:
        candidates.append(clean_html(entry.description))
    if not candidates:
        return ""
    text = candidates[0]
    words = text.split()
    if len(words) <= 30:
        return text
    return ' '.join(words[:30]) + '...'

def extract_image(entry):
    # media_content
    if 'media_content' in entry:
        try:
            url = entry.media_content[0].get('url')
            if url:
                return url
        except:
            pass
    # media_thumbnail
    if 'media_thumbnail' in entry:
        try:
            url = entry.media_thumbnail[0].get('url')
            if url:
                return url
        except:
            pass
    # enclosure links
    if 'links' in entry:
        for link in entry.links:
            if link.get('type','').startswith('image'):
                return link.get('href')
    # some entries have 'image' field
    if 'image' in entry and isinstance(entry.image, dict):
        return entry.image.get('href') or entry.image.get('url')
    return None

def build_card(entry):
    title = html.escape(entry.title) if 'title' in entry else "Sem título"
    link = entry.link if 'link' in entry else "#"
    image = extract_image(entry) or "https://via.placeholder.com/800x450?text=World+News"
    summary = short_summary(entry)
    card = f'''
    <article class="card">
      <img src="{image}" alt="imagem">
      <div class="card-content">
        <h3><a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a></h3>
        <p>{html.escape(summary)}</p>
        <div class="meta"><a href="{link}" target="_blank" rel="noopener noreferrer">Leia na fonte</a></div>
      </div>
    </article>
    '''
    return card

def main():
    cards = []
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print("Erro lendo feed:", feed_url, e)
            continue
        entries = getattr(feed, 'entries', [])[:MAX_PER_FEED]
        for e in entries:
            try:
                cards.append(build_card(e))
            except Exception as exc:
                print("Erro item:", exc)
            if len(cards) >= TOTAL_MAX:
                break
        if len(cards) >= TOTAL_MAX:
            break
        time.sleep(0.3)  # pequeno delay entre feeds

    grid_html = "\n".join(cards)

    # ler template e substituir marcador
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            tpl = f.read()
    except FileNotFoundError:
        print("Template não encontrado:", TEMPLATE_FILE)
        return

    out_html = tpl.replace("<!-- NEWS_GOES_HERE -->", grid_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(out_html)

    print(f"Gerei {OUTPUT_FILE} com {len(cards)} cards.")

if __name__ == "__main__":
    main()
