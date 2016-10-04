import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

# Main view
def index(request):
    return render(request, 'index.html')

def get_topics_for_tweet(text):
    url = "https://gateway-a.watsonplatform.net/calls/text/TextGetRankedTaxonomy"
    querystring = {
        "apikey":"3f2b08f9bf2c5f59a2d7b2d61dd95890a80fb2b6",
        "text":text,
        "outputMode":"json"}
    text_analysis = requests.request("GET", url, params=querystring)
    topics = text_analysis.json()['taxonomy'][0].get('label', '/')[1:].split("/")
    return topics

# Content discovery API endpoint
def get_articles(request):
    topics = request.GET.get('topics','Marketing,Social_Media')
    url = "https://aras.hootsuite.com/articles"
    querystring = {"q": topics}
    response = {}

    try:
        aras_response = requests.request("GET", url, params=querystring)
        response['result'] = aras_response.json()
        articles = response['result']['articles']
        response['result']['articles'] = [article for article in articles if article['image', None] is not None]
        response['message'] = ''
        return HttpResponse(json.dumps(response),
                            content_type="application/json");
    except Exception, e:
        print e
        response['result'] = {}
        response['message'] = 'Content Source Error.'
        return HttpResponse(json.dumps(response),
                            content_type="application/json");

# AI API endpoint
def get_topics(request):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    querystring = {"screen_name":"mozhacks"}
    headers = {
        'authorization': "Bearer AAAAAAAAAAAAAAAAAAAAALYVxQAAAAAArsFh33H%2BFhZWl27Tn0vmsgxXBDs%3DzMUgdB9LjfL2JyefZn2GiWkGjmhirPyvkciA4mrX6MjP8eKaPz",
        'cache-control': "no-cache"        }
    twitter_response = requests.request("GET", url,
                                        headers=headers, params=querystring)

    # extract the last 10 tweets
    messages = list()
    i = 1
    for tweet in twitter_response.json():
        if (i > 3):
            break
        messages.append(tweet.get('text', ''))
        i = i +1
    print messages
    topics = list()
    for message in messages:
        topics.extend(get_topics_for_tweet(message))
    topic = max(set(topics), key=topics.count)

    response = {}
    response['result'] = {'topics': topic}
    response['message'] = ''
    return HttpResponse(json.dumps(response),
                        content_type="application/json");