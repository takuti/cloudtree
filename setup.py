from setuptools import setup, find_packages

setup(
    name='url2wordcloud',
    version='0.0.1',
    description='Create wordcloud from URL',
    author='Takuya Kitazawa',
    author_email='k.takuti@gmail.com',
    license='MIT',
    url='https://github.com/takuti/url2wordcloud',
    packages=find_packages(exclude=['*tests*']),
    install_requires=[
        'wordcloud==1.8.1',
        'requests==2.19.1',
        'beautifulsoup4==4.10.0',
    ],
)
