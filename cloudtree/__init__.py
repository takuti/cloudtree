import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
from urllib.parse import urljoin


class CloudTree(object):

    def __init__(self, root_url):
        self.root_url = root_url
        self.texts = None
        self.wordcloud = None

    def traverse(self, max_depth=1):
        visited = set()
        queue = [(0, self.root_url)]

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
                urls = set(self.__extract_all_child_links(soup))
                queue += [(depth + 1, u) for u in urls if u not in visited]

            ignore_tags = ['script', 'style', 'header', 'footer']
            for script in soup.findAll(ignore_tags):
                script.decompose()

            texts.append(soup.get_text(' ', strip=True))
        self.texts = texts

    def to_wordcloud(self, **kwargs):
        assert self.texts is not None, 'call traverse() first'

        if 'stopwords' not in kwargs:
            kwargs['stopwords'] = STOPWORDS
        self.wordcloud = WordCloud(**kwargs).generate(' '.join(self.texts))

    def save_wordcloud(self, output_filename):
        assert self.wordcloud is not None, 'call to_wordcloud() first'

        self.wordcloud.to_file(output_filename)

    def __extract_all_child_links(self, soup):
        for link in soup.findAll('a'):
            href = link.attrs['href'] if 'href' in link.attrs else ''

            if href.startswith('/'):
                yield urljoin(self.root_url, href)
            elif href.startswith(self.root_url):
                yield href
            else:
                continue
