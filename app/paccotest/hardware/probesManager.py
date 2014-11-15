##
# Datas from the GPS
#
#
class GPSPosition:
    latitude = 0
    longitude = 0
    elevation = 0
    utc = 0

    def __init__(self, latitude, longitude, elevation, utc):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.utc = utc


##
# An abstract class for making tests with probes
#
#
class ProbesManager:

    def initGPIO( self ):
        raise NotImplementedError( "Should have implemented this" )

    def getGPSPosition(self):
        return NotImplementedError( "Should have implemented this" )

    def getProbeValue(self, probeName):
        return NotImplementedError( "Should have implemented this" )

