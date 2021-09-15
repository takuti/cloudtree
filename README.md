CloudTree
===

Traverse a link tree given a root URL, and create a [word cloud](https://github.com/amueller/word_cloud).

![wordcloud](./examples/wordcloud.png)

### Installation

```sh
$ pip install git+https://github.com/takuti/cloudtree.git
```

### Usage

```py
from cloudtree import CloudTree

tree = CloudTree('https://takuti.me/')
tree.traverse()

tree.to_wordcloud()
tree.to_file('wordcloud.png')
```
