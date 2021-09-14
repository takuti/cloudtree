import os
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
from urllib.parse import urljoin


class CloudTree(object):

    def __init__(self, root_url):
        self.root_url = root_url
        self.texts = None
        self.wordcloud = None

    def traverse(self, max_depth=1, max_nodes=100,
                 ignore_tags=['script', 'style', 'header', 'footer', 'code']):
        visited = set()
        queue = [(0, self.root_url)]

        texts = []
        while len(queue) > 0 and len(texts) <= max_nodes:
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
                urls = set(self.__extract_all_child_links(soup))
                queue += [(depth + 1, u) for u in urls if u not in visited]

            for script in soup.findAll(ignore_tags):
                script.decompose()

            texts.append(soup.get_text(' ', strip=True))
        self.texts = texts

    def to_wordcloud(self, **kwargs):
        assert self.texts is not None, 'call traverse() first'

        if 'stopwords' not in kwargs:
            kwargs['stopwords'] = STOPWORDS
        self.wordcloud = WordCloud(**kwargs).generate(' '.join(self.texts))

    def to_file(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.txt':
            assert self.texts is not None, 'call traverse() first'
            with open(filename, 'w') as f:
                for text in self.texts:
                    f.write(text)
                    f.write('\n')
        else:
            assert self.wordcloud is not None, 'call to_wordcloud() first'
            self.wordcloud.to_file(filename)

    def __extract_all_child_links(self, soup):
        for link in soup.findAll('a'):
            href = link.attrs['href'] if 'href' in link.attrs else ''

            if href.startswith('/'):
                yield urljoin(self.root_url, href)
            elif href.startswith(self.root_url):
                yield href
            else:
                continue
