import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
from bertopic import BERTopic



def run_topic_modeling(comments):
    df=pd.DataFrame(comments)

    def clean_text(text):
        nltk.download("stopwords")
        stop_words = set(stopwords.words("english"))

        text = text.lower()
        text = re.sub(r"http\S+", "", text)  # remove links
        text = re.sub(r"[^a-z\s]", "", text)  # remove symbols
        words = text.split()
        words = [w for w in words if w not in stop_words] # remove stop words
        
        return " ".join(words)
    


    cleaned_texts = [clean_text(t) for t in df["text"].dropna().tolist()]

    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(cleaned_texts)

    return topic_model.get_topic_info()
