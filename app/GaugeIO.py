from pytz import timezone
from math import ceil
from time import time, sleep
from serial import Serial
from os.path import join
from datetime import datetime


# Path to sensor
maxWait = 3 # Seconds to wait for first sample
serialDevice = '/dev/ttyS0'
samplingResolution = 10 # Seconds
dataResolution = 10*60 # Seconds
dataFolder = 'data' # Folder to store daily raw data files in
dataTimeZone = timezone('Etc/GMT-1') # Timezone is assumed sampled in


def record(portName):
    # Make serial object
    ser = Serial(portName, 9600, 8, 'N', 1, timeout=1)

    # Wait for initial read before proceeding
    timeStart = time()
    while ser.inWaiting() < 6:
        if time() - timeStart > maxWait:
            raise ValueError('Max initial wait exceeded.')
        sleep(0.1)

    # Main loop for data recording
    while 1:
        try:
            if ser.inWaiting() > 5:
                # Get all new data
                newData = ser.read(ser.inWaiting()).decode('utf-8')

                # Search for latest complete recording
                idx = 1
                while idx < 14:
                    if newData[-idx] == 'R' and -idx + 5 < 0:
                        curLevel = newData[-idx + 1 : -idx + 5]
                        break

                    idx += 1

                # Convert from mm to m
                curLevel = int(curLevel)/1000

                # Pretty print
                now = datetime.now(dataTimeZone)
                print('Time: {}, Level: {} m'.format(now.strftime('%Y/%m/%d %H:%M:%S'), curLevel), end='\r')

                # Log to file
                dataFile = join(dataFolder, '{}.txt'.format(now.strftime('%Y%m%d')))
                addToFile(dataFile, '{}, {}'.format(now, curLevel))

        except ValueError:
            continue

        # Sleep till a new sample is called for by samplingResolution parameter
        timeToSleep = int(ceil(time()/samplingResolution))*samplingResolution - time()
        sleep(timeToSleep)

    ser.close()


def addToFile(file, content):
    with open(file, 'a') as fo:
	fo.write('{}\n'.format(content)) 


record(serialDevice)
