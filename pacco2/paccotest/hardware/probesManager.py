##
# Datas from the GPS
#
#
class GPSPosition:
    latitude = 0
    longitude = 0
    elevation = 0
    utc = 0


##
# An abstract class for making tests with probes
#
#
class ProbesManager:

    def initGPIO( self ):
        raise NotImplementedError( "Should have implemented this" )


    def getGPSPosition(self):
        return NotImplementedError( "Should have implemented this" )

    def getProbeValue(self, probeType):
        return NotImplementedError( "Should have implemented this" )

