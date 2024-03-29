# PiGauge

## Installation

## Raspberry Pi
1. Setting up a Raspberry Pi 4b
2. Install NOOBS on a Raspberry Pi4b. Name your user `pi`
3. We need to enable serial data
	```
	sudo nano /boot/config.txt
	```
	and, to end of file, add
	```
	enable_uart=1
	dtoverlay=uart4
	dtoverlay=pi4-disable-bt
	dtoverlay=pi4-miniuart-bt
	```
	Check that SPI is disabled (has conflict with uart4):
	```
	dtparam=spi=off
	```

4. Serial devices are owned by root and dialout, give access to our user.
 	```
 	sudo usermod -a -G dialout $USER
 	```
	Note: Sometimes you might end up in a race condition with the system. In that case, the group owner will be tty (check with `ls -l /dev/ttyS0`). Sudo raspi-config and disable, reboot, enable, and reboot helps.
  
Test connection to sensor:
	```
	sudo apt-get install minicom
	minicom -b 9600 -o -D /dev/ttyAMA1
	```




## Assembly
1. GPIO pin layout on Raspberry Pi

| Attach to | Function | Pin # | Pin # | Function | Attach to  |
|-----------|----------|:-----:|:-----:|----------|------------|
| Fan V+    | 3V3      |   1   |   2   | 5V       | PSU V+     |
|           |          |   3   |   4   | 5V       | Sim V+     |
|           |          |   5   |   6   | GND      | Sim GND    |
|           |          |   7   |   8   | TXD1     | Sim RXD    |
| Fan GND   | GND      |   9   |   10  | RXD1     | Sim TXD    |
|           |          |   11  |   12  |          |            |
|           |          |   13  |   14  |          |            |
|           |          |   15  |   16  |          |            |
| Sensor V+ | 3V3      |   17  |   18  |          |            |
|           |          |   19  |   20  | GND      | PSU GND    |
| Sensor RX | RXD4     |   21  |   22  |          |            |
|           |          |   23  |   24  | TXD4     |            |
| Sensor GND| GND      |   25  |   26  |          |            |
|           |          |   27  |   28  |          |            |
|           |          |   29  |   30  | GND      |            |
|           |          |   31  |   32  |          |            |
|           |          |   33  |   34  | GND      |            |
|           |          |   35  |   36  |          |            |
|           |          |   37  |   38  |          |            |
|           |          |   39  |   40  |          |            |
