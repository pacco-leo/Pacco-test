from django.conf.urls import patterns, url

from paccotest import views


urlpatterns = patterns('',
    # ex: /polls/
    url(r'^gpsPositionForm/$', views.gpsPositionForm, name='gpsPositionForm'),
    url(r'^questionnaireForm/$', views.questionnaireForm, name='questionnaireForm'),
    url(r'^probesForm/(?P<probeType>[a-z]+)/$', views.probesForm, name='probesForm'),
    url(r'^test/$', views.test, name='test'),
    url(r'^complete/$', views.complete, name='complete'),

    #Ajax
    url(r'^gpsPositionForm/gpsPosition/$', views.gpsPosition, name='gpsPosition'),
    url(r'^probeMeasure/(?P<probeType>[a-z]+)/$', views.probeMeasure, name='probeMeasure'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
)