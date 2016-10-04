from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^articles/', hello.views.get_articles, name='articles'),
    url(r'^topics/', hello.views.get_topics, name='topics'),
    url(r'^$', hello.views.index, name='index')
]
