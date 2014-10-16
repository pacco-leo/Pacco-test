from paccotest.probesManager import *
import serial, time, RPi.GPIO as GPIO


class ProbesManagerReal(ProbesManager):
    # #
    # Initialize GPIO
    #
    def initGPIO(self):
        # Initilization of the GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)

    ##
    # Get GPS Position
    #
    def getGPSPosition(self):
        import gps
        import threading
        # if ser.isOpen() != True:
        # ser.open()
        channelselect(0)
        port(0)
        # os.system('sudo killall gpsd')
        # print 'killall gpsd'
        #os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')
        #print 'set gps port'
        #usbport = '/dev/ttyAMA0'
        #ser = serial.Serial(usbport, 38400, timeout=0)

        global gpsd
        gpsd = None  #seting the global variable

        #os.system('clear') #clear the terminal (optional)

        class GpsPoller(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)

        global gpsd  #bring it in scope
        gpsd = gps.gps(mode=gps.WATCH_ENABLE)  #starting the stream of info
        self.current_value = None
        self.running = True  #setting the thread running to true

        def run(self):
            global gpsd
            while self.running:
                try:
                    if gpsd.waiting():
                        gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer
                except:
                    raise

        gpsp = GpsPoller()  # create the thread

        gpsp.start()  # start it up
        # os.system('clear')
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
                #data = str(gpsd.utc)+';'+str(gpsd.fix.latitude)+';'+str(gpsd.fix.longitude)+';'+str(gpsd.fix.altitude)
                #print data
                #write_csv(data)

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
                print gpsd.fix.latitude
                print 'GPS looking for satellite'
                print '----------------------------------------'
                countloop += 1
                time.sleep(5)
        keep_result(nid, 'datetime', gpsd.utc)
        keep_result(nid, 'gps1', gpsd.fix.latitude)
        keep_result(nid, 'gps2', gpsd.fix.longitude)
        keep_result(nid, 'gps3', gpsd.fix.altitude)
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()  # wait for the thread to finish what it's doing

        ser.flushInput()
        ser.flushOutput()

        # ser.close()
        print "Done.\nExiting."

        return GPSPosition(gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.utc)


    ##
    # Get values form probes
    #
    def getProbesValues(self):
        last_question = False
        correction = 'False'
        array_qr = ''
        if 'correction' in request.GET:
            correction = request.GET.get('correction')

        stotal = len(sensors)

        if int(num) == stotal + 1:
            array_qr = []
            for ns in range(1, stotal + 1):
                print ns
                temp_array = []
                s = sensors[int(ns) - 1][0]
                temp_array.append(ns)
                temp_array.append(s)
                r1 = Reponses.objects.get(titre=nid)
                exec "r = r1.s" + str(ns) in globals(), locals()
                temp_array.append(r)
                array_qr.append(temp_array)
            last_question = True
            snext = '../../../outro/' + nid + '/' + lg
            return render_to_response('sonde.html',
                                      {'sensor': array_qr, 'sact': 'X', 'snext': snext, 'stotal': stotal, 'etape': 'X',
                                       'txt': txts, 'last_question': last_question})

        else:
            if correction == 'False':
                snext = str(int(num) + 1) + '?etape=1'
            else:
                snext = str(stotal + 1)

            etape = int(request.GET.get('etape'))

            if etape == 1:

                return render_to_response('sonde.html',
                                          {'sensor': sensors[int(num) - 1][0], 'sact': num, 'snext': snext,
                                           'stotal': stotal, 'etape': etape, 'txt': txts,
                                           'last_question': last_question, 'correction': correction})
            elif etape == 2:
                if sensors[int(num) - 1][0] == 'TEMPERATURE':
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
                            temp_string = lines[1][equals_pos + 2:]
                            temp_c = float(temp_string) / 1000.0
                            # temp_f = temp_c * 9.0 / 5.0 + 32.0
                            # return temp_c, temp_f
                            return temp_c

                    line = read_temp()
                    # write_csv(str(line))
                    keep_result(nid, 's' + num, str(line))
                    print line
                else:
                    channelselect(sensors[int(num) - 1][1])
                    port(None)

                    ser.write("L1\r")
                    ser.write("C\r")
                    line = ""
                    countloop = 0
                    while True:
                        data = ser.read()
                        if (data == "\r"):
                            # waiting_room()
                            # treat_results(sensor,line)
                            print line
                            # write_csv(line)
                            keep_result(nid, 's' + num, str(line))
                            break
                        elif countloop > 20000:
                            print 'failed'
                            line = 'X'
                            break
                        else:
                            line = line + data
                            countloop += 1
            return {'result': line, 'sensor': sensors[int(num) - 1][0], 'sact': num, 'snext': snext,
                    'stotal': stotal, 'etape': etape, 'txt': txts, 'last_question': last_question}


sensors = [('PH', 4), ('REDOX', 5), ('CONDUCTIVITY', 7), ('DO', 6), ('TEMPERATURE', 100)]


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

        # return [A,B,C]
        #Matt: commented
        # GPIO.output(16,A) #S2
        # GPIO.output(18,B) #S1
        # GPIO.output(22,C) #S0