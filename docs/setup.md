# PiGauge

## Installation
1. Setting up a Raspberry Pi 4b
1.1 Install NOOBS on a Raspberry Pi4b. Name your user `pi`
1.2 /dev/ttyS0 is owned by root and dialout, give access to our user.
  ```
  sudo usermod -a -G dialout $USER
  ```
  Note: Sometimes you might end up in a race condition with the system. In that case, the group owner will be tty. Sudo raspi-config and disable, reboot, enable, and reboot helps.
  
  Test with minicom, if you'd like:
  ```
  minicom -b 9600 -o -D /dev/ttyS0
  ```


### Raspberry Pi
1. Pin Layout
| Attach to | Function | Pin # | Pin # | Function | Attach to  |
|-----------|----------|:-----:|:-----:|----------|------------|
| Fan V+    | 3V3      |   1   |   2   | 5V       | PSU V+     |
|           |          |   3   |   4   | 5V       | Sensor V+  |
|           |          |   5   |   6   | GND      | Sensor GND |
|           |          |   7   |   8   | TXD1     |            |
| Fan GND   | GND      |   9   |   10  | RXD1     | Sensor RX  |
|           |          |   11  |   12  |          |            |
|           |          |   13  |   14  | GND      | PSU GND    |
|           |          |   15  |   16  |          |            |
| Sim V+    | 3V3      |   17  |   18  |          |            |
|           |          |   19  |   20  | GND      | Sim GND    |
| Sim RX    | RXD4     |   21  |   22  |          |            |
|           |          |   23  |   24  | TXD4     | Sim TX     |
|           | GND      |   25  |   26  |          |            |
|           |          |   27  |   28  |          |            |
|           |          |   29  |   30  | GND      |            |
|           |          |   31  |   32  |          |            |
|           |          |   33  |   34  | GND      |            |
|           |          |   35  |   36  |          |            |
|           |          |   37  |   38  |          |            |
|           |          |   39  |   40  |          |            |