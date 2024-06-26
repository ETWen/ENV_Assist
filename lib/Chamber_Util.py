import time
import pyvisa
import re
import matplotlib.pyplot as plt


dbg_dly = 5

class ChamberCmd(object):
	def __init__(self,_ip,_port):
		self._ip = _ip
		self._port = _port
		self.rm = pyvisa.ResourceManager()
		self.my_inst = None
		self.flag_connect = False

	def connect(self):
		try:
			# Open connection to instrument
			self.my_inst = self.rm.open_resource(f"TCPIP::{self._ip}::{self._port}::SOCKET")
			print(f"Connected to chamber at {self._ip}")
			self.flag_connect = True
			return self.flag_connect
		except Exception as e:
			print(f"Error connecting to chamber at {self._ip}: {e}")
			self.flag_connect = False
			return self.flag_connect

	def disconnect(self):
		try:
			if self.my_inst:
				self.my_inst.close()
				print(f"Disconnected from chamber at {self._ip}")
				self.flag_connect = False
				return self.flag_connect
		except Exception as e:
			print(f"Error disconnecting from chamber at {self._ip}: {e}")

	def CheckConnection(self):
		try:
			status = self.myQuery("ROM?")
			if status == "123":
				return True
			else:
				return False
		except Exception as e:
			print(f"An error occurred while checking chamber connection: {e}")
			return False

	def write(self, command):
		try:
			# Write command to instrument
			if self.my_inst:
				self.my_inst.write(command)
				#print(f"Sent command: {command}")
			else:
				print("Error: Instrument connection not established.")
		except pyvisa.errors.VisaIOError as e:
			print(f"Error writing command: {e}")

	def read_until_terminator(self, terminator='\r\n'):
		try:
			if self.my_inst:
				response = bytearray()
				while True:
					byte = self.my_inst.read_bytes(1)
					response.extend(byte)
					if response.endswith(terminator.encode()):
						break
				return response.decode().strip()
			else:
				print("Error: Instrument connection not established.")
				return None
		except pyvisa.errors.VisaIOError as e:
			print(f"Error reading data: {e}")
			return None

	def myQuery(self, command):
		try:
			self.write(command)
			response = self.read_until_terminator()
			if response is None:
				raise ValueError("No response received")
			return response
		except (pyvisa.errors.VisaIOError, ValueError) as e:
			print(f"Error during query '{command}': {e}")
			return None

	def GetChbTime(self):
		#time.sleep(dbg_dly)
		date = self.myQuery("DATE?")
		if date is None:
			print("Error: DATE? query returned None")
			return None
		
		#time.sleep(dbg_dly)
		time_r = self.myQuery("TIME?")
		if time_r is None:
			print("Error: TIME? query returned None")
			return None
		try:
			year, month_day = date.split('.')
			month, day = month_day.split('/')
			year = "20" + year
			Chb_time = f"{year}-{month.zfill(2)}-{day.zfill(2)} {time_r}"
		except ValueError as e:
			print(f"Error parsing date: {date} or time: {time_r} - {e}")
			Chb_time = None
			
		return Chb_time

	def GetCondition(self):
		try:
			mon = self.myQuery("MON?")
			#print(f"Monitor: {mon}")
			# Parse the response
			mon_parts = mon.split(',')
			if len(mon_parts) == 4:
				return [mon_parts[0], mon_parts[1], mon_parts[2], mon_parts[3]]
			elif len(mon_parts) == 3:
				return [mon_parts[0], 'NA', mon_parts[1], mon_parts[2]]
			else:
				print(f"Unexpected MON response format: {mon}")
				return []
		except Exception as e:
			print(f"An error occurred in GetCondition: {e}")
			return []

	def GetProgStat(self):
		try:
			prgm_mon = self.myQuery("PRGM MON?")	   #1,50.0,5,1:54,0,0
			prgm_set_parts = prgm_mon.split(',')
			#print(f"Program Monitor: {prgm_mon}")
			return prgm_set_parts
		except Exception as e:
			print(f"An error occurred in GetProgStat: {e}")
			return None

	def GetProgSet(self):
		try:
			prgm_set = self.myQuery("PRGM SET?")
			rm_data, data = prgm_set.split(':')
			prgm_set_parts = data.split(',')
			#print(f"Program Setting: {prgm_set}")
			return prgm_set_parts
		except Exception as e:
			print(f"An error occurred in GetProgSet: {e}")
			return None

	def GetProgInfo(self, PGM_Num):
		prgm_data = self.myQuery(f"PRGM DATA?, RAM:{PGM_Num}")
		#print(prgm_data)
		if prgm_data == "NA:DATA NOT READY":
			return prgm_data, prgm_data
		else:
			prgm_data_parts = prgm_data.split(',')
			prgm_stp_lst = []
			for step_num in range( int(prgm_data_parts[0]) ):
				step_num +=1
				prgm_data_stp = self.myQuery(f"PRGM DATA?, RAM:{PGM_Num}, STEP{step_num}")
				prgm_stp_lst.append(prgm_data_stp)
				#print(prgm_data_stp)
			return prgm_data_parts, prgm_stp_lst

	def ParseProgInfo(self,data):
		temp_values = []
		humi_values = []
		cumulative_time = []
		total_minutes = 0

		for line in data:
			parts = line.split(',')
			if len(parts) >= 5:
				temp = float(parts[1].replace("TEMP", ""))
				humi = parts[3].replace("HUMI", "").strip()
				if humi == "OFF":
					humi = None
				else:
					humi = float(humi)
				
				time_part = re.search(r'TIME(\d+:\d+)', line).group(1)
				hours, minutes = map(int, time_part.split(':'))
				total_minutes += hours * 60 + minutes
				total_hours = total_minutes / 60
				
				temp_values.append(temp)
				humi_values.append(humi)
				cumulative_time.append(total_hours)
		return temp_values, humi_values, cumulative_time

	def PlotProgProfile(self,PGM_Num,PGM_Name,data):
		temp_values, humi_values, cumulative_time = self.ParseProgInfo(data)
		
		# Add origin point with the same values as the first data point
		temp_values.insert(0, temp_values[0])
		humi_values.insert(0, humi_values[0])
		cumulative_time.insert(0, 0)
		steps = range(0, len(temp_values))

		print(f"ProgProfile Temp : {temp_values}")
		print(f"ProgProfile Humi : {humi_values}")

		# Create a figure with two subplots (2 rows, 1 column)
		fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
		
		# Create twin axes for steps
		twin_ax1 = ax1.twiny()
		twin_ax2 = ax2.twiny()
		
		# Plotting temperature on the first subplot
		ax1.plot(cumulative_time, temp_values, marker='o', linestyle='-', color='b', label='Temperature')
		ax1.set_ylabel('Temperature (°C)')
		ax1.set_xlim(0)  # Set Y axis limits for temperature
		ax1.set_ylim(-50, 75)  # Set Y axis limits for temperature
		ax1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
		ax1.xaxis.set_major_locator(plt.MultipleLocator(0.5))
		ax1.legend()
		
		twin_ax1.set_xlim(ax1.get_xlim())
		twin_ax1.set_xticks(cumulative_time)
		twin_ax1.set_xticklabels(steps)
		twin_ax1.set_xlabel('Steps')

		# Plotting humidity on the second subplot
		humi_cumulative_time = [time for time, humi in zip(cumulative_time, humi_values) if humi is not None]
		humi_values_filtered = [humi for humi in humi_values if humi is not None]
		ax2.plot(humi_cumulative_time, humi_values_filtered, marker='o', linestyle='-', color='g', label='Humidity')
		ax2.set_xlabel('Cumulative Time (hr)')
		ax2.set_ylabel('Humidity (%)')
		ax2.set_xlim(0)  # Set Y axis limits for temperature
		ax2.set_ylim(0, 100)  # Set Y axis limits for humidity
		ax2.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
		ax2.xaxis.set_major_locator(plt.MultipleLocator(0.5))
		ax2.legend()
		
		twin_ax2.set_xlim(ax2.get_xlim())
		twin_ax2.set_xticks(cumulative_time)
		twin_ax2.set_xticklabels(steps)
		twin_ax2.set_xlabel('Steps')

		# Set the window title after calling plot function
		plt.gcf().canvas.manager.set_window_title(f"PGM : {PGM_Num} {PGM_Name}")

		# Adjust layout and show the plot
		fig.tight_layout()
		plt.show()

	def SetProgRun(self,PGM_Num):
		#cmd = (f"PRGM, RUN, RAM:{PGM_Num}, STEP:{STP_Num}")
		cmd = (f"MDOE, RUN, PTN{PGM_Num}")
		#self.write(cmd)
		print(cmd)
		return

	def SetProgPause(self,PGM_Num):
		cmd = self.myQuery("PRGM, PAUSE")
		#self.write(cmd)
		print(cmd)
		return

	def SetConstTempRun(self,const_temp):
		cmd = (f"TEMP, S{const_temp}")
		print(cmd)
		return

	def SetConstHumiRun(self,const_humi):
		cmd = (f"HUMI, S{const_humi}")
		print(cmd)
		return

	def Read_Chamber_Temp(self):
		temp = self.myQuery("TEMP?")
		temp_parts = temp.split(',')
		#print(f"Temperature: {temp}")
		return temp_parts

	def Read_Chamber_Humi(self):
		humi = self.myQuery("HUMI?")
		try:
			humi_parts = humi.split(',')
			return humi_parts
		except Exception as e:
			print("No Humidity functionality available.")
			return ['NA', 'NA', 'NA', 'NA']

	def Read_Chamber_Mode(self):		#OFF/STANDBY/CONSTANT/RUN
		mode = self.myQuery("MODE?")
		#print(f"Mode: {mode}")
		return mode

	def Read_Chamber_Mon(self):
		mon = self.myQuery("MON?")
		# Parse the response
		mon_parts = mon.split(',')
		if len(mon_parts) == 4:
			return [mon_parts[0], mon_parts[1], mon_parts[2], mon_parts[3]]
		elif len(mon_parts) == 3:
			return [mon_parts[0], 'NA', mon_parts[1], mon_parts[2]]
		else:
			print(f"Unexpected MON response format: {mon}")
			return []

	def Read_Chamber_PRGM_Mon(self):				#Return the state when program is opreating 
		prgm_mon = self.myQuery("PRGM MON?")		#1,50.0,5,1:54,0,0
		prgm_set_parts = prgm_mon.split(',')
		#print(f"Program Monitor: {prgm_mon}")
		return prgm_set_parts



if __name__ == "__main__":
	instrument = ChamberCmd("192.168.1.5", "57732")
	instrument.connect()

	date = instrument.myQuery("DATE?")		#24.06/19
	print(f"Date: {date}")

	'''
	instrument.write("prgm data write,pgm31,edit start")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,step1,temp20.0,time0:05,grantyon")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,step2,grantyoff,trampon,temp-40.0,time1:10")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,step3,trampoff,grantyon,temp-40.0,time0:10")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,step4,grantyoff,trampon,temp100.0,time1:15")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,step5,trampoff,grantyon,temp100.0,time0:10")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,name,test")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,end,standby")
	time.sleep(1)
	instrument.write("prgm data write,pgm31,edit end")
	time.sleep(1)
	'''
