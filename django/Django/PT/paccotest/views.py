import os
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from paccotest.models import Reponses
import serial, time, RPi.GPIO as GPIO

#sensors
sensors=[('PH',4),('REDOX',5),('CONDUCTIVITY',7),('DO',6),('TEMPERATURE',100)]

def channelselect (cs):
    if cs == 0:
        A = 0
        B = 0
        C = 0
	print '-------GPS'
    elif cs == 1:
        A = 0
        B = 0
        C = 1
    elif cs == 2:
        A = 0
        B = 1
        C = 0
	print '-------print results'
    elif cs == 3:
        A = 0
        B = 1
        C = 1
    elif cs == 4:
        A = 1
        B = 0
        C = 0
	print '-------PH'
    elif cs == 5:
        A = 1
        B = 0
        C = 1
	print '-------REDOX (ORP)'
    elif cs == 6:
        A = 1
        B = 1
        C = 0
	print '-------DO'
    elif cs == 7:
        A = 1
        B = 1
        C = 1
	print '-------CONDUCTIVITY'
    #clear input/output
    #ser.flushInput()
    #ser.flushOutput() 
  
    #return [A,B,C]
    GPIO.output(16,A) #S2
    GPIO.output(18,B) #S1
    GPIO.output(22,C) #S0


def port(timeot) :

	usbport = '/dev/ttyAMA0'
	global ser
	ser = serial.Serial(usbport, 38400, timeout=timeot)
    	ser.flushInput()
    	ser.flushOutput()


def keep_result(idtest,col,val):

	r1 = Reponses.objects.get(titre=idtest)
	#r1 = Reponses(col=val)
	exec "r1."+str(col)+" = '"+str(val)+"'"
	#r1.col = val
	r1.save()
	print 'datetime'+str(r1.datetime)
	print 'gps1'+str(r1.gps1)
	print 'gps2'+str(r1.gps2)
	print 'gps3'+str(r1.gps3)
	print 'Q1'+str(r1.q1)
	print 'Q2'+str(r1.q2)
	print 'Q3'+str(r1.q3)
	print 'Q4'+str(r1.q4)
	print 'Q5'+str(r1.q5)
	print 'Q6'+str(r1.q6)
	print 'Q7'+str(r1.q7)
	print 'Q8'+str(r1.q8)
	print 'Q9'+str(r1.q9)
	print 'Q10'+str(r1.q10)
	print 'Q11'+str(r1.q11)
	print 'Q12'+str(r1.q12)
	print 'S1'+str(r1.s1)
	print 'S2'+str(r1.s2)
	print 'S3'+str(r1.s3)
	print 'S4'+str(r1.s4)
	print 'S5'+str(r1.s5)
	#r1 = Reponses.objects.get(titre='te')
	#r1.titre='pool'
	#r1.save() 
	#r1 = Reponses(titre="te",q1=1,q2=1)
	#r1.save()
def ouverture(request):
#r1 = Reponses(titre="aa")
#r1.save()
	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(16, GPIO.OUT)
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(22, GPIO.OUT)

	Reponses.objects.create(titre="tem")
	r1 = Reponses.objects.get(titre="tem")
	r1.titre = r1.id
	nid = r1.id
	r1.save()
	#r1 = Reponses.objects.get(titre=nid)
	#print r1.titre
	module_dir = os.path.dirname(__file__)
	file_path = os.path.join(module_dir,'../img/')
	return render_to_response('ouverture.html',{'nid':nid,'imgfolder':file_path})

def intro(request,nid,lg):
	#import eval('txt_'+lg) as txts
	exec 'import txt_'+lg+' as txts'
	return render_to_response('intro.html',{'nid':nid,'lg':lg,'txt':txts,})
	#array_CSV.append('blibli')
	#array_CSV.append('bloblo')
	#array_CSV.append('bleble')
#array_CSV=[]

def position(request,nid,lg):

	import gps
	import threading
	#if ser.isOpen() != True:
	#	ser.open()
	channelselect(0)
	port(0)
	#os.system('sudo killall gpsd')
	#print 'killall gpsd'
	#os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')
	#print 'set gps port'
	#usbport = '/dev/ttyAMA0'
	#ser = serial.Serial(usbport, 38400, timeout=0)

	global gpsd
	gpsd = None #seting the global variable
	 
	#os.system('clear') #clear the terminal (optional)
	
	class GpsPoller(threading.Thread):
	  def __init__(self):
	    threading.Thread.__init__(self)
	    global gpsd #bring it in scope
	    gpsd = gps.gps(mode=gps.WATCH_ENABLE) #starting the stream of info
	    self.current_value = None
	    self.running = True #setting the thread running to true
	 
	  def run(self):
	    global gpsd
	    while self.running:
		try:
			if gpsd.waiting():
		      		gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
	 	except:
			raise
	gpsp = GpsPoller() # create the thread

	gpsp.start() # start it up
	#os.system('clear')
	countloop = 0
	while True:
		if(gpsd.fix.latitude!=0.0):
			print
			print 'GPS reading'
			print '----------------------------------------'
			#global gpsd

			print 'latitude    ' , gpsd.fix.latitude
			print 'longitude   ' , gpsd.fix.longitude
			print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
			print 'altitude (m)' , gpsd.fix.altitude
			#data = str(gpsd.utc)+';'+str(gpsd.fix.latitude)+';'+str(gpsd.fix.longitude)+';'+str(gpsd.fix.altitude)
			#print data
			#write_csv(data)

			break
		elif countloop > 3:
			print
			print 'GPS failed'
			gpsd.fix.longitude='None'
			gpsd.fix.latitude='None'
			gpsd.fix.altitude='None'
			gpsd.utc='None'
			break			
			
		else:
			print gpsd.fix.latitude
			print 'GPS looking for satellite'
			print '----------------------------------------'
			countloop += 1
			time.sleep(5)
	keep_result(nid,'datetime',gpsd.utc)
	keep_result(nid,'gps1',gpsd.fix.latitude)
	keep_result(nid,'gps2',gpsd.fix.longitude)
	keep_result(nid,'gps3',gpsd.fix.altitude)	 	 
	print "\nKilling Thread..."
	gpsp.running = False
	gpsp.join() # wait for the thread to finish what it's doing

    	ser.flushInput()
   	ser.flushOutput()
	
	#ser.close()
	print "Done.\nExiting."	
	#if lg == 'fr':
	#	import txt_fr as txts
	#elif lg == 'nl':
	#	import txt_nl as txts
	#else :
	#	import txt_en as txts
	exec 'import txt_'+lg+' as txts' in globals(), locals()
	return render_to_response('position.html',{'latitude':gpsd.fix.latitude,'longitude':gpsd.fix.longitude,'altitude':gpsd.fix.altitude,'utc':gpsd.utc,'nid':nid,'lg':lg,'txt':txts})


