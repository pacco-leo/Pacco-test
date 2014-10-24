from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms

from paccotest.models import Question
from paccotest.forms import GPSMeasureForm, QuestionForm
import json

from paccotest.hardware.probesManager import GPSPosition, ProbesManager
from paccotest.hardware.probesManagerDummy import ProbesManagerDummy


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



class ProbesManagerFactory:
    @classmethod
    def make_realProbesManager(Class):
        #return Class.ProbesManagerReal()
        return globals()['ProbesManagerReal']()

    @classmethod
    def make_dummyProbesManager(Class):
        #return Class.ProbesManagerDummy()
        return globals()['ProbesManagerDummy']()


global IS_DEBUGGING
IS_DEBUGGING = True   #Set IS_DEBUGGING for RaspberryPI

if IS_DEBUGGING:
    g_probesMananager = ProbesManagerFactory.make_dummyProbesManager();  #For Dummy Probes
else:
    g_probesMananager = ProbesManagerFactory.make_realProbesManager();  #For Real Probes



# Create your views here.

# Page of test
def test(request):
    return render(request, 'paccotest/test.html')

# The form (hidden) for GPS Position
def gpsPositionForm(request):
    #http://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django
    #http://stackoverflow.com/questions/23285558/datetime-date2014-4-25-is-not-json-serializable-in-django

    initial={'gpsForm': request.session.get('gpsForm', None)}
    form = GPSMeasureForm(request.POST or None, initial=initial)

    if request.method == "POST":

        if form.is_valid():
            form.cleaned_data["utc"] = json.dumps(form.cleaned_data["utc"], cls = DateTimeEncoder)
            request.session['gpsForm'] = form.cleaned_data
            return HttpResponseRedirect(reverse('paccotest:questionnaireForm'))
        else:
            print "GpsForm not valid!"
            print form.errors.as_json()

    return render(request, 'paccotest/gpsPositionForm.html', {'form':form})


# Page of the survey
def questionnaireForm(request):

    initial={'surveyForm': request.session.get('surveyForm', None)}
    #form = forms.Form(request.POST or None, initial=initial)
    form = QuestionForm(request.POST or None, initial=initial)

    #all_questions_list = Question.objects.all()
    if request.method == 'POST':
        pass
        # if form.is_valid():
        #     #request.session['surveyForm'] = form.cleaned_data
        #     #print json.dumps(form.cleaned_data)
        #     return HttpResponseRedirect(reverse('paccotest:probesForm'))
    #context = {'all_questions': all_questions_list}
    return render(request, 'paccotest/questionnaireForm.html', {'form':form})


# Form for probes
def probesForm(request, probeType):

    print probeType
    form = GPSMeasureForm(request.POST or None)

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('paccotest:complete'))

    return render(request, 'paccotest/probesForm.html', {'form':form})

def complete(request):

    _session1 = request.session['gpsForm']
    _session2 = request.session['surveyForm']

    #Save the brol
    #survey = Survey.objects.create(fn=request.session['gpsForm'])
    #

    context = {'SESSION': json.dumps(_session1)}
    return render(request, 'paccotest/complete.html', context)



#Ajax Calls
#URL: http://localhost:8000/paccotest/gpsPosition
def gpsPosition(request):
    gpsPosition = g_probesMananager.getGPSPosition()
    return HttpResponse(json.dumps(vars(gpsPosition)), content_type="application/json")


def probeMeasure(request, probeType):
    probeValue = g_probesMananager.getProbeValue(probeType)
    return HttpResponse(probeValue, content_type="application/json")



#------JSON Encoder for DateTime------------
import datetime
import decimal

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, decimal.Decimal):
           return float(obj)
       elif isinstance(obj, ModelState):
           return None
       else:
           return json.JSONEncoder.default(self, obj)
#------/JSON Encoder for DateTime------------