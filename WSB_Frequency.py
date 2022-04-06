
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams
from nltk.probability import FreqDist
tknzr = TweetTokenizer()

# FREQUENCY
def get_n2grams_byrows(text):
    if pd.isnull(text) or text == "":
        return float('NaN')
    else:
        text_tknz = tknzr.tokenize(text)
        ngram = list(ngrams(text_tknz, 2))
        treshold = 2
        filtered_ngram = [bigram for bigram in ngram if len(bigram[0]) > treshold and len(bigram[1]) > treshold]
        return filtered_ngram


def get_words_byrows(text):
    if pd.isnull(text) or text == "":
        return float('NaN')
    else:
        text_tknz = tknzr.tokenize(text)
        treshold = 2
        filtered_words = [word for word in text_tknz if len(word) > treshold]
        return filtered_words


def get_data_freq(index_column, date_value_a, date_value_b, column_freq, data):
    df = data.loc[(data[index_column] >= date_value_a) & (data[index_column] <= date_value_b), [index_column, column_freq]]
    try:
        n_grams = df.apply(lambda x: get_n2grams_byrows(x[column_freq]), axis=1)
        n_grams = n_grams.dropna()
        flat_ngrams = [w for l in n_grams for w in l]

        words = df.apply(lambda x: get_words_byrows(x[column_freq]), axis=1)
        words = words.dropna()
        flat_words = [w for l in words for w in l]

        fdist_n = FreqDist(flat_ngrams)
        fdist_w = FreqDist(flat_words)
        # Tabla (pandas) de frecuencias para crear el PMI
        df_g = pd.DataFrame()
        df_g['bi_gram'] = list(fdist_n)
        df_g['word_0'] = df_g['bi_gram'].apply(lambda x: x[0])
        df_g['word_1'] = df_g['bi_gram'].apply(lambda x: x[1])
        df_g['bi_gram_freq'] = df_g['bi_gram'].apply(lambda x: fdist_n[x])
        df_g['word_0_freq'] = df_g['word_0'].apply(lambda x: fdist_w[x])
        df_g['word_1_freq'] = df_g['word_1'].apply(lambda x: fdist_w[x])
        df_g['PMI'] = df_g[['bi_gram_freq', 'word_0_freq', 'word_1_freq']].apply(
            lambda x: np.log2(x.values[0] / (x.values[1] * x.values[2])), axis=1)
        df_g['log(bi_gram_freq)'] = df_g['bi_gram_freq'].apply(lambda x: np.log2(x))
        df_g = df_g.sort_values(by='PMI', ascending=False)
        return df_g
    except:
        return 0