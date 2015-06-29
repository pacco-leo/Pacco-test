from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import activate as translationactivate
from django.utils.translation import get_language as translationget_language
from django.utils.translation import LANGUAGE_SESSION_KEY

from paccotest.models import Question, Probe, CalibrationMemo, WaterCategoriesValue
from paccotest.forms import GPSMeasureForm,ProbeMeasureForm
import json
import unicodedata

from paccotest.hardware.probesManager import GPSPosition, ProbesManager

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
    from paccotest.hardware.probesManagerDummy import ProbesManagerDummy
    g_probesMananager = ProbesManagerFactory.make_dummyProbesManager();  #For Dummy Probes
else:
    from paccotest.hardware.probesManagerReal import ProbesManagerReal
    g_probesMananager = ProbesManagerFactory.make_realProbesManager();  #For Real Probes



# Create your views here.


# The Opening Page
def opening(request):
    g_probesMananager.allProbesToSleep()
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
                if i !=  "csrfmiddlewaretoken" and request.POST[i] != "> skip all Questions":    #TODO: Make it cleaner
                    #print 'I have been passed the following keys: ',i, ' and value:',request.POST[i]
                    request.session['questionnaireValues'][i] = request.POST[i]

            #print request.session['questionnaireValues']  #DEBUG
            return HttpResponseRedirect(reverse('paccotest:probesForm'))

    all_questions_list = Question.objects.all().filter(actif=True).order_by('order')
    firstTab = 1
    lastTab = all_questions_list.count() + 1
    context = {'all_questions': all_questions_list,'firstTab':firstTab,'lastTab':lastTab}
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
    #print gpsValues
    #print questionnaireValues
    #print 'probesvalues===='
    #print probesValues  #DEBUG
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

    #print(request.session.keys())
    #print(request.session['probesValues'])
    #all_WaterCategories_list = WaterCategories.objects.all()
    #all_surveyProbeMeasures_list = ProbeMeasure.objects.all().filter(survey = survey)

    all_WaterCategorie_list = WaterCategorie.objects.all().order_by('order')
    #probeMeasures_list = ProbeMeasure.objects.get(survey_id='61')

    waterCategorieGoodtoUse_list = []

    for waterCategorie in all_WaterCategorie_list:
        watercategorieOK = True

        #print waterCategorie.text
        #for probe in probeMeasures_list:
        probesValues = request.session['probesValues']
        #print probesValues
        for key in probesValues:
            probe = Probe.objects.get(id=key)
            if probe.criterable == True:
                #print key
                #item = WaterCategoriesValue.objects.get(waterCategorie=waterCategorie,probeType=probe.probeType_id)
                item = WaterCategoriesValue.objects.get(waterCategorie=waterCategorie,probeType=Probe.objects.get(id=key))
                #print 'max'+str(item.valueMax)
                #print 'min'+str(item.valueMin)
                #print 'prVal'+probesValues[key]
                if item.valueMax >= float(probesValues[key]) >= item.valueMin:
                    #print waterCategorie.text+': MAYBE'
                    pass
                else:
                    print waterCategorie.text+': NON'
                    watercategorieOK = False
                    break
        if watercategorieOK == True:
            print waterCategorie.text+': OUI'
            #waterCategorieGoodtoUse_list.append(waterCategorie.text)
            waterCategorieGoodtoUse_list.append(waterCategorie.id)


    #print 'eau bonne pour:'
    #print waterCategorieGoodtoUse_list
    #print ', '.join(waterCategorieGoodtoUse_list)
    waterCat_list = []
    waterCat_listinString = '0'
    for i in waterCategorieGoodtoUse_list:
        waterCat_list.append(all_WaterCategorie_list[i].text)
        waterCat_listinString = waterCat_listinString+'--'+str(all_WaterCategorie_list[i].id)
    context = {'SESSION': json.dumps(gpsValues)+ " ---- " +json.dumps(questionnaireValues)+ " ---- " + json.dumps(probesValues),'waterCategorieslist':waterCat_list,'waterCategories_listinString':waterCat_listinString}
    return render(request, 'paccotest/complete.html', context)



