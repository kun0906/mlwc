
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from functools import partial
from nlp import *

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

sns.set(style='darkgrid', context='talk', palette='colorblind')


def plot_wordcloud(csv_file, column='title', dpi=300, sep='|'):
    """
    https://github.com/amueller/word_cloud/blob/master/examples/simple.py

    Minimal Example
    ===============
    Generating a square wordcloud from the US constitution using default arguments.
    """

    from wordcloud import WordCloud

    df = pd.read_csv(csv_file, index_col=0, sep=sep)
    if column == 'keywords':
        words = pd.Series(', '.join(df['keywords'].dropna().apply(partial(transform, stopword=False))).lower().
            replace(' learn',' learning').split(',')).str.strip()
    else:
        words = pd.Series(' '.join(df[column].dropna().apply(transform)).split(' ')).str.strip()
    text_str = '\t'.join(words)

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text_str)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(f'{csv_file}, {column}')
    plt.tight_layout()
    plt.savefig(f'{csv_file}.png', dpi=dpi, bbox_inches='tight')
    plt.show()


def plot_wordranking(csv_file, column='title', dpi=300, sep='|'):
    """
    https://github.com/EdisonLeeeee/ICLR2023-OpenReviewData/blob/master/visualization.ipynb

    """

    df = pd.read_csv(csv_file, index_col=0, sep=sep)
    print('# papers:', len(df))
    # print(df.head())

    if column == 'keywords':
        words = pd.Series(', '.join(df['keywords'].dropna().apply(partial(transform, stopword=False))).lower().
                          replace(' learn', ' learning').split(',')).str.strip()
    else:
        words = pd.Series(' '.join(df[column].dropna().apply(transform)).split(' ')).str.strip()

    counts = words.value_counts().sort_values(ascending=True)

    counts.iloc[-50:].plot.barh(figsize=(8, 12), fontsize=15)
    plt.title(f'50 MOST APPEARED {column} ({csv_file})', loc='center', fontsize='25',
              fontweight='bold', color='black')
    plt.tight_layout()
    plt.savefig(f'{csv_file}.png', dpi=dpi, bbox_inches='tight')
    plt.show()
