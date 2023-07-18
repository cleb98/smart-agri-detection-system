import serial
import serial.tools.list_ports
import configparser

from utils import take_photo, prediction, send_prediction, empty_folders, checkInfectedMicrocontrollers, set_micro_light



import time


class Bridge():

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('config.ini')
		self.setupSerial()

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
		#
		while (True):
			# attuazione
			# check if micro_id is in infected list from check routine 1
			# funzione in utils che se ritorna a true si invia un pacchetto seriale al microcontrollore per accendere il led
			mic_state = checkInfectedMicrocontrollers() #assegno vero se la varibile è presente nella lista 
			set_micro_light(mic_state, self.ser) #accendo il led se mic_state è True
				
			#poi si fa la lettura del seriale per vedere le foto ricevute
			#look for a byte from serial
			if not self.ser is None:

				if self.ser.in_waiting>0:
					# data available from the serial port
					lastchar=self.ser.read(1)

					if lastchar==b'\xfe': #EOL
						print("\nValue received")
						self.useData()
						self.inbuffer = []
					else:
						# append
						self.inbuffer.append(lastchar)

	def useData(self):

				
		if len(self.inbuffer)<2:   # at least 2 bytes
			return False
		
		# split parts
		if self.inbuffer[0] != b'\xff':
			return False
														
		if self.inbuffer[1] != b'\xfa':
			return False
		else:
			
			print(self.inbuffer)
			start_time = time.time()

			print('take a photo!')
			take_photo()
			print('make prediction!')
			data = prediction()
			response = send_prediction(data)
			if response == 200:
				print('data sent!')
			print('empty folders!')
			empty_folders()

			end_time = time.time()
			elapsed_time = end_time - start_time
			print(f"Code took {elapsed_time} seconds to execute.")	



if __name__ == '__main__':

	br = Bridge()
	br.loop()

