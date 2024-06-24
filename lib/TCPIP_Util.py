import pyvisa
import time
#pip install PyVISA
#pip install PyVISA-py

class TCPIP_CMD(object):
	def __init__(self, _ip, _port):
		self._ip = _ip
		self._port = _port
		self.rm = pyvisa.ResourceManager()
		self.my_inst = None
	
	def connect(self):
		try:
			# Open connection to instrument
			self.my_inst = self.rm.open_resource(f"TCPIP::{self._ip}::{self._port}::SOCKET")
			print(f"Connected to chamber at {self._ip}")
		except Exception as e:
			print(f"Error connecting to chamber at {self._ip}: {e}")
	
	def write(self, command):
		try:
			# Write command to instrument
			if self.my_inst:
				self.my_inst.write(command)
				print(f"Sent command: {command}")
			else:
				print("Error: Instrument connection not established.")
		except pyvisa.errors.VisaIOError as e:
			print(f"Error writing command: {e}")
	
	def read(self):
		try:
			# Read data from instrument
			if self.my_inst:
				data = self.my_inst.query_ascii_values("DATE?\n\r", delay=5)  # Example command to read data  #query_ascii_values
				#self.my_inst.write("DATE?\n\r")
				#data = self.my_inst.read()
				print(f"Received data: {data}")
				return data
			else:
				print("Error: Instrument connection not established.")
				return None
		except pyvisa.errors.VisaIOError as e:
			print(f"Error reading data: {e}")
			return None

if __name__ == "__main__":
	
	rm = pyvisa.ResourceManager()
	instrument = rm.open_resource("TCPIP::192.168.1.4::57732::SOCKET")

	instrument.write("DATE?")
	date = instrument.read_bytes(10)
	print(date)

	time.sleep(1)

	instrument.write("TIME?")
	time = instrument.read_bytes(10)
	print(time)

	instrument.write("TEMP?")
	temp = instrument.read_bytes(23)
	print(temp)

	instrument.write("HUMI?")
	humi = instrument.read_bytes(13)
	print(humi)

	# MON? <Temp now, Humi now, Op State>
	instrument.write("MON?")
	mon = instrument.read_bytes(15)
	print(mon)

	instrument.write("PRGM MON?")
	prgm_mon = instrument.read_bytes(20)
	print(prgm_mon)

	###instrument.write("MODE, OFF")