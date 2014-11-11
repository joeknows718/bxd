from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='/about'),
	url(r'resources/', views.resources, name ='/resources'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	url(r'^add_project/$', views.add_project, name='add_project'), 
	url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
	url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
	url(r'^project_info/(?P<project_name_url>\w+)/$', views.project_info, name='project'),
	url(r'^projects/', views.projects, name='/projects'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^restricted/', views.restricted, name='/restricted'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'events/$', views.event_page, name='events'),
	url(r'test/$', views.fuck_bootstrap, name='test'),
	) 
