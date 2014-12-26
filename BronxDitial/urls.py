from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BronxDitial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^BXD/$', include('BXD.urls')),
    #url(r'^$', "BXD.views.index"),
    url(r'', include('BXD.urls')),
    url(r'^BXD/', include('BXD.urls')),
    url(r'^calendar/', include('django_bootstrap_calendar.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns(
	'django.views.static',
	(r'^media/(?P<path>.*)',
	'serve',
	{'document_root': settings.MEDIA_ROOT}),
		)
    
if settings.DEBUG:
    urlpatterns += patterns('',
     (r'^static/(?P<path>.*)$', 'django.views.static.serve',         
     {'document_root': settings.STATIC_ROOT}),
        )