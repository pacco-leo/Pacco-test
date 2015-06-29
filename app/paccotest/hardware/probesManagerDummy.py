from paccotest.hardware.probesManager import ProbesManager, GPSPosition
import time
from paccotest.models import Probe, CalibrationSteps, CalibrationMemo
from datetime import datetime

##
# A Dummy Probes Manager that emulates the real Probes behaviour
#
#
class ProbesManagerDummy(ProbesManager):

    def allProbesToSleep(self):
	pass

    def initGPIO( self ):
        pass

    def getGPSPosition(self):
        time.sleep(3)
        from django.utils import timezone
        return GPSPosition(latitude = 12, longitude=13, elevation=14, utc=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

    def getProbeValue(self, probeName):
        #Probe.objects.get(name=probeName).channel
        time.sleep(1)
	    #from random import randint
        #return randint(1,100)
        return 5

    def StartCalibrateProbe(self,probeType):
		pass

    def calibrateProbe(self,probeType,stepID):
        if  stepID=='0':
            #save datetime of calibration
            CalibrationMemo.objects.update_or_create(probeType=Probe.objects.get(channel=probeType))
        return 'OK'
