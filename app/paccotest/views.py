from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import activate as translationactivate
from django.utils.translation import get_language as translationget_language
from django.utils.translation import LANGUAGE_SESSION_KEY

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


# The Opening Page
def opening(request):
    return render(request, 'paccotest/opening.html')

# The Intro Page
def intro(request,lg):
    request.session.clear()
    translationactivate(lg)
    request.session[LANGUAGE_SESSION_KEY] = lg
    return render(request, 'paccotest/intro.html')

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

    initial={'questionnaireValues': request.session.get('questionnaireValues', None)}
    form = forms.Form(request.POST or None, initial=initial)
    #form = QuestionForm(request.POST or None, initial=initial)

    if request.method == 'POST':

        if form.is_valid():  #Useless!
            if 'questionnaireValues' not in request.session:
                 request.session['questionnaireValues']={}

            #Get values of the form
            #Key: QuestionID,   Value: AnswerID
            for i in request.POST:
                if i !=  "csrfmiddlewaretoken":    #TODO: Make it cleaner
                    #print 'I have been passed the following keys: ',i, ' and value:',request.POST[i]
                    request.session['questionnaireValues'][i] = request.POST[i]

            #print request.session['questionnaireValues']  #DEBUG
            return HttpResponseRedirect(reverse('paccotest:probesForm'))

    all_questions_list = Question.objects.all().order_by('order')
    lastTab = all_questions_list.count() + 1
    context = {'all_questions': all_questions_list,'lastTab':lastTab}
    return render(request, 'paccotest/questionnaireForm.html', context)


# Form for probes
def probesForm(request):
    all_probes_list = Probe.objects.all().order_by('order')
    lastTab = all_probes_list.count() + 1

    initial = {'probesValues': request.session.get('probesValues', None), 'all_probes': all_probes_list}
    form = forms.Form(request.POST or None, initial=initial)

    if request.method == 'POST':

        if form.is_valid():   #Useless!

            if 'probesValues' not in request.session:
                request.session['probesValues'] = {}

            # Get values of the form
            #Key: ProbeID,   Value: ProbeValue
            for i in request.POST:
                if i != "csrfmiddlewaretoken":  #TODO: Make it cleaner
                    #print 'I have been passed the following keys: ',i, ' and value:',request.POST[i]
                    request.session['probesValues'][i] = request.POST[i]

            print request.session['probesValues']  #DEBUG

            # if 'probesValues' not in request.session:
            #     request.session['probesValues'] = {}
            #
            #     for probe in all_probes_list:
            #         request.session['probesValues'][probe.id] = form.cleaned_data['probe' + str(probe.id)]
            #
            #     print request.session['probesValues']  #DEBUG

            return HttpResponseRedirect(reverse('paccotest:complete'))

    return render(request, 'paccotest/probesForm.html',
                  {'all_probes': all_probes_list, 'lastTab': lastTab, 'form': form})


from models import *  #TEMP

def complete(request):

    gpsValues = request.session['gpsForm']
    questionnaireValues = request.session['questionnaireValues']
    probesValues = request.session['probesValues']

    utc_formated = gpsValues["utc"][1:11]+' '+gpsValues["utc"][12:20]

    #Save GPS Values
    survey = Survey.objects.create(latitude = gpsValues["latitude"],
                                    longitude = gpsValues["longitude"],
                                    elevation = gpsValues["elevation"],
                                    utc = utc_formated
                                    )
    #Save Questionnaire
    for key in questionnaireValues:
        UserAnswer.objects.create(  survey = survey,
                                    answer=Answer.objects.get(id=questionnaireValues[key]),
                                    question=Question.objects.get(id=key))

    #Save Probes values
    for key in probesValues:
        ProbeMeasure.objects.create(  survey = survey,
                                    probeType=Probe.objects.get(id=key),
                                    measure=probesValues[key])


    #print(request.session.keys())   #DEBUG: Print all the keys

    context = {'SESSION': json.dumps(gpsValues)+ " ---- " +json.dumps(questionnaireValues)+ " ---- " + json.dumps(probesValues)}
    return render(request, 'paccotest/complete.html', context)



