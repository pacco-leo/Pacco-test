from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'paccoProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^paccotest/', include('paccotest.urls', namespace="paccotest")),
    url(r'^admin/', include(admin.site.urls)),
)
