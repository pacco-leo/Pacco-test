from paccotest.hardware.probesManager import ProbesManager, GPSPosition
from paccotest.models import Probe, CalibrationSteps, CalibrationMemo
import serial, RPi.GPIO as GPIO
import os, time, threading
import gps
from datetime import datetime

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)



#TRY 27 juin 2015
usbport="/dev/ttyAMA0"
ser = serial.Serial(usbport,9600)




##
# A Probes Manager for the real-world probes
#
#
class ProbesManagerReal(ProbesManager):
    def getGPSPosition(self):
	channelselect('0')
	# a mettre aileurs ? pour eviter le sleepp 3 seconds...
	os.system('>& killall gpsd')
	os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')
	time.sleep(3) #time needed for gps-port start

	global gpsd
	gpsd = None #seting the global variable
	class GpsPoller(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			global gpsd #bring it in scope
			gpsd = gps.gps(mode=gps.WATCH_ENABLE) #starting the stream of info
			self.current_value = None
			self.running = True #setting the thread running to true
		def run(self):
			global gpsd
			while gpsp.running:
				gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
	gpsp = GpsPoller() # create the thread
	gpsp.start() # start it up
	countloop = 0
	import math
	while True:
		if (gpsd.fix.latitude != 0.0 and math.isnan(gpsd.fix.latitude) != True):
			print
			print 'GPS reading'
			print '----------------------------------------'
			# global gpsd
			print 'latitude    ', gpsd.fix.latitude
			print 'longitude   ', gpsd.fix.longitude
			print 'time utc    ', gpsd.utc, ' + ', gpsd.fix.time
			print 'altitude (m)', gpsd.fix.altitude
			break
		elif countloop > 3:
			print
			print 'GPS failed'
			gpsd.fix.longitude = '0'
			gpsd.fix.latitude = '0'
			gpsd.fix.altitude = '0'
			gpsd.utc = '2015-03-20 08:00:00'
			break
		else:
			print 'GPS looking for satellite'
			print '----------------------------------------'
			countloop += 1
			time.sleep(5)
	print "\nKilling Thread..."
	gpsp.running = False
	#gpsp.join() # wait for the thread to finish what it's doing
	print "Done.\nExiting."
	utc_formated = gpsd.utc[:10]+' '+gpsd.utc[11:19]
	latitude=gpsd.fix.latitude
	longitude=gpsd.fix.longitude
	altitude=gpsd.fix.altitude
	os.system('sudo killall gpsd')
        return GPSPosition(latitude, longitude, altitude, utc_formated)
	
    ##
    # Get values form probes
    #
    def getProbeValue(self, probeChannel):
	if probeChannel == '15': #temperature is not on muxdemux
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
		return line	
	else:
		#port()	
		channelselect(probeChannel)
		########usbport='/dev/ttyAMA0'
		########ser = serial.Serial(usbport,9600)
		########ser.flushInput()
		########ser.flushOutput()
		time.sleep(.5)
		#ser.write("L,1\r")
		ser.write("WAKEUP!\r")
		ser.write("C,1\r")
		line=""
		counterLoop=20	
		#sensorOK=0
		while True:
			data=ser.read()
			if(data== "\r" and counterLoop>0):
				counterLoop -= 1
				print line
				line=""
			elif(data == "\r" and line == '*OK'):
				line=""
				print 'redo'
			elif(data == "\r" and line == '*ER'):
				line=""
				print 'redo'
			elif(data == "\r"):
				#if(sensorOK==1 and line!='*OK'):
				#	print "Received from sensor:" + line
				#	return line
				#	line = ""
				#	break
				#if(line=='*OK'):
				#	print 'sensor OK'
				#	sensorOK=1
				#line = ""
				print "Received from sensor:" + line
				ser.write("C,0\r")
				ser.write("RESPONSE,0\r")
				time.sleep(.5)
				ser.write("SLEEP\r")
				time.sleep(.5)
				return line
				break
			else:
				line = line + data
				print 'working...'
		time.sleep(.5)
		ser.write("SLEEP\r")
		time.sleep(.5)

    ##
    # Calibrate probes
    #
    def StartCalibrateProbe(self,probeType):
        probe=Probe.objects.get(pk=probeType)
	channelselect(str(probe.channel))
	#########import serial
	#########usbport='/dev/ttyAMA0'
	#########ser = serial.Serial(usbport,9600)
	#########ser.flushInput()
	#########ser.flushOutput()
	time.sleep(.5)
	ser.write("wake\r")
	time.sleep(.5)
        ser.write("C,0\r")
	ser.write("Cal,clear\r")
    def calibrateProbe(self,probeType,stepID):
        if  stepID=='0':
            print 'step 000'
            #verfier si tout s'est bien pass
            allProbeSteps = CalibrationSteps.objects.filter(probeType=probeType)
            nbSteps=allProbeSteps.count()
            if probeType=='4':
                nbSteps=nbSteps-1
            print 'nbsteps='+str(nbSteps)
            ########ser = serial.Serial('/dev/ttyAMA0',9600)
            ser.write("WAKE UP\r")
            ser.write("Cal,?\r")
            ser.write("Cal,?\r")
            line=""
            print 'rr'
            while True:
                data=ser.read()
                if(data == "\r" and line.startswith('*')):
                    print line
                    line=""
		    ser.write("Cal,?\r")
		elif(data == "\r"):
                    creturn = line
                    print creturn
                    line = ""
                    break
                else:
                    line = line + data
            if (creturn == '?CAL,'+str(nbSteps)):
                #tout est OK
                #save datetime of calibration
                CalibrationMemo.objects.update_or_create(probeType=probeType)
                #put EZO circuit of the probe to SLEEP
                time.sleep(.5)
                ser.write("SLEEP\r")
                time.sleep(.5)
                print 'well done'
                return 'The probe has been well calibrated.'
            else: #error
                print 'error'
        else :
               #######ser = serial.Serial('/dev/ttyAMA0',9600)
               step = CalibrationSteps.objects.get(id=stepID)
               print 'OOOOOO'
               #time.sleep(step.delay)
               ser.write('WAKE\r')
               time.sleep(.5)
               ser.write(step.command+"\r")
               print 'ICI'
               print(step.command+"\r")
               return 'OK'

def port():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(16,GPIO.OUT)
	GPIO.setup(18,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)

	#usbport='/dev/ttyAMA0'
	#global ser
	#ser=serial.Serial(usbport,9600)
	#ser.flushInput()
	#ser.flushOutput()
	

def channelselect(cs):
    print 'cs='+cs
    if cs == '0':
        A = 0
        B = 0
        C = 0
        print '-------GPS'
    elif cs == '1':
        A = 0
        B = 0
        C = 1
    elif cs == '2':
        A = 0
        B = 1
        C = 0
        print '-------print results'
    elif cs == '3':
        A = 0
        B = 1
        C = 1
    elif cs == '4':
        A = 1
        B = 0
        C = 0
        print '-------PH'
    elif cs == '5':
        A = 1
        B = 0
        C = 1
        print '-------REDOX (ORP)'
    elif cs == '6':
        A = 1
        B = 1
        C = 0
        print '-------DO'
    elif cs == '7':
        A = 1
        B = 1
        C = 1
        print '-------CONDUCTIVITY'
        # clear input/output
        # ser.flushInput()
        # ser.flushOutput()

    #return [A,B,C]
    #Matt: commented
    #GPIO.cleanup()
    ser.flushInput()
    ser.flushOutput()
    GPIO.output(16,A) #S2
    GPIO.output(18,B) #S1
    GPIO.output(22,C) #S0
    ser.flushInput()	
    ser.flushOutput()
