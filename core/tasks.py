from __future__ import absolute_import, unicode_literals

import threading

import celery
from django.apps import apps
from django.utils import timezone

from TrendingSentiments import settings
from utils.ai.nlp import isascii
from utils.ai.sentiment import analyse_sentiment, clean_tweet
from utils.db.helpers import cleanup_fields
from utils.tweepy.helpers import TweePy

app = celery.Celery('GitLabExt')


@app.task()
def get_trends():
    Trend = apps.get_model('core.Trend')
    api = TweePy()
    trends = api.get_trends()[0]['trends']
    trends = filter(lambda x: isascii(x['name']), trends)
    for trend in trends:
        trend = cleanup_fields(trend, Trend)
        obj, created = Trend.objects.update_or_create(name=trend['name'], defaults=trend)
        print(created)
    return f"{len(list(trends))} added on {timezone.datetime.today().strftime(settings.DATE_FORMAT)}"


class CrawlThread(threading.Thread):
    def __init__(self, name, counter, trend):
        threading.Thread.__init__(self)
        self.name = name
        self.trend = trend
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        __crawl__(self.trend)
        print("Exiting " + self.name)


def __crawl__(trend):
    Tweet = apps.get_model('core.Tweet')
    api = TweePy()
    c = 0
    print(trend.name)
    if trend.latest_id and trend.earliest_id:
        since_id = trend.latest_id
        max_id = trend.earliest_id
    else:
        since_id = None
        max_id = None

    tweets_since = api.search(q=trend.query, since_id=since_id)
    tweets_max = api.search(q=trend.query, max_id=max_id)
    if tweets_since:
        trend.latest_id = tweets_since[0].id
    if tweets_max:
        trend.earliest_id = tweets_max[-1].id
    trend.save()

    tweets = tweets_max + tweets_since
    print(f'{since_id} - {max_id} - {len(tweets)}')
    re_since = 0
    un_usable_since = 0
    re_max = 0
    un_usable_max = 0
    cc = 0
    for tweet in tweets_since:
        cc = 0
        text = tweet.text
        cleaned = clean_tweet(text)
        if len(cleaned) < 5:
            un_usable_since += 1
            continue
        id = tweet.id_str
        polarity, subjectivity = analyse_sentiment(text)

        if not Tweet.objects.filter(id=id).exists():
            c = c + 1
            cc = cc + 1
            Tweet.objects.create(trend=trend, cleaned_text=cleaned, id=id, text=text, polarity=polarity,
                                 subjectivity=subjectivity)
        else:
            re_since += 1
    for tweet in tweets_max:
        text = tweet.text
        cleaned = clean_tweet(text)
        if len(cleaned) < 5:
            un_usable_max += 1
            continue
        id = tweet.id_str
        polarity, subjectivity = analyse_sentiment(text)

        if not Tweet.objects.filter(id=id).exists():
            c = c + 1
            cc = cc + 1
            Tweet.objects.create(trend=trend, cleaned_text=cleaned, id=id, text=text, polarity=polarity,
                                 subjectivity=subjectivity)
        else:
            re_max += 1

    print(
        f'MAX: {re_max}:{un_usable_max} |SINCE: {re_since}:{un_usable_since} '
        f'| added: {cc}/{len(tweets)}')


@app.task()
def crawl():
    print('in')
    Trend = apps.get_model('core.Trend')
    Tweet = apps.get_model('core.Tweet')
    trends = Trend.objects.filter(created_at_date=timezone.datetime.today())
    counter = 1
    th = []
    for trend in trends:
        th.append(CrawlThread(trend.name, counter, trend))
    for t in th:
        t.start()
    for t in th:
        t.join()
    return
    api = TweePy()
    c = 0
    for trend in trends:
        print(trend.name)
        if trend.latest_id and trend.earliest_id:
            since_id = trend.latest_id
            max_id = trend.earliest_id
        else:
            since_id = None
            max_id = None

        tweets_since = api.search(q=trend.query, since_id=since_id)
        tweets_max = api.search(q=trend.query, max_id=max_id)
        if tweets_since:
            trend.latest_id = tweets_since[0].id
        if tweets_max:
            trend.earliest_id = tweets_max[-1].id
        trend.save()

        tweets = tweets_max + tweets_since
        print(f'{since_id} - {max_id} - {len(tweets)}')
        re_since = 0
        un_usable_since = 0
        re_max = 0
        un_usable_max = 0
        cc = 0
        for tweet in tweets_since:
            cc = 0
            text = tweet.text
            cleaned = clean_tweet(text)
            if len(cleaned) < 5:
                un_usable_since += 1
                continue
            id = tweet.id_str
            polarity, subjectivity = analyse_sentiment(text)

            if not Tweet.objects.filter(id=id).exists():
                c = c + 1
                cc = cc + 1
                Tweet.objects.create(trend=trend, cleaned_text=cleaned, id=id, text=text, polarity=polarity,
                                     subjectivity=subjectivity)
            else:
                re_since += 1
        for tweet in tweets_max:
            text = tweet.text
            cleaned = clean_tweet(text)
            if len(cleaned) < 5:
                un_usable_max += 1
                continue
            id = tweet.id_str
            polarity, subjectivity = analyse_sentiment(text)

            if not Tweet.objects.filter(id=id).exists():
                c = c + 1
                cc = cc + 1
                Tweet.objects.create(trend=trend, cleaned_text=cleaned, id=id, text=text, polarity=polarity,
                                     subjectivity=subjectivity)
            else:
                re_max += 1

        print(
            f'MAX: {re_max}:{un_usable_max} |SINCE: {re_since}:{un_usable_since} '
            f'| added: {cc}/{len(tweets)}')
        cc = 0
    print(c)
    crawl()
    # return f'{c} tweets added'
