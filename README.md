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
tree.to_file('source.txt')

mask = tree.get_mask('tree.png')
tree.to_wordcloud(
    width=800,
    height=600,
    random_state=1,
    background_color='white',
    colormap='Pastel1',
    collocations=False,
    max_font_size=64,
    mask=mask
)
tree.fit_mask_color()
tree.to_file('wordcloud.png')
```

Then you will see `source.txt` and `wordcloud.png` in the directory, which respectively represent a list of page contents and word cloud itself.
