from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from paccotest.models import Question
from paccotest.forms import GPSMeasureForm
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
    #http://pydanny.com/core-concepts-django-modelforms.html
    #http://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django
    #http://burnbit.com/torrent/316217/pycharm_professional_3_4_1_dmg
    #https://docs.djangoproject.com/en/dev/topics/forms/

    initial={'fn': request.session.get('fn', None)}
    form = GPSMeasureForm(request.POST or None, initial=initial)

    if request.method == "POST":

        form = GPSMeasureForm(request.POST, initial=initial)

        if form.is_valid():
            form.save()
            #print form.cleaned_data()
           #https://docs.djangoproject.com/en/1.3/ref/forms/api/

            #request.session['fn'] = form.cleaned_data['fn']
            #request.session['fn'] = form.cleaned_data()
            #request.session['fn'] = form #.data['fn']
            return HttpResponseRedirect(reverse('paccotest:survey'))
        else:
            #http://stackoverflow.com/questions/18528932/django-form-with-no-errors-return-false-for-is-valid
            print form.is_valid()   #form contains data and errors
            print "hello"
            print form.errors.as_json()

    return render(request, 'paccotest/gpsPositionForm.html', {'form':form})

# Page of the survey
def survey(request):
    all_questions_list = Question.objects.all()
    if request.method == 'POST':
    #    if form.is_valid():
    #        #SAVE THE THINGS HERE
            return HttpResponseRedirect(reverse('paccotest:probesForm'))
    context = {'all_questions': all_questions_list}
    return render(request, 'paccotest/survey.html', context)

# Form for probes
def probesForm(request):

    form = GPSMeasureForm(request.POST or None)

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('paccotest:complete'))

    return render(request, 'paccotest/probesForm.html', {'form':form})

def complete(request):

    _session = request.session['fn']
    context = {'SESSION': _session}
    return render(request, 'paccotest/complete.html', context)



#Ajax Calls
#URL: http://localhost:8000/paccotest/gpsPosition
def gpsPosition(request):
    gpsPosition = g_probesMananager.getGPSPosition()
    return HttpResponse(json.dumps(vars(gpsPosition)), content_type="application/json")
