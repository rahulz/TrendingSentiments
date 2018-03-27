import pdb
from enum import Enum

import tweepy

from TrendingSentiments import settings


class Places(Enum):
    INDIA = 23424848
    WORLDWIDE = 1


class TweePy:
    def __init__(self):
        auth = tweepy.OAuthHandler(settings.TW_CONSUMER_KEY, settings.TW_CONSUMER_SECRET)
        auth.set_access_token(settings.TW_APP_KEY,
                              settings.TW_APP_SECRET)
        self.api = tweepy.API(auth)

    def get_trends(self):
        return self.api.trends_place(Places.INDIA)

    def search(self, q, since_id=None, max_id=None):
        return self.api.search(lang='en', q=q, count=100, result_type='recent', since_id=since_id, max_id=max_id)


if __name__ == '__main__':
    t = TweePy()
    trends = t.get_trends()
    pdb.set_trace()
