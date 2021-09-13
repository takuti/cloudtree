from setuptools import setup, find_packages

setup(
    name='cloudtree',
    version='0.0.1',
    description='Traverse a link tree given a root URL, and create a word cloud.',
    author='Takuya Kitazawa',
    author_email='k.takuti@gmail.com',
    license='MIT',
    url='https://github.com/takuti/cloudtree',
    packages=find_packages(exclude=['*tests*']),
    install_requires=[
        'wordcloud==1.8.1',
        'requests==2.19.1',
        'beautifulsoup4==4.10.0',
    ],
)
