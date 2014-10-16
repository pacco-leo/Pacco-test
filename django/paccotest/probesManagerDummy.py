from paccotest.probesManager import *

class ProbesManagerDummy(ProbesManager):

    def initGPIO( self ):
        pass

    def getGPSPosition(self):
        return GPSPosition(12, 13, 14, 15)

    def getProbesValues(self):
        return {'line': "hello", 'sensor': 2, 'sact': 3, 'snext': 4,
            'stotal': 5, 'etape': 6, 'txt': "hello", 'last_question': "lastQuestion"}  # sensors