#--------------------- CRON ----------------------------------
#Called by Cron, to send all new surveys to remote Server
def uploadToServer(request):
    newSurveys = Survey.objects.filter(uploadedToServer=False)

    # Send to remote Queue
    import pika

    #The RabbitMQ host
    RABBITMQ_HOST = '192.168.1.5'   #TODO: Add this to settings somewhere


    credentials = pika.PlainCredentials('matt', 'matt')

    # parameters = pika.ConnectionParameters(host='localhost')

    parameters = pika.ConnectionParameters(RABBITMQ_HOST,
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='paccotest')


    for survey in newSurveys:
        channel.basic_publish(exchange='',
                              routing_key='paccotest',
                              body=getJsonFromSurvey(survey.id))
        #survey.uploadedToServer = True
        #survey.save() #Debug: commented for debugging

    connection.close()

    uploadedCount = newSurveys.count()
    return HttpResponse("UploadedToServer: " + str(uploadedCount))
#--------------------- /CRON ----------------------------------

#Return a JSON from all user data for survey "surveyID"
def getJsonFromSurvey(surveyID):

    from django.core import serializers
    data = serializers.serialize("json", [Survey.objects.get(id=surveyID)])
    data2 =   serializers.serialize("json", UserAnswer.objects.filter(survey=surveyID), fields=('question','answer'))
    data3 =   serializers.serialize("json", ProbeMeasure.objects.filter(survey=surveyID), fields=('probeType','measure'))

    return data + data2 + data3




#Ajax Calls
#URL: http://localhost:8000/paccotest/gpsPosition
def gpsPosition(request):
    gpsPosition = g_probesMananager.getGPSPosition()
    return HttpResponse(json.dumps(vars(gpsPosition)), content_type="application/json")


def probeMeasure(request, probeChannel):
    probeValue = g_probesMananager.getProbeValue(probeChannel)
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


#------UPDATE DB------------
def update(request):

    #OPTION1
    #from django.db import connection
    #cursor = connection.cursor()
    #cursor.execute("INSERT INTO `paccotest_question` (`id`, `text`, `text_fr`, `text_nl`, `text_en`, `order`) VALUES (8, 'Question1', 'LM''eau est-elle pporonfde?', 'LM''eau est-elle pporonfde?', 'LM''eau est-elle pporonfde?', 1), (9, 'Question1', 'LM''eau est-elle pporonfde?', 'LM''eau est-elle pporonfde?', 'LM''eau est-elle pporonfde?', 1)")

    #OPTION2
    Question.objects.all().delete()
    Answer.objects.all().delete()
    Probe.objects.all().delete()
    #data='[{"model":"paccotest.question","fields":{"id":"1","text":"Question1","text_fr":"LM\'eau est-elle pporonfde?","text_nl":"LM\'eau est-elle pporonfde?","text_en":"LM\'eau est-elle pporonfde?","order":"0","answers":[1,2]}},{"model":"paccotest.question","fields":{"id":"2","text":"Questoin2","text_fr":"couleur?","text_nl":"couleur?","text_en":"couleur?","order":"2","answers":[1,2]}},{"model":"paccotest.answer","fields":{"id":"1","text":"0","text_fr":"oui","text_nl":"","text_en":"","order":"0"}},{"model":"paccotest.answer","fields":{"id":"2","text":"0","text_fr":"non","text_nl":"","text_en":"","order":"0"}},{"model":"paccotest.probe","fields":{"id":"1","name":"pH","text_fr":"pH","text_nl":"pH","text_en":"pH","channel":"4","order":"0"}},{"model":"paccotest.probe","fields":{"id":"2","name":"ORP (redox)","text_fr":"Potentiel d\'oxydor\u00e9duction","text_nl":"Redoxpotentiaal","text_en":"Reduction potential","channel":"5","order":"2"}},{"model":"paccotest.probe","fields":{"id":"3","name":"conductivityyy","text_fr":"Conductivit\u00e9","text_nl":"Geleidbaarheid","text_en":"Conductivity","channel":"7","order":"2"}},{"model":"paccotest.probe","fields":{"id":"4","name":"do","text_fr":"Oxyg\u00e8ne Dissous","text_nl":"Opgeloste Zuurstof","text_en":"Dissolved oxygen","channel":"6","order":"3"}},{"model":"paccotest.probe","fields":{"id":"5","name":"temperature","text_fr":"Temperature","text_nl":"Temperatuur","text_en":"Temperatur","channel":"15","order":"4"}}]'
    with open('updateDB.json') as f:
        data = f.read()
    from django.core import serializers
    for deserialized_object in serializers.deserialize("json", str(data)):
        deserialized_object.save()

    return  HttpResponse("DB updated!")