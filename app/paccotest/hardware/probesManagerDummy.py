from paccotest.hardware.probesManager import ProbesManager, GPSPosition
import time
from paccotest.models import Probe, CalibrationSteps, CalibrationMemo
from datetime import datetime
##
# A Dummy Probes Manager that emulates the real Probes behaviour
#
#
class ProbesManagerDummy(ProbesManager):

    def initGPIO( self ):
        pass

    def getGPSPosition(self):
        time.sleep(3)
        return GPSPosition(latitude = 12, longitude=13, elevation=14, utc="2014-07-24 21:45:38")

    def getProbeValue(self, probeName):
        #Probe.objects.get(name=probeName).channel
        time.sleep(1)
	from random import randint
        return randint(1,100)

    def StartCalibrateProbe(self,probeType):
		pass

    def calibrateProbe(self,probeType,stepID):
        if  stepID=='0':
            #save datetime of calibration
            CalibrationMemo.objects.update_or_create(probeType=Probe.objects.get(channel=probeType))
        return 'OK'
