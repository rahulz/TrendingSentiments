import re

from textblob import TextBlob


def clean_tweet(text):
    """
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def analyse_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment
