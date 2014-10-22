from django.conf.urls import patterns, url

from paccotest import views

from paccotest.forms import ContactForm1, ContactForm2
from paccotest.views import ContactWizard

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^surveyComplete/$', views.surveyComplete, name='surveyComplete'),
    url(r'^test/$', views.test, name='test'),
    url(r'^contact/$', ContactWizard.as_view([ContactForm1, ContactForm2])),

)