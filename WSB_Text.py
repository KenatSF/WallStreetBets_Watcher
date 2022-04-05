
import pandas as pd
from emosent import get_emoji_sentiment_rank
import emoji
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()

# EMOJIS
def get_no_emojis(text):
    return emoji.emoji_count(str(text))

def get_full_emojis_sentiment(text):
    emojis_list = emoji.emoji_lis(str(text))
    emojis_nodic = [key['emoji'] for key in emojis_list]
    emojis = list(set(emojis_nodic))

    if not emojis:
        return 'nothing'
    else:
        negative = []
        neutral = []
        positive = []

        for i in emojis:
            try:
                sentiment = get_emoji_sentiment_rank(i)
                negative.append(float(sentiment['negative']))
                neutral.append(float(sentiment['neutral']))
                positive.append(float(sentiment['positive']))
            except:
                continue
        if not negative or not neutral or not positive:
            return 'nothing'
        else:
            negative_mean = sum(negative) / len(negative)
            neutral_mean = sum(neutral) / len(neutral)
            positive_mean = sum(positive) / len(positive)

            sentiment_max = max([negative_mean, neutral_mean, positive_mean])

            if sentiment_max == negative_mean:
                return 'negative'
            elif sentiment_max == neutral_mean:
                return 'neutral'
            elif sentiment_max == positive_mean:
                return 'poisitive'
            else:
                return 'nothing'

# CLEAING TEXT
def delete_emojis(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def cleantext(text):
    if pd.isnull(text):
        return text
    else:
        text = delete_emojis(text)
        text = re.sub(r'@[A-Za-z0-9]+', '', text)
        text = re.sub(r'#', '', text)
        text = re.sub(r'https?:\/\/\S*', '', text)
        text = re.sub(r"[()[\]{}]", "", text)
        text = re.sub(r"\n", "", text)
        text = text.lower()
        return text


def get_links(text):
    return re.findall(r'https?:\/\/\S*', text)

def get_text_sentiment(text):
    if pd.isnull(text):
        return float('NaN')
    else:
        score = TextBlob(text).sentiment.polarity
        if score < -0.05:
            return -1
        elif score > 0.05:
            return 1
        else:
            return 0

def stopwords_percentage(text):
    if pd.isnull(text):
        return float('NaN')
    else:
        if text == "":
            return float('NaN')
        else:
            stopwd = stopwords.words('english')
            content = [w for w in text if w.lower() not in stopwd]
            return len(content) / len(text)

# TOKENIZE
def tokenize_length(text):
    if pd.isnull(text) or text == "":
        return 0
    else:
        tokens = tknzr.tokenize(text)
        return len(tokens)

def characteres_length(text):
    if pd.isnull(text) or text == "":
        return 0
    else:
        return len(text)