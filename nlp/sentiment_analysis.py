import re
import html
import pandas as pd
from transformers import pipeline


def run_sentiment_analysis(comments):
    df=pd.DataFrame(comments)

    def preprocess_comment(text: str) -> str:
      if not isinstance(text, str):
            return ""

        # 1. Decode HTML entities (e.g., &amp;)
      text = html.unescape(text)

        # 2. Remove HTML tags (e.g., <a href=...>...</a>)
      text = re.sub(r"<.*?>", " ", text)

        # 3. Remove URLs
      text = re.sub(r"http\S+|www\S+", " ", text)

        # 4. Remove extra whitespace
      text = re.sub(r"\s+", " ", text).strip()

        # 5. Remove timestamps
      text = re.sub(r"\b\d{1,2}:\d{2}\b", " ", text)

      return text
    
    df["text"] = df["text"].apply(preprocess_comment)

    sentiment_pipeline = pipeline("sentiment-analysis",model="cardiffnlp/twitter-roberta-base-sentiment-latest",truncation=True,max_length=512)

    sentiment_res= sentiment_pipeline(df["text"].tolist())

    df[["label","score"]]=pd.DataFrame(sentiment_res)

    positive_df = df[df["label"] == "positive"]
    negative_df = df[df["label"] == "negative"]

    print(f"Total comments: {len(df)}, Positive: {len(positive_df)}, Negative: {len(negative_df)}, Neutral:{len(df)-len(positive_df)-len(negative_df)}")

    return df









