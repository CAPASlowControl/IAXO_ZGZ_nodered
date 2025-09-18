IAXO ZGZ nodered
===
***

This repository includes the nodered flows of the IAXO Zgz detector.

The repository is installed in `/home/iaxo/.node-red/`.

Functionalities or code that need To Be Checked is marked as (<mark>TBC</mark>).

# Flows

The code is composed of the following flows:

 - Bronkorst:
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
 - Thyracont Pressure Sensor
	+ Pressure Outlet Sensor 
	+ Thyracont VSR53USB
	+ SerialPort `dev/THYU0` 

	
 - PLC Operation & Status
	+ PLC with outlet pressure sensors
		+ Recirculation and vacuum pressure (<mark>TBC</mark>)
	* Open / Close ElectroValves
	* Communication using mqtt
	
 - PLC_REC
	 + Moisture Analyzer 
		 * MZD SMART-MT20
	 + Oxygen Analyzer
		 * Southland Sensing EMD-485-X-T-TO2-1x-6
	 + Recirculation Pressure  (<mark>TBC</mark>)
	 + Recirculation ElectroValves (<mark>TBC</mark>)
     + Using an Idustrial Shield PLC (Arduino based)
	 + SerialPort `dev/PLC_REC` 
 - CAEN 
 	 + High Voltage Power Supply (HVPS) for TPC
 	 	+ Cathode: *channel0* 
 	 	+ Mesh:  *channel1*
 	 + CAEN N1471HA
	 + SerialPort `dev/CAEN0` 

 - RIGOL  (<mark>TBC</mark>)
	 + SerialPort `dev/RIGOL` 

 - BGA 
	 + Measures gas mixture ratio
	 + Standfor Research Systems (SRS) BGA 244 HP
	 + SerialPort `dev/BGA` 

 
 - Security
 	- <mark>TBC</mark>: Security code should be checked carefully.
 	- The Errors Shutdown ElectroValves and CAEN PS.
 	- Two modes are stablished: *normal* with security and *filling*with relaxed security.
	- <ins>Normal Mode</ins>:
		1. OverPressure: Outlet Pressure (Thyracont) > 1450 mBa
	- <ins>Normal Mode: </ins>
		1. OverPressure:
			- Outlet Pressure (Thyracont) > 1450 mBar
		    - Outlet Measure (Thyracont)> SetPoint (BRKPR)+ 40 mBar
		1. Gass Loss:
			- Flow out Meas (BRKM1)> Flow In Set (BRKFL)
				- Additionally if `(pout (thyracont)-100) < pcrl (BRKPR))` gas preesure error.
		1. Pressure
			- Thyracont Connection error (<mark>TBC</mark>)
			- Pressure error `(Pin (PLC)> (PCtrl_out (BRKPR)+60))`then error.
		1. Flow
			- OutFlow Connection error. (<mark>TBC</mark>) 


 - Database
	 + Postgressql Database
	 + Database: *iaxod0slowctldb*
	 + User: *iaxo*
	 + Password: *bujaruelo*
	 
 - OPC UA
	 + OPCUA server with nodered variables for communication with Desy
	 + Database: *opc.tcp://127.0.0.1:55480*
	 + User: *iaxo*
	 + Password: *bujaruelo*
	 

 


# NODERED NOTES

## Memory Leaks
Nodered is prone to memory leaks. 

To avoid memory leaks it is important to avoid errors in the code. In serial ports it is important to:

 - Check the status of the response from the serial port and filter the message only when the `msg.status` is  `OK`.
 - Send messages to the serialport only when the port is connected
	 + If messages are always sent nodered is not able to reconnect upon a communication error.

## USB Configuration
The serialport configuration is included in `/etc/udev/rules.d/99-sub-serial.rules

For information on the serial ports  `devadm info --name=/dev/<device>`

## Credentials
Credentials are set in `settings.js`.

Credentials are encryptes usin `node-red admin hash-pw`.

# TODO LIST

- Review Security Flow
- Migrate Slack messages to Mattermost