#--------------------- CRON ----------------------------------
#Called on startup, if the RPI is connected to internet
def uploadToServer(request):
    newSurveys = Survey.objects.filter(uploadedToServer=False)
    uploadedCount = newSurveys.count()


    print(uploadedCount);
    return render(request, 'paccotest/uploadToServer.html', {'newSurveysCount':uploadedCount})

###
# get Raspberry PI unique identifier
###
def getRPIserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial
#--------------------- /CRON ----------------------------------

#Return a JSON from all user data for survey "surveyID"
def getJsonFromSurvey(surveyID):

    from django.core import serializers
    data = serializers.serialize("json", [Survey.objects.get(id=surveyID)])
    data2 =   serializers.serialize("json", UserAnswer.objects.filter(survey=surveyID), fields=('question','answer'))
    data3 =   serializers.serialize("json", ProbeMeasure.objects.filter(survey=surveyID), fields=('probeType','measure'))

    #return data + data2 + data3
    return '['+data+','+data2+','+data3+']'



#Ajax Calls
#URL: http://localhost:8000/paccotest/gpsPosition
def gpsPosition(request):
    gpsPosition = g_probesMananager.getGPSPosition()
    return HttpResponse(json.dumps(vars(gpsPosition)), content_type="application/json")


def probeMeasure(request, probeChannel):
    probeValue = g_probesMananager.getProbeValue(probeChannel)
    return HttpResponse(probeValue, content_type="application/json")

# Called when user click "Upload to server" in the uploadToServer.html page
def uploadToServerClick(request):
    newSurveys = Survey.objects.filter(uploadedToServer=False)
    uploadedCount = newSurveys.count()


# Called when userUpload to servero server" in the uploadToServer.html page
def uploadToServerClick(request):

    paccoboxid = getRPIserial() 
    softwareVersion = '1'
    newSurveys = Survey.objects.filter(uploadedToServer=False)
    uploadedCount = newSurveys.count()

    # send Survey via SMTP

    # Import smtplib to provide email functions
    import smtplib

    # Import the email modules
    from email.mime.text import MIMEText

    # Define email addresses to use
    addr_to   = 'paccobox@citymined.org'
    addr_from = 'paccobox@citymined.org'

    # Define SMTP email server details
    smtp_server = 'smtp.domainepublic.net:465'
    smtp_user   = 'paccobox@citymined.org'
    smtp_pass   = 'P4CC0B0X3CR1R3'

    s = smtplib.SMTP_SSL(smtp_server)

    for survey in newSurveys:
        msg = MIMEText(getJsonFromSurvey(survey.id))
        msg['To'] = addr_to
        msg['From'] = addr_from
        msg['Subject'] = 'PACCORESULT-'+str(paccoboxid)+'-'+softwareVersion+'-'+str(survey.id)

        survey.uploadedToServer = True
        survey.save() #Debug: commented for debugging

        # Send the message via an SMTP server
        s.login(smtp_user,smtp_pass)
        s.sendmail(addr_from, addr_to, msg.as_string())

    s.quit()


    # # Send to remote Queue
    # import pika
    #
    # #The RabbitMQ host
    # RABBITMQ_HOST = 'localhost'   #TODO: Add this to settings somewhere
    #
    #
    #
    #
    # credentials = pika.PlainCredentials('guest', 'guest')
    #
    # # parameters = pika.ConnectionParameters(host='localhost')
    #
    # parameters = pika.ConnectionParameters(RABBITMQ_HOST,
    #                                        5672,
    #                                        '/',
    #                                        credentials)
    #
    # connection = pika.BlockingConnection(parameters)
    #
    # channel = connection.channel()
    #
    # channel.queue_declare(queue='paccotest')
    #
    #
    # for survey in newSurveys:
    #     channel.basic_publish(exchange='',
    #                           routing_key='paccotest',
    #                           body=getJsonFromSurvey(survey.id))
    #     #survey.uploadedToServer = True
    #     #survey.save() #Debug: commented for debugging
    #
    # connection.close()

    #return HttpResponse("UploadedToServer: " + str(uploadedCount))

    # Get again the count in case that the upload hasn't succeed
    newSurveys = Survey.objects.filter(uploadedToServer=False)
    uploadedCountLeft = newSurveys.count()

    answer = {u"uploadCountLeft": uploadedCountLeft, u"error": "TO_BE_FILLED"}
    return HttpResponse(json.dumps(answer), content_type="application/json")

