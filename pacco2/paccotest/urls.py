from django.conf.urls import patterns, url

from paccotest import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^surveyComplete/$', views.surveyComplete, name='surveyComplete'),
    url(r'^test/$', views.test, name='test')
)