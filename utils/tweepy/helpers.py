import pdb

import tweepy


class TweePy:
    def __init__(self):
        auth = tweepy.OAuthHandler("ABqdGcPLLERJHc8SuAvWjj15g", "4k6rMnryRLMBKjP9cHZcstViCHpvlgcyBP7WHsNBXHfJotgDXA")
        auth.set_access_token("569727959-Uo7W00UqRmnFidEpYr62RTsQvSzinRjNFNryxTPz",
                              "k5X6s4A6RzB005HCY9r9bFqR2OXcwlg0euaao2HDn113H")
        self.api = tweepy.API(auth)

    def get_trends(self):
        return self.api.trends_place(23424848)

    def search(self, q, since_id=None, max_id=None):
        return self.api.search(lang='en', q=q, count=100, result_type='recent', since_id=since_id, max_id=max_id)


if __name__ == '__main__':
    t = TweePy()
    trends = t.get_trends()
    pdb.set_trace()
