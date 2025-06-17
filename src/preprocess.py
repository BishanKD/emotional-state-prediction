import pandas as pd
import re
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in STOPWORDS]
    return " ".join(tokens)

def preprocess_dataframe(df):
    df["full_text"] = df["title"].fillna("") + " " + df["selftext"].fillna("")
    df["clean_text"] = df["full_text"].apply(clean_text)
    df = df[df["clean_text"].str.len() > 10]
    return df[["clean_text", "emotion_score"]]