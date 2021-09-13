CloudTree
===

Traverse a link tree given a root URL, and create a [word cloud](https://github.com/amueller/word_cloud).

### Installation

```sh
$ pip install git+https://github.com/takuti/cloudtree.git
```

### Usage

```py
from cloudtree import to_wordcloud
to_wordcloud(
  'https://takuti.me/',
  width=3000,
  height=2000,
  random_state=1,
  background_color='salmon',
  colormap='Pastel1',
  collocations=False
)
```

Then you will see `wordcloud.png` in the directory.
