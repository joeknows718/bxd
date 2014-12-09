from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BronxDitial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^BXD/', include('BXD.urls')),
    url(r'^calendar/', include('calendarium.urls')),
    url(r'^calendar/', include('calendarium.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns(
	'djano.views.static',
	(r'^media/(?P<path>.*)',
	'serve',
	{'document_root': settings.MEDIA_ROOT}),
		)