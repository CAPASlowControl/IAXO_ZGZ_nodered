IAXO ZGZ nodered
===
***

This repository includes the nodered flows of the IAXO Zgz detector.

The repository is installed in `/home/iaxo/.node-red/`.

Functionalities or code that need To Be Checked is marked as (<mark>TBC</mark>).

# Flows

The code is composed of the following flows:

 - **Bronkorst**
	 + Pressure controler
		 * Placed at the line output
		 * Bronkhorst P-702CV-MBD-33-V
		 * SerialPort `dev/BRKPR`
	 + Inlet Flow Controller
	 	 * Placed at the line inlet
	 	 * Bronkhorst F-201CV-200-MGD-33-V
	 	 * SerialPort `dev/BRKFL`
	 	 
	 + Outlet Flow Controller 
	  	 * Placed at the line outlet
	 	 * Bronkhorst F-201CB-ABD-00-V
	 	 * SerialPort `dev/BRKM1`
	 + Flow Sensor 
 	 	 * Placed after the inlet flow contoller
	 	 * Bronkhorst D6310-HGD-BB-AV-99-0-S
	 	 * SerialPort `dev/BRKM0` 
 - **Thyracont Pressure Sensor**
	+ Pressure Outlet Sensor 
	+ Thyracont VSR53USB
	+ SerialPort `dev/THYU0` 

	
 - **PLC Operation & Status**
	+ PLC with outlet pressure sensors
		+ Recirculation and vacuum pressure (<mark>TBC</mark>)
	* Open / Close ElectroValves
	* Communication using mqtt
	
 - **PLC_REC**
	 + Moisture Analyzer 
		 * MZD SMART-MT20
	 + Oxygen Analyzer
		 * Southland Sensing EMD-485-X-T-TO2-1x-6
	 + Recirculation ElectroValves (<mark>TBC</mark>)
     + Using an Idustrial Shield PLC (Arduino based)
     + 
	 + SerialPort `dev/PLC_REC` 
 - **CAEN** 
 	 + High Voltage Power Supply (HVPS) for TPC
 	 	+ Cathode: *channel0* 
 	 	+ Mesh:  *channel1*
 	 + CAEN N1471HA
	 + SerialPort `dev/CAEN0` 

 - **RIGOL**
     + Voltage supply for DAQ (feminos and TCM boards)
	 + RIGOL DP811A
	 + SerialPort `dev/RIGOL` 

 - **BGA** 
	 + Measures gas mixture ratio
	 + Standfor Research Systems (SRS) BGA 244 HP
	 + SerialPort `dev/BGA` 

 
 - **Security**
 	- <mark>TBC</mark>: Security code should be checked carefully.
 	- The Errors Shutdown ElectroValves and CAEN PS.
 	- The errors/warnings send a message to mattermost, to nodered debug and to Security tab in the ui.
 	- Two modes are stablished: *normal* with security and *filling* with relaxed security.
	- <ins>Filling Mode</ins>:
		1. OverPressure: Outlet Pressure (Thyracont) > 1500 mBar
	- <ins>Normal Mode: </ins>
		1. Outlet Pressure (Thyracont) > 1450 mBar
		1. Outlet Pres. Measure (Thyracont)> SetPoint (BRKPR)+ 40 mBar
	 	1. Flow out Meas (BRKM1)< Flow In Set (BRKFL) - 0.1 l/h
 	
 - **Database**
	 + Postgressql Database
	 + Database: *iaxod0slowctldb*
	 + User: *iaxo*
	 + Password: *bujaruelo*
	 
 - **OPC UA**
	 + OPCUA server with nodered variables for communication with Desy
		 * The OPCUA server does not run if nodered is run with the user `iaxo`. But run correctly with users `root` or `desy`. 
		 * Therefore Nodered is run with user `root` in the `systemctl`service.
	 + Server: *opc.tcp://127.0.0.1:55480*
	 + There is an user with ports open for connection from Desy:
		 * user: *desy*
		 * password: *BbyIAXOCollab2025!*

 
# Operation Notes

The operational conditions may vary with the experiment.

Notes for operation on 22/09/2025:

* Pressure: ~1.4 bar
* Flow:
	- 2 l/h
	- up to 6 l/h during filling
* BGA:
	- 99% Ze - 1% Isobutane (depending on the mixture)
* Humidity
	- 7 ppm
* LVPS (RIGOL):
 	-  5.2 V / 5.5 A
* HVPS (CAEN):
	- 850 V cathode
	- 350 V mesh
	- 0.2 uA Current (trip)
		+ If IMRange=LOW the maximum current is 2 uA.
		+ If IMRange=HIGH the maximum current is 20 uA
	 	
- Shutdown Gas:
	+ Close EV
	+ Close manual valves after EV
	+ Close Inlet and outlet valves


# NODERED NOTES

## Memory Leaks
Nodered is prone to memory leaks. 

To avoid memory leaks it is important to avoid errors in the code.

In **serial ports** it is important to:

 - Check the status of the response from the serial port and filter the message only when the `msg.status` is  `OK`.
 - Send messages to the serialport only when the port is connected
	 + If messages are always sent nodered is not able to reconnect upon a communication error.
	 
In **Databases** (or in **join** nodes):

 - It is important that in a join node all input messages are sent. If a device is disconnected but a node keeps input to join (e.g. TableName) there may be a memory leak.


## USB Configuration
The serialport configuration is included in `/etc/udev/rules.d/99-usb-serial.rules

For information on the serial ports  `devadm info --name=/dev/<device>`

For reloading the rules:

```
	sudo udevadm control --reload-rules
  	sudo udevadm trigger
```

## Credentials
Credentials are set in `settings.js`.

Credentials are encrypted usin `node-red admin hash-pw`.

# TODO LIST

- Review Security Flow
	+ Check operation with new security flow.
- Check Reconnection:
	+ The serial devices sometimes reconnect and sometimes not.
- Check baud rates:
	- CAEN: 115200 (maximum)
	- Bronkhorst: 38400 (default)
	- Others (Rigol, BGA, PLC_REC) at 9600


