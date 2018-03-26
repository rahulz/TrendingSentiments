import json

import pandas
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.dates import timezone_today

from core.models import Trend, Tweet


# Create your views here.

@csrf_exempt
def home(request):
    if request.method == "GET":
        return render(request, 'home.html')
    else:
        trends = Trend.objects.filter(created_at_date=timezone_today())
        res = []
        for trend in trends:
            tweets = Tweet.objects.filter(trend=trend).exclude(polarity=0)
            if tweets.count() < 1:
                continue
            df = pandas.DataFrame(list(tweets.values()))
            positive_sum = df[df['polarity'] > 0].sum(numeric_only=True).polarity / df.count()[0] * 100
            negative_sum = df[df['polarity'] < 0].sum(numeric_only=True).polarity / df.count()[0] * 100
            res.append({
                'name': trend.name,
                'positive': positive_sum,
                'negative': negative_sum,
                'count': int(df.count()[0])
            })
        res = pandas.DataFrame(res)
        res = res.sort_values(by='count')[:50]
        res = res.sort_values(by=['negative'], ascending=True)

        return HttpResponse(res.to_json(orient='table'), content_type='application/json')
