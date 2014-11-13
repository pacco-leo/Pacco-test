from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms

from paccotest.models import Question, Probe
from paccotest.forms import GPSMeasureForm,ProbeMeasureForm
import json

from paccotest.hardware.probesManager import GPSPosition, ProbesManager
from paccotest.hardware.probesManagerDummy import ProbesManagerDummy
#from paccotest.hardware.probesManagerReal import ProbesManagerReal

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
IS_DEBUGGING = True  #Set IS_DEBUGGING for RaspberryPI

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
    form = forms.Form(request.POST or None, initial=initial)
    #form = QuestionForm(request.POST or None, initial=initial)

    if request.method == 'POST':
        print "hggdfdfgop"
        if form.is_valid():
            print form.cleaned_data  #FIX: void
        #     #request.session['surveyForm'] = form.cleaned_data
        #     #print json.dumps(form.cleaned_data)
        firstProbeName = Probe.objects.all().order_by('order')[0].name
        return HttpResponseRedirect(reverse('paccotest:probesForm', args=(firstProbeName,)))

    all_questions_list = Question.objects.all()
    lastTab = all_questions_list.count() + 1
    context = {'all_questions': all_questions_list,'lastTab':lastTab}
    return render(request, 'paccotest/questionnaireForm.html', context)


# Form for probes
def probesForm(request, probeName):

    #TODO: Test if probeName exists!
    probeTypeID = Probe.objects.get(name=probeName).id

    initial={'probesValues': request.session.get('probesValues', None), 'probeType': probeTypeID}
    form = ProbeMeasureForm(request.POST or None, initial=initial)

    if request.method == 'POST':

        if form.is_valid():

            if 'probesValues' not in request.session:
                request.session['probesValues']={}

            request.session['probesValues'][form.cleaned_data['probeType'].id] = form.cleaned_data['measure']


            #Get the list of probes
            currentOrder = Probe.objects.get(name=probeName).order
            nextProbes = Probe.objects.all().order_by('order').filter(order__gt=currentOrder)

            #Go to the next probe
            if nextProbes:
                nextProbeName = nextProbes[0].name
                return HttpResponseRedirect(reverse('paccotest:probesForm', args=(nextProbeName,)))
            #This is the last probe
            else:
                return HttpResponseRedirect(reverse('paccotest:complete'))

        else:
            print "ProbeForm not valid!"
            print form.errors.as_json()

    return render(request, 'paccotest/probesForm.html', {'probeName':probeName, 'form':form})

def complete(request):

    _session1 = request.session['gpsForm']
    _session2 = request.session['probesValues']

    print(request.session.keys())   #Print all the keys
    #_session2 = request.session['surveyForm']

    #Save the brol
    #survey = Survey.objects.create(fn=request.session['gpsForm'])
    #

    context = {'SESSION': json.dumps(_session1)+ " ---- " +json.dumps(_session2)}
    return render(request, 'paccotest/complete.html', context)



#Ajax Calls
#URL: http://localhost:8000/paccotest/gpsPosition
def gpsPosition(request):
    gpsPosition = g_probesMananager.getGPSPosition()
    return HttpResponse(json.dumps(vars(gpsPosition)), content_type="application/json")


def probeMeasure(request, probeName):
    probeValue = g_probesMananager.getProbeValue(probeName)
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
