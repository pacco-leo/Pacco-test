class GPSPosition:
    latitude = 0
    longitude = 0
    altitude = 0
    utc = 0

    def __init__(self, latitude, longitude, altitude, utc):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.utc = utc


class ProbesManager:
    def initProbes(self):
        pass
        # Initilization of the GPIO
        # Matt: Commented this
        # GPIO.setmode(GPIO.BOARD)
        #
        # GPIO.setup(16, GPIO.OUT)
        # GPIO.setup(18, GPIO.OUT)
        # GPIO.setup(22, GPIO.OUT)


    def getGPSPosition(self):
        pass
        # import gps
        # import threading
        # # if ser.isOpen() != True:
        # #	ser.open()
        # channelselect(0)
        # port(0)
        # #os.system('sudo killall gpsd')
        # #print 'killall gpsd'
        # #os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')
        # #print 'set gps port'
        # #usbport = '/dev/ttyAMA0'
        # #ser = serial.Serial(usbport, 38400, timeout=0)
        #
        # global gpsd
        # gpsd = None  #seting the global variable
        #
        # #os.system('clear') #clear the terminal (optional)
        #
        # class GpsPoller(threading.Thread):
        # def __init__(self):
        # threading.Thread.__init__(self)
        #         global gpsd  #bring it in scope
        #         gpsd = gps.gps(mode=gps.WATCH_ENABLE)  #starting the stream of info
        #         self.current_value = None
        #         self.running = True  #setting the thread running to true
        #
        #     def run(self):
        #         global gpsd
        #         while self.running:
        #             try:
        #                 if gpsd.waiting():
        #                     gpsd.next()  #this will continue to loop and grab EACH set of gpsd info to clear the buffer
        #             except:
        #                 raise
        #
        # gpsp = GpsPoller()  # create the thread
        #
        # gpsp.start()  # start it up
        # #os.system('clear')
        # countloop = 0
        # while True:
        #     if (gpsd.fix.latitude != 0.0):
        #         print
        #         print 'GPS reading'
        #         print '----------------------------------------'
        #         #global gpsd
        #
        #         print 'latitude    ', gpsd.fix.latitude
        #         print 'longitude   ', gpsd.fix.longitude
        #         print 'time utc    ', gpsd.utc, ' + ', gpsd.fix.time
        #         print 'altitude (m)', gpsd.fix.altitude
        #         #data = str(gpsd.utc)+';'+str(gpsd.fix.latitude)+';'+str(gpsd.fix.longitude)+';'+str(gpsd.fix.altitude)
        #         #print data
        #         #write_csv(data)
        #
        #         break
        #     elif countloop > 3:
        #         print
        #         print 'GPS failed'
        #         gpsd.fix.longitude = 'None'
        #         gpsd.fix.latitude = 'None'
        #         gpsd.fix.altitude = 'None'
        #         gpsd.utc = 'None'
        #         break
        #
        #     else:
        #         print gpsd.fix.latitude
        #         print 'GPS looking for satellite'
        #         print '----------------------------------------'
        #         countloop += 1
        #         time.sleep(5)
        # keep_result(nid, 'datetime', gpsd.utc)
        # keep_result(nid, 'gps1', gpsd.fix.latitude)
        # keep_result(nid, 'gps2', gpsd.fix.longitude)
        # keep_result(nid, 'gps3', gpsd.fix.altitude)
        # print "\nKilling Thread..."
        # gpsp.running = False
        # gpsp.join()  # wait for the thread to finish what it's doing
        #
        # ser.flushInput()
        # ser.flushOutput()
        #
        # #ser.close()
        # print "Done.\nExiting."

        # return GPSPosition(gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.utc)
        return GPSPosition(12, 13, 14, 15)


