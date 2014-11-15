import os
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.http import HttpResponse
from paccotest.models import Reponses
from paccotest.probesManager import GPSPosition, ProbesManager
import json

##
# Abstract Factory of Probe Managers
#
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
    from paccotest.probesManagerDummy import ProbesManagerDummy  # For Dummy Probes
    g_probesMananager = ProbesManagerFactory.make_dummyProbesManager();  #For Dummy Probes
else:
    from paccotest.probesManagerReal import ProbesManagerReal  #For Real Probes
    g_probesMananager = ProbesManagerFactory.make_realProbesManager();  #For Real Probes




def port(timeot):
    usbport = '/dev/ttyAMA0'
    global ser
    ser = serial.Serial(usbport, 38400, timeout=timeot)
    ser.flushInput()
    ser.flushOutput()


def keep_result(idtest, col, val):
    r1 = Reponses.objects.get(titre=idtest)
    #r1 = Reponses(col=val)
    exec "r1." + str(col) + " = '" + str(val) + "'"
    #r1.col = val
    r1.save()
    print 'datetime' + str(r1.datetime)
    print 'gps1' + str(r1.gps1)
    print 'gps2' + str(r1.gps2)
    print 'gps3' + str(r1.gps3)
    print 'Q1' + str(r1.q1)
    print 'Q2' + str(r1.q2)
    print 'Q3' + str(r1.q3)
    print 'Q4' + str(r1.q4)
    print 'Q5' + str(r1.q5)
    print 'Q6' + str(r1.q6)
    print 'Q7' + str(r1.q7)
    print 'Q8' + str(r1.q8)
    print 'Q9' + str(r1.q9)
    print 'Q10' + str(r1.q10)
    print 'Q11' + str(r1.q11)
    print 'Q12' + str(r1.q12)
    print 'S1' + str(r1.s1)
    print 'S2' + str(r1.s2)
    print 'S3' + str(r1.s3)
    print 'S4' + str(r1.s4)
    print 'S5' + str(r1.s5)


#r1 = Reponses.objects.get(titre='te')
#r1.titre='pool'
#r1.save()
#r1 = Reponses(titre="te",q1=1,q2=1)
#r1.save()
def ouverture(request):
    # r1 = Reponses(titre="aa")
    #r1.save()

    # Initilization of the GPIO
    g_probesMananager.initGPIO()

    Reponses.objects.create(titre="tem")
    r1 = Reponses.objects.get(titre="tem")
    r1.titre = r1.id
    nid = r1.id
    r1.save()  #r1 = Reponses.objects.get(titre=nid)
    #print r1.titre
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../img/')
    return render_to_response('ouverture.html', {'nid': nid, 'imgfolder': file_path})


def intro(request, nid, lg):
    #import eval('txt_'+lg) as txts
    exec 'import txt_' + lg + ' as txts'
    return render_to_response('intro.html', {'nid': nid, 'lg': lg, 'txt': txts, })


#array_CSV.append('blibli')
#array_CSV.append('bloblo')
#array_CSV.append('bleble')
#array_CSV=[]

def position(request, nid, lg):
    # Get the GPS coordinates
    #gpsPosition = g_probesMananager.getGPSPosition()

    #if lg == 'fr':
    #	import txt_fr as txts
    #elif lg == 'nl':
    #	import txt_nl as txts
    #else :
    #	import txt_en as txts
    exec 'import txt_' + lg + ' as txts' in globals(), locals()

    #return render_to_response('position.html', {'latitude': gpsPosition.latitude, 'longitude': gpsPosition.longitude,
    #                                            'altitude': gpsPosition.altitude, 'utc': gpsPosition.utc, 'nid': nid,
    #                                            'lg': lg,
    #                                            'txt': txts})
    return render_to_response('position.html', {'nid': nid, 'lg': lg, 'txt': txts})


