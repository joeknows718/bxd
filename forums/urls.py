from django.conf.urls import patterns, url
from forums import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^forum/(\d+)/$', views.forum, name='forum'),
	url(r'^thread/(\d+)/$', views.thread, name='thread'),
	url(r'^post/(new_thread|reply)/(\d+)/$', views.post, name='post'),
	url(r'^rely/(\d+)/$', views.reply, name='reply'),
	url(r'^new_thread/(\d+)/$', views.new_thread, name='new_thread'),
	url(r'^profile/(\d+)/$', views.profile, name='profile'),
	)
