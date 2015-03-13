from django.conf.urls import patterns, url

from paccotest import views


urlpatterns = patterns('',
    # ex: /polls/
    url(r'^opening/$', views.opening, name='opening'),
    url(r'^intro/(?P<lg>[a-z]+)$', views.intro, name='intro'),
    url(r'^gpsPositionForm/$', views.gpsPositionForm, name='gpsPositionForm'),
    url(r'^questionnaireForm/$', views.questionnaireForm, name='questionnaireForm'),
    url(r'^probesForm/$', views.probesForm, name='probesForm'),
    url(r'^complete/$', views.complete, name='complete'),
    url(r'^uploadToServer/$', views.uploadToServer, name='uploadToServer'),

    #Ajax
    url(r'^gpsPositionForm/gpsPosition/$', views.gpsPosition, name='gpsPosition'),
    #url(r'^probesForm/(?P<probeName>[a-zA-Z]+)/probeMeasure/$', views.probeMeasure, name='probeMeasure'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
    url(r'^probesForm/(?P<probeChannel>[0-9]+)/probeMeasure/$', views.probeMeasure, name='probeMeasure'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
    url(r'^update/$', views.update, name='update'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
    url(r'^uploadToServer/uploadToServerClick/$', views.uploadToServerClick, name='uploadToServerClick'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
    url(r'^uploadToServer/doShutdown/$', views.doShutdown, name='doShutdown'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
    url(r'^complete/doShutdown/$', views.doShutdown, name='doShutdown'),  #Ex: http://127.0.0.1:8000/paccotest/probeMeasure/ph/
)