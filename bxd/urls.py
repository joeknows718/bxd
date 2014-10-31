from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bxd.views.home', name='home'),
    # url(r'^bxd/', include('bxd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('calendarium.urls')),
    url(r'^forums/', include('forums.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    ) #url for BXD tuple added
if settings.DEBUG: #if the debug is set to true, then an addiiton url is added to the patterns tuple
	urlpatterns += patterns(
		'django.views.static',
		(r'media/(?P<path>.*)',#any url starting with media will be appended to the django.views.static file. EI uploading a profile pic  
		'serve',
		{'document_root': settings.MEDIA_ROOT}),
		)
