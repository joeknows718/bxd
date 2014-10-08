from django.conf.urls import patterns, url, include 

from polls import views 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^specifics/(?P<poll_id>\d+)$', views.detail, name='detail'), 
	url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
	url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
	)