# Called when user click "Shutdown Paccotest" in the uploadToServer.html page
def doShutdown(request):
    print "Shutdown Paccotest"
    ## Code to shutdown the Raspberry PI
    import os.path
    from os.path import *

    sudoPassword = 'raspberry'
    command = "sudo shutdown -h now "
    p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    #-------
    return HttpResponse("Shuting Down Pacco-test", content_type="application/json")

def doPrint(request, datas):
    print 'start Printing'
    from paccotest.hardware.probesManagerReal import channelselect

    channelselect('2')
    from paccotest.hardware.Adafruit_Thermal import *

    printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
    printer.wake()
    import paccotest.hardware.logoPaccoTest as logo

    printer.printBitmap(logo.width, logo.height, logo.data)
    gpsValues = request.session['gpsForm']
    utc_formated = gpsValues["utc"][1:11]+' '+gpsValues["utc"][12:20]
    latitude = gpsValues["latitude"]
    longitude = gpsValues["longitude"]
    elevation = gpsValues["elevation"]
    printer.println('date&time: ',utc_formated)   
    printer.println('latitude: ',gpsValues["latitude"])   
    printer.println('longitude: ',gpsValues["longitude"])   
    printer.println('elevation: ',gpsValues["elevation"])   
    
    printer.println(_('Datas:'))
    probesValues = request.session['probesValues']
    for key in probesValues:
        line = Probe.objects.get(id=key).name + ': ' + probesValues[key]
        printer.println(line)
    
    datas = datas.split('-')
    printer.println(_('Results:'))
    if len(datas) > 1 :
	datas.pop(0)
	counter = 1
        for item in datas:
            waterCategorie=WaterCategorie.objects.get(pk=int(item))
            waterCategorie=remove_accents(waterCategorie.text)
            if counter == 1 :
                printer.println(_("water best used for: ")+waterCategorie)
            elif counter == 2 :
                phrase=_("water could be used for : ")
                phrase=phrase+waterCategorie
                if counter < len(datas) :
                    phrase=phrase+', '
                printer.println(phrase)
            else :
                phrase=waterCategorie
                if counter < len(datas) :
                    phrase=phrase+', '
                printer.println(phrase)
        counter += 1
    else :
        printer.println(_("water should not be"))

    printer.println()
    printer.println('Merci! * Bedankt! * Thank you!')
    printer.println('www.properwater.org')
    printer.println('www.eaupropre.org')
    printer.println()
    printer.println()
    printer.println()
    printer.println()
    printer.sleep()
    print 'end Printing'

    return HttpResponse("Print completed", content_type="application/json")

def remove_accents(string):
    return ''.join(c for c in unicodedata.normalize('NFD',string) if unicodedata.category(c) != 'Mn')

# Calibration Menu
def calibrateMenu(request):
    #all_probes_list = Probe.objects.filter(calibrable=True).order_by('channel')
    all_probes_list = CalibrationMemo.objects.all().order_by('probeType')
    return render(request, 'paccotest/calibrateMenu.html',{'all_probes': all_probes_list})

# The Calibration Page
def calibrate(request,probeType):
    g_probesMananager.StartCalibrateProbe(probeType)
    allProbeSteps = CalibrationSteps.objects.filter(probeType=probeType).order_by('probeType','order')
    lastTab = allProbeSteps.count() + 1
    return render(request, 'paccotest/calibrate.html',
                  {'lastTab': lastTab, 'allProbeSteps':allProbeSteps})

def calibrateMeasure(request,probeType,stepID):
    probeValue = g_probesMananager.calibrateProbe(probeType,stepID)
    return HttpResponse(probeValue, content_type="application/json")



def doCalibrationCommand(request,key):
    calibrateItem = CalibrationSteps.objects.get(id=key)
    if calibrateItem.tempCompensation==True:
        writeTemperature()
    ser.write(calibrateItem.command)

def writeTemperature(self):
	import glob
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
	def read_temp_raw():
		f = open(device_file, 'r')
		lines = f.readlines()
		f.close()
		return lines
	def read_temp():
		lines = read_temp_raw()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = read_temp_raw()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			#temp_f = temp_c + 9.0 / 5.0 + 32.0
			return temp_c
	line = read_temp()
	#return line
	ser.write("T,"+line+"\r")

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
