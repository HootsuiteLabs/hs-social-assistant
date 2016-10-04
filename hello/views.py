import json
import requests

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def get_articles(request):

    topics = request.GET.get('topics','Marketing,Social_Media')
    url = "https://aras.hootsuite.com/articles"
    querystring = {"q": topics}
    response = {}

    try:
        aras_response = requests.request("GET", url, params=querystring)
        response['result'] = aras_response.json()
        response['message'] = ''
        return HttpResponse(json.dumps(response), content_type="application/json");
    except:
        response['result'] = {}
        response['message'] = 'Content Source Error.'
        return HttpResponse(json.dumps(response), content_type="application/json");
