from __future__ import absolute_import, unicode_literals

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


@app.task()
def crawl():
    print('in')
    Trend = apps.get_model('core.Trend')
    Tweet = apps.get_model('core.Tweet')
    trends = Trend.objects.filter(created_at_date=timezone.datetime.today())
    api = TweePy()
    c = 0
    for trend in trends:
        print(trend.name)
        try:
            since_id = Tweet.objects.filter(trend=trend).latest(field_name='created_at').id
            max_id = Tweet.objects.filter(trend=trend).earliest(field_name='created_at').id
        except Tweet.DoesNotExist:
            since_id = None
            max_id = None
        tweets_since = api.search(q=trend.query, since_id=since_id)
        tweets_max = api.search(q=trend.query, max_id=max_id)
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
