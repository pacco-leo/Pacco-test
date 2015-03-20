from paccotest.hardware.probesManager import ProbesManager, GPSPosition
import time

##
# A Dummy Probes Manager that emulates the real Probes behaviour
#
#
class ProbesManagerDummy(ProbesManager):

    def initGPIO( self ):
        pass

    def getGPSPosition(self):
        time.sleep(0)
        return GPSPosition(latitude = 12, longitude=13, elevation=14, utc="2014-07-24 21:45:38")

    def getProbeValue(self, probeName):
        #Probe.objects.get(name=probeName).channel
        time.sleep(0)
	from random import randint
        return randint(1,100)
