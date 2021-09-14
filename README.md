CloudTree
===

Traverse a link tree given a root URL, and create a [word cloud](https://github.com/amueller/word_cloud).

### Installation

```sh
$ pip install git+https://github.com/takuti/cloudtree.git
```

### Usage

```py
from cloudtree import CloudTree

tree = CloudTree('https://takuti.me/')
tree.traverse()
tree.to_wordcloud(
  width=3000,
  height=2000,
  random_state=1,
  background_color='salmon',
  colormap='Pastel1',
  collocations=False
)
tree.to_file('source.txt')
tree.to_file('wordcloud.png')
```

Then you will see `source.txt` and `wordcloud.png` in the directory, which respectively represent a list of page contents and word cloud itself.
