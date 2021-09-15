from cloudtree import CloudTree

tree = CloudTree('https://en.wikipedia.org/wiki/Tag_cloud')
tree.traverse()

mask = tree.get_mask('tree.png')
tree.to_wordcloud(
    random_state=1,
    background_color='white',
    colormap='Pastel1',
    collocations=False,
    max_font_size=64,
    mask=mask
)
tree.fit_mask_color()
tree.to_file('wordcloud.png')
