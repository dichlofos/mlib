from django.conf.urls import patterns, url

from face import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^download/(?P<book_id>\d+)/$', views.download, name='download'),
)
