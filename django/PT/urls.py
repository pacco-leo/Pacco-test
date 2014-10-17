from django.conf.urls import patterns, include, url
from django.contrib import admin
import os.path

site_media = os.path.join(
	os.path.dirname(__file__), 'site_media'
)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^paccotest/ouverture/$', 'paccotest.views.ouverture'),
    url(r'^paccotest/intro/(?P<nid>[0-9]+)/(?P<lg>[a-z]+)$', 'paccotest.views.intro'),
    url(r'^paccotest/question/(?P<nid>[0-9]+)/(?P<lg>[a-z]+)/(?P<num>[0-9]+)$', 'paccotest.views.question'),
    url(r'^paccotest/sonde/(?P<nid>[0-9]+)/(?P<lg>[a-z]+)/(?P<num>[0-9]+)$', 'paccotest.views.sonde'),  
    url(r'^paccotest/position/(?P<nid>[0-9]+)/(?P<lg>[a-z]+)$', 'paccotest.views.position',name='position'),
    url(r'^paccotest/outro/(?P<nid>[0-9]+)/(?P<lg>[a-z]+)$', 'paccotest.views.outro'),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':site_media}),
    url(r'^paccotest/updateremote/$', 'paccotest.views.updateremote'),
    #url(r'^paccotest/', 'paccotest.views.ouverture'),  
)


