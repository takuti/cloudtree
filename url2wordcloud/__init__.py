import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
from urllib.parse import urljoin


def extract_all_links_under(root_url, soup):
    for link in soup.findAll('a'):
        href = link.attrs['href'] if 'href' in link.attrs else ''

        if href.startswith('/'):
            yield urljoin(root_url, href)
        elif href.startswith(root_url):
            yield href
        else:
            continue


def to_wordcloud(root_url, max_depth=1, output_filename='wordcloud.png'):
    visited = set()
    queue = [(0, root_url)]

    texts = []
    while len(queue) > 0:
        depth, url = queue.pop(0)

        if url in visited:
            continue
        visited.add(url)

        res = requests.get(url)
        if not res.headers['Content-Type'].startswith('text/html'):
            continue
        html = res.text

        try:
            soup = BeautifulSoup(html, 'html.parser')
        except Exception:
            continue

        if depth < max_depth:
            urls = set(extract_all_links_under(root_url, soup))
            queue += [(depth + 1, u) for u in urls if u not in visited]

        for script in soup.findAll(["script", "style", "header", "footer"]):
            script.decompose()

        texts.append(soup.get_text(' ', strip=True))

    wordcloud = WordCloud(
        width=3000,
        height=2000,
        random_state=1,
        background_color='salmon',
        colormap='Pastel1',
        collocations=False,
        stopwords=STOPWORDS
    ).generate(' '.join(texts))
    wordcloud.to_file(output_filename)
