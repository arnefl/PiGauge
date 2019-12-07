# PiGauge
PiGauge is a project to remotely monitor the water level of rivers and report it to the Nessie database. 


## Hardware:
- Raspberry Pi 4 Model B, 2GB RAM
- MaxBotix MB7380 HRXL-MaxSonar-WRT
- SIM7600E-H 4G
- Buck converter DC 12V to 5V 10A
- TODO: Charge controller
- TODO: Solar panel
- TODO: Battery
- TODO: Locker


## Software
- NOOBS 3.2.1
- Python 3.7
	- NumPy, Pandas, PyYAML, pytz, pySerial, datetime, Requests
- OpenSSH server
- TODO: Networking

See docs/setup.md for details on the build.


## Setting up a new gauge
1. Update configuration, config.yml.
2. 