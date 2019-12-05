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

