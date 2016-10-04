import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

# Main view
def index(request):
    return render(request, 'index.html')

# Content discovery API endpoint
def get_articles(request):
    topics = request.GET.get('topics','Marketing,Social_Media')
    url = "https://aras.hootsuite.com/articles"
    querystring = {"q": topics}
    response = {}

    try:
        aras_response = requests.request("GET", url, params=querystring)
        response['result'] = aras_response.json()
        response['message'] = ''
        return HttpResponse(json.dumps(response),
                            content_type="application/json");
    except:
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
        'cache-control': "no-cache",
        'postman-token': "eaca0070-cdd4-7f61-82b1-2f4837b35680"
        }
    twitter_response = requests.request("GET", url,
                                        headers=headers, params=querystring)

    # extract the last 10 tweets
    messages = list()
    i = 1
    for tweet in twitter_response.json():
        if (i > 10):
            break
        messages.append(tweet.get('text', ''))
        i = i +1
    print messages

    response = {}
    response['result'] = {'topics': 'software'}
    response['message'] = ''
    return HttpResponse(json.dumps(response),
                        content_type="application/json");