def question(request, nid, lg, num):
    exec 'import txt_' + lg + ' as txts'
    qtotal = 12  #nombre de questions
    last_question = False
    correction = False
    array_qr = ''
    othervariables = ''

    if 'correction' in request.GET:
        correction = request.GET.get('correction')

    if int(num) > 1:
        if correction == False:
            answer = str(int(request.GET.get('r')) - 1)
            keep_result(nid, 'q' + str(int(num) - 1), answer)
        else:
            if correction != 'True':
                answer = str(int(request.GET.get('r')) - 1)
                keep_result(nid, 'q' + str(correction), answer)
    if int(num) == qtotal + 1:  # page resume
        question = ''
        array_reponses = ''
        array_qr = []
        for nq in range(1, qtotal + 1):
            temp_array = []
            q = txts.questions[nq - 1][0]
            temp_array.append(nq)
            temp_array.append(q)
            r1 = Reponses.objects.get(titre=nid)
            exec "r = txts.questions[nq-1][1][r1.q" + str(nq) + "]"
            temp_array.append(r)
            array_qr.append(temp_array)
        last_question = True
        qnext = '../../../sonde/' + nid + '/' + lg + '/1?etape=1'
    else:
        question = txts.questions[int(num) - 1][0]
        reponses = txts.questions[int(num) - 1][1]
        array_reponses = []
        for r in reponses:
            array_reponses.append(r)
        if correction == False:
            qnext = int(num) + 1
        else:
            qnext = str(qtotal + 1)
            othervariables = '&correction=' + num

    return render_to_response('question.html',
                              {'qact': num, 'qnext': qnext, 'qtotal': qtotal, 'txt': txts, 'question': question,
                               'reponses': array_reponses, 'othervariables': othervariables,
                               'last_question': last_question, 'range': range(0, qtotal), 'array_qr': array_qr})


def sonde(request, nid, lg, num):
    # Get the probes values
    (line, sensor, num, snext, stotal, etape, txts, last_question) = g_probesMananager.getProbesValues()

    exec 'import txt_' + lg + ' as txts' in globals(), locals()

    return render_to_response('sonde.html',
                              {'result': line, 'sensor': sensor, 'sact': num, 'snext': snext,
                               'stotal': stotal, 'etape': etape, 'txt': txts, 'last_question': last_question})


def outro(request, nid, lg):
    #import eval('txt_'+lg) as txts
    exec 'import txt_' + lg + ' as txts'
    # PRINT
    #from Adafruit_Thermal import *
    #print 'start'
    #channel = channelselect(2)
    #printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
    ##printer.wake()
    #import PaccoTestPrintLogo as logo
    #printer.printBitmap(logo.width, logo.height, logo.data)
    #xdate = time.strftime("%d-%m-%Y")
    #xtime = time.strftime("%H:%M:%S")
    #printer.println(xdate+', '+xtime)
    #printer.println()
    #printer.println()
    #printer.sleep()
    #print 'end'
    #ser.flushInput()
    #ser.flushOutput()
    write_csv(nid)
    #return render_to_response('outro.html',{'nid':nid,'lg':lg,'txt':txts})
    return render_to_response('outro.html', {'txt': txts})


# function generales

def write_csv(nid):
    #phrase=sensor+':'+data
    #show on screen
    #print phrase
    #print ''
    #keep data to print later
    #results_datas.append(phrase)
    #write data to CSV


    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../export/paccotest.txt')
    f = open(file_path, 'a')
    datas = Reponses.objects.filter(titre=nid).values()
    for d in datas:
        f.write(str(d))
    #datas = Reponses.objects.get(titre=nid)
    #for name,value in datas.get_fields:
    #	if value:
    #		f.write(name+':'+str(value)+';')
    f.write('\n')
    f.close()

#clear line
#line = ""

def updateremote(request):
    return render_to_response('updateRemote.html')


#Ajax Calls
#URL: http://localhost:8000/paccotest/gpsPosition
def gpsPosition(request):
    gpsPosition = g_probesMananager.getGPSPosition()
    return HttpResponse(json.dumps(vars(gpsPosition)), content_type="application/json")
