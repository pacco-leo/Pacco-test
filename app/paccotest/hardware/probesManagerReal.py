from paccotest.hardware.probesManager import *
from paccotest.models import Probe
import serial, RPi.GPIO as GPIO
import os, time, threading
from gps import *

##
# A Probes Manager for the real-world probes
#
#
class ProbesManagerReal(ProbesManager):
    def getGPSPosition(self):
	global gpsd
	gpsd = None #seting the global variable
	class GpsPoller(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
			global gpsd #bring it in scope
			gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
			self.current_value = None
			self.running = True #setting the thread running to true
		def run(self):
			global gpsd
			while gpsp.running:
				gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
	gpsp = GpsPoller() # create the thread
	gpsp.start() # start it up
	countloop = 0
	while True:
		if (gpsd.fix.latitude != 0.0):
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
			gpsd.fix.longitude = 'None'
			gpsd.fix.latitude = 'None'
			gpsd.fix.altitude = 'None'
			gpsd.utc = 'None'
			break
		else:
			print 'GPS looking for satellite'
			print '----------------------------------------'
			countloop += 1
			time.sleep(5)
	print "\nKilling Thread..."
	gpsp.running = False
	gpsp.join() # wait for the thread to finish what it's doing
	print "Done.\nExiting."
	utc_formated = gpsd.utc[:10]+' '+gpsd.utc[11:19]
        return GPSPosition(gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, utc_formated)

    ##
    # Get values form probes
    #
    def getProbeValue(self, probeName):
	if probeName == 'temperature':
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
		probeChannel = Probe.objects.get(name=probeName).channel
		channelselect(probeChannel)
		port()
		ser.write("L,1\r")
		ser.write("C,1,\r")
		line=""
		while True:
			data=ser.read()
			if(data== "\r"):
				print "Received from sensor:" + line
				return line
				line=""
				break
			else:
				line= line + data
	


#sensors = [('PH', 4), ('REDOX', 5), ('CONDUCTIVITY', 7), ('DO', 6), ('TEMPERATURE', 100)]


def port():
	usbport='/dev/ttyAMA0'
	global ser
	ser=serial.Serial(usbport,38400)
	ser.flushInput()
	ser.flushOutput()
	

def channelselect(cs):
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
        # clear input/output
        # ser.flushInput()
        # ser.flushOutput()

        #return [A,B,C]
        #Matt: commented
        GPIO.output(16,A) #S2
        GPIO.output(18,B) #S1
        GPIO.output(22,C) #S0