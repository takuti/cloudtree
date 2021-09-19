import os
import requests
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from urllib.parse import urljoin


DEFAULT_SKIP_TAGS = [
    'head',
    'script',
    'style',
    'header',
    'nav',
    'aside',
    'footer',
    'code'
]


class CloudTree(object):

    def __init__(self, root_url):
        self.root_url = root_url
        self.texts = None
        self.wordcloud = None

    def traverse(self, max_depth=1, max_nodes=100, child_links_only=True,
                 skip_tags=DEFAULT_SKIP_TAGS, skip_selectors=[]):
        visited = set()
        queue = [(0, self.root_url)]

        texts = []
        while len(queue) > 0 and len(texts) <= max_nodes:
            depth, url = queue.pop(0)

            if url in visited:
                continue
            visited.add(url)

            try:
                res = requests.get(url)
            except Exception:
                continue
            if 'Content-Type' not in res.headers or \
                    not res.headers['Content-Type'].startswith('text/html'):
                continue
            html = res.text

            try:
                soup = BeautifulSoup(html, 'html.parser')
            except Exception:
                continue

            if depth < max_depth:
                urls = set(self.__extract_links(soup, child_links_only))
                queue += [(depth + 1, u) for u in urls if u not in visited]

            for element in soup.find_all(skip_tags):
                element.decompose()

            for selector in skip_selectors:
                for element in soup.select(selector):
                    element.decompose()

            texts.append(soup.get_text(' ', strip=True))
        self.texts = texts

    def to_wordcloud(self, **kwargs):
        assert self.texts is not None, 'call traverse() first'

        if 'stopwords' not in kwargs:
            kwargs['stopwords'] = set(STOPWORDS)
        self.wordcloud = WordCloud(**kwargs).generate(' '.join(self.texts))

    def get_mask(self, filename):
        return np.array(Image.open(filename))

    def fit_mask_color(self):
        assert self.wordcloud is not None and \
            self.wordcloud.mask is not None, \
            'call to_wordcloud(mask=mask) first'
        image_colors = ImageColorGenerator(self.wordcloud.mask)
        self.wordcloud = self.wordcloud.recolor(color_func=image_colors)

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

    def __extract_links(self, soup, child_links_only):
        for link in soup.select('a[href]'):
            href = link.attrs['href']

            if not child_links_only:
                yield href
                continue

            if href.startswith('/'):
                yield urljoin(self.root_url, href)
            elif href.startswith(self.root_url):
                yield href
            else:
                continue