def question(request,nid,lg,num):

	exec 'import txt_'+lg+' as txts'	
	qtotal=12 #nombre de questions
	last_question = False
	correction = False
	array_qr = ''
	othervariables=''

	if 'correction' in request.GET:	
		correction = request.GET.get('correction')

	if int(num) > 1:
		if correction == False:
			answer=str(int(request.GET.get('r'))-1)
			keep_result(nid,'q'+str(int(num)-1),answer)
		else:
			if correction != 'True':
				answer=str(int(request.GET.get('r'))-1)
				keep_result(nid,'q'+str(correction),answer)
	if int(num)==qtotal+1: # page resume
		question = ''
		array_reponses = ''
		array_qr = []
		for nq in range(1,qtotal+1):
			temp_array = []
			q = txts.questions[nq-1][0]
			temp_array.append(nq)
			temp_array.append(q)
			r1 = Reponses.objects.get(titre=nid)
			exec "r = txts.questions[nq-1][1][r1.q"+str(nq)+"]"
			temp_array.append(r)
			array_qr.append(temp_array)
		last_question = True
		qnext='../../../sonde/'+nid+'/'+lg+'/1?etape=1'
	else:
		question = txts.questions[int(num)-1][0]
		reponses = txts.questions[int(num)-1][1]
		array_reponses = []
		for r in reponses:
			array_reponses.append(r)
		if correction == False:
			qnext=int(num)+1
		else:
			qnext=str(qtotal+1)
			othervariables = '&correction='+num
		
	return render_to_response('question.html',{'qact':num,'qnext':qnext,'qtotal':qtotal,'txt':txts,'question':question,'reponses':array_reponses,'othervariables':othervariables,'last_question':last_question,'range':range(0,qtotal),'array_qr':array_qr})

def sonde(request,nid,lg,num):
	last_question = False
	correction = 'False'
	array_qr = ''
	if 'correction' in request.GET:	
		correction = request.GET.get('correction')

	exec 'import txt_'+lg+' as txts' in globals(), locals()
	stotal = len(sensors)

	if int(num)==stotal+1:
		array_qr = []
		for ns in range(1,stotal+1):
			print ns
			temp_array = []
			s = sensors[int(ns)-1][0]
			temp_array.append(ns)
			temp_array.append(s)
			r1 = Reponses.objects.get(titre=nid)
			exec "r = r1.s"+str(ns) in globals(), locals()
			temp_array.append(r)
			array_qr.append(temp_array)
		last_question = True
		snext='../../../outro/'+nid+'/'+lg
		return render_to_response('sonde.html',{'sensor':array_qr,'sact':'X','snext':snext,'stotal':stotal,'etape':'X','txt':txts,'last_question':last_question})
	else:
		if correction == 'False':
			snext=str(int(num)+1)+'?etape=1'
		else:
			snext=str(stotal+1)
		
		etape = int(request.GET.get('etape'))
	
		if etape == 1 :	
				
			return render_to_response('sonde.html',{'sensor':sensors[int(num)-1][0],'sact':num,'snext':snext,'stotal':stotal,'etape':etape,'txt':txts,'last_question':last_question,'correction':correction})
		elif etape == 2 :
			if sensors[int(num)-1][0] == 'TEMPERATURE' :
				import glob
				os.system('modprobe w1-gpio')
				os.system('modprobe w1-therm')

				base_dir='/sys/bus/w1/devices/'
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
						#temp_f = temp_c * 9.0 / 5.0 + 32.0
						#return temp_c, temp_f
						return temp_c
				line = read_temp()
				#write_csv(str(line))
				keep_result(nid,'s'+num,str(line))
				print line	
			else :
				channelselect(sensors[int(num)-1][1])
				port(None)

				ser.write("L1\r")
				ser.write("C\r")
				line = ""
				countloop = 0
				while True:
					data = ser.read()
					if(data == "\r"):
						#waiting_room()		
						#treat_results(sensor,line)
						print line
						#write_csv(line)
						keep_result(nid,'s'+num,str(line))
						break
					elif countloop > 20000:
						print 'failed'
						line = 'X'
						break
					else:
						line = line + data
						countloop += 1
					
		
			return render_to_response('sonde.html',{'result':line,'sensor':sensors[int(num)-1][0],'sact':num,'snext':snext,'stotal':stotal,'etape':etape,'txt':txts,'last_question':last_question})


def outro(request,nid,lg):
	#import eval('txt_'+lg) as txts
	exec 'import txt_'+lg+' as txts'
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
	return render_to_response('outro.html',{'txt':txts})


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
	file_path = os.path.join(module_dir,'../export/paccotest.txt')
	f = open(file_path,'a')
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



