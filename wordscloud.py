import os
import sys

from wordcloud import WordCloud, STOPWORDS

os.chdir(sys.path[0])

#lendo fonte de palavras
texto = open('data/doc.txt', mode='r', encoding='utf-8').read()

stopwords = STOPWORDS

wc = WordCloud(
    background_color='white',
    stopwords=stopwords,
    height=300,
    width=1128,
)

wc.generate(texto)

wc.to_file('data/wordcloud_doc.png')
