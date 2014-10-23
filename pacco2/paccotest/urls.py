from django.conf.urls import patterns, url

from paccotest import views


urlpatterns = patterns('',
    # ex: /polls/
    url(r'^gpsPositionForm/$', views.gpsPositionForm, name='gpsPositionForm'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^probesForm/$', views.probesForm, name='probesForm'),
    url(r'^test/$', views.test, name='test'),
    url(r'^complete/$', views.complete, name='complete'),
    url(r'^gpsPositionForm/gpsPosition/$', views.gpsPosition, name='gpsPosition'),
)