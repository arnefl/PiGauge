from pytz import timezone
from math import ceil
from time import time, sleep
from serial import Serial
from os.path import join
from datetime import datetime
from Configuration import Configuration


# Load configuration
config = Configuration()

# Path to sensor
max_wait = 3 # Seconds to wait for first sample
time_zone = timezone(config['sampling']['time_zone'])


def record(port_name):
    # Make serial object
    ser = Serial(port_name, 9600, 8, 'N', 1, timeout=1)

    # Wait for initial read before proceeding
    time_start = time()
    while ser.inWaiting() < 6:
        if time() - time_start > max_wait:
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

                # Invert height, and convert from mm to m
                curLevel = (config['sampling']['ground_to_device'] - int(curLevel))/1000

                # Pretty print
                now = datetime.now(time_zone)
                print('Time: {}, Level: {} m'.format(now.strftime('%Y/%m/%d %H:%M:%S'), curLevel), end='\r')

                # Log to file
                dataFile = join(config['sampling']['data_folder'], '{}.txt'.format(now.strftime('%Y%m%d')))
                addToFile(dataFile, '{}, {}'.format(now, curLevel))

        except ValueError:
            continue

        # Sleep till next time to sample
        sres = config['sampling']['resolution']
        timeToSleep = int(ceil(time()/sres))*sres - time()
        sleep(timeToSleep)

    ser.close()


def addToFile(file, content):
    with open(file, 'a') as fo:
        fo.write('{}\n'.format(content))


record(config['sampling']['serial_device'])
