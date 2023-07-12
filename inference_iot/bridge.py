import serial
import serial.tools.list_ports
import configparser
import requests
from snapshot import take_photo
from Roboflow_inference import prediction
import time



#controlla se take_photo e prediction sono eseguiti quando arriva il pacchetto da arduino e correggi il codice


class Bridge():
	
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.ini')
		self.setupSerial()
	#controlla se la porta seriale è disponibile

	def setupSerial(self):
		# open serial port
		self.ser = None

		if self.config.get("Serial","UseDescription", fallback=False):
			self.portname = self.config.get("Serial","PortName", fallback="COM3")
		else:
			print("list of available ports: ")
			ports = serial.tools.list_ports.comports()

			for port in ports:
				print (port.device)
				print (port.description)
				if self.config.get("Serial","PortDescription", fallback="arduino").lower() \
						in port.description.lower():
					self.portname = port.device

		try:
			if self.portname is not None:
				print ("connecting to " + self.portname)
				self.ser = serial.Serial(self.portname, 9600, timeout=0)
		except:
			self.ser = None
		

		# internal input buffer from serial
		self.inbuffer = []

	def loop(self):
	# infinite loop for serial managing
		while True:
			#variable for duration of the loop
			start_time = time.time()
			# check if serial port is still available
			if self.ser is None or not self.ser.is_open:
				self.setupSerial()

			# look for a byte from serial
			# if self.ser.in_waiting > 0:
			# 	# data available from the serial port
			# 	lastchar = self.ser.read(1)

			# 	if lastchar == b'\xfe': # EOL
			# 		print("\nValue received")              
			# 		take_photo()
			# 		print('take image')
			# 		prediction()
			# 		print('data posted')
			# 		self.useData()
			# 		self.inbuffer = []
			# 	else:
			# 		# append
			# 		self.inbuffer.append(lastchar)

			# look for a byte from serial
			if self.ser.in_waiting > 1:  # <-- changed condition here
            # data available from the serial port
				lastchar = self.ser.read(2)  # <-- read two bytes
		
				if lastchar == b'\xff\xfa':  # <-- check for previous byte
					if lastchar[-1] == b'\xfe': # check for last byte
						print("\nValue received")
						take_photo()
						print('take image')
						prediction()
						print('prediction done')	
						print('json done')
						self.useData()
						self.inbuffer = []
					else:
						# append
						self.inbuffer.append(lastchar[-1])
				else:
					# append both bytes to buffer
					self.inbuffer.extend(lastchar)

				end_time = time.time()
				duration = end_time - start_time
				print("Duration: {:.2f} seconds".format(duration))

	def useData(self):
		# I have received a packet from the serial port. I can use it
		if len(self.inbuffer)<3:   # at least header, size, footer
			return False
		# split parts
		if self.inbuffer[0] != b'\xff':
			return False
		numval = int.from_bytes(self.inbuffer[1], byteorder='little')
		for i in range(numval):
				print(i)

if __name__ == '__main__':
    br = Bridge()
    br.loop()
    