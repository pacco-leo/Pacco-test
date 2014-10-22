from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from paccotest.models import Question
from paccotest.forms import GPSMeasureForm

# from django.contrib.formtools.wizard.views import SessionWizardView

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
       # if form.is_valid():
       if 1 == 1:
           #https://docs.djangoproject.com/en/1.3/ref/forms/api/
            #request.session['fn'] = form.cleaned_data['fn']
            request.session['fn'] = "hello123" #.data['fn']
            return HttpResponseRedirect(reverse('paccotest:survey'))
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
