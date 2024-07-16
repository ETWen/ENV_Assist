import time
from datetime import datetime

# Used for GUI main.py
from lib import NuPython
from lib import nuconst


# Dbg used for NuStream_Util.py
#import NuPython
#import nuconst

class NustreamCmd(object):
	def __init__(self,_ip):
		self._ip = _ip
		self.nscmd = NuPython.NuStreamsModuleSetting()
		self.nsconst = nuconst.NuStreamsConst()
		self.flag_connect = False

	def Connect(self):
		if (self.nscmd.server_connect(self._ip)==1):
			print(f"Connected to NuStream at {self._ip}")
			self.flag_connect = True
			return self.flag_connect
		else:
			print(f"Error connecting to NuStream at {self._ip}")
			self.flag_connect = False
			return self.flag_connect

	def Disconnect(self):
		self.nscmd.port_unlock()
		time.sleep(1)
		self.nscmd.server_disconnect()
		self.flag_connect = False
		return self.flag_connect

	def CheckConnection(self):
		try:
			print(self.GetModuleSN(1))
			status = len(self.GetModuleSN(1))
			if status > 0:
				print(status)
				return True
			else:
				return False
		except Exception as e:
			print(f"An error occurred while checking NuStream connection: {e}")
			return False

	def GetModuleSN(self,boardid):
		self.nscmd.read_info_module()
		return self.nscmd.get_serialnum(boardid)

	def GetModuleName(self):
		self.module_names = {}
		self.nscmd.read_info_module()
		for idx in range(8):
			model_name = self.nscmd.get_modelname(idx+1)
			if model_name:
				self.module_names[idx+1] = model_name
		return self.module_names

	def GetMedia(self):
		model_list = self.GetModuleName()
		pidx = 0
		port_info_list = []
		while pidx < len(self.nscmd.ns_info_portlist):
			if self.nscmd.ns_info_portlist[pidx].board_id != 1 and self.nscmd.ns_info_portlist[pidx].board_id != 18:
				# Format the data as a string
				#port_info = '(%d,%d,%d) Speed:%s, Duplex:%s, AutoNegotiation:%s' % (
				port_info = '(%d,%d,%d) ' % (
					self.nscmd.ns_info_portlist[pidx].chassis_id, 
					self.nscmd.ns_info_portlist[pidx].board_id, 
					self.nscmd.ns_info_portlist[pidx].port_id, 
					#self.nscmd.get_media_speed(pidx), 
					#self.nscmd.get_media_duplex(pidx), 
					#self.nscmd.get_media_autonego(pidx)
				)
				if self.nscmd.ns_info_portlist[pidx].board_id in model_list:
					port_info += model_list[self.nscmd.ns_info_portlist[pidx].board_id]
				port_info_list.append(port_info)
			pidx += 1
		return port_info_list

	def GetPortIdx(self,cid, bid, pid):
		port_idx = self.nscmd.get_portidx(cid, bid, pid)
		return port_idx

	def SetLockPort(self,cid, bid, pid):
		self.nscmd.port_mark(cid, bid, pid)
		self.nscmd.port_lock()

	def SetUnLockPort(self):
		self.nscmd.port_unlock()

	def GetPortMediaInfo(self, port_idx):
		self.nscmd.read_info_link(port_idx)
		speed_map = {
			5: "5G",
			4: "2.5G",
			3: "10G",
			2: "1G",
			1: "100M",
			0: "10M"
		}
		speed = self.nscmd.get_media_speed(port_idx)
		speed_str = speed_map.get(speed, "Link Down")
		duplex = self.nscmd.get_media_duplex(port_idx)
		autonego = self.nscmd.get_media_autonego(port_idx)

		port_media_info = [speed_str, duplex, autonego]
		return port_media_info

	def SetPortClearCounters(self, port_idx):
		self.nscmd.clear_counter_port(port_idx)

	def SetPortTansmitConfig(self, pkt_len, utilization, xtag, smac, dmac, sip, dip, protocol):
		self.nscmd.config_stream_pktlen(pkt_len)				# Packet length
		self.nscmd.config_stream_enable_xtag(xtag)				# X-Tag
		self.nscmd.config_stream_smac(smac)					# MAC address - SA
		self.nscmd.config_stream_dmac(dmac)					# MAC address - DA
		self.nscmd.config_stream_sip(sip)					# IP address - SIP
		self.nscmd.config_stream_dip(dip)					# IP address - DIP
		self.nscmd.config_stream_utilization(utilization)	# Rate
		self.nscmd.config_stream_protocol(1)				# protocol=1 means layer3, 2 means udp, 0 means layer2
		time.sleep(1)

	def SetStreamNum(self,num):
		self.nscmd.config_stream_streamnum(num)

	def SetStream(self, port_idx, stream_max_num):
		for idx in range(stream_max_num):
			self.nscmd.set_stream(port_idx, idx)

	def SetTxTimeConfig(self,tx_time):
		self.nscmd.config_tx_txtime(tx_time)

	def SetTxPacketConfig(self,tx_packets):
		self.nscmd.config_tx_txpkts(tx_packets)

	def SetTxStartPort(self,port_idx):
		self.nscmd.transmit_pkts(port_idx)

	def SetTxStopPort(self,port_idx):
		self.nscmd.transmit_pkts_stop(port_idx)

	def GetTxCounterResult(self,port_idx,tx_time):
		tx_pkt = self.nscmd.get_counter_port(port_idx, self.nsconst.IDX_PORTCOUNTER_TX_PKT)
		tx_pkt_byte = self.nscmd.get_counter_port(port_idx, self.nsconst. IDX_PORTCOUNTER_TX_BYTE)
		tx_pkt_rate = self.nscmd.get_counter_port(port_idx, self.nsconst. IDX_PORTCOUNTER_TX_RATE_PKT)
		tx_byte_rate = self.nscmd.get_counter_port(port_idx, self.nsconst. IDX_PORTCOUNTER_TX_RATE_BYTE)
		tx_l2_rate = tx_pkt_byte * 8 / tx_time / 1_000_000
		tx_line_rate = tx_byte_rate / 1_000_000
		print(tx_pkt, tx_pkt_byte,tx_pkt_rate,tx_byte_rate,tx_l2_rate,tx_line_rate)

	def GetRxCounterResult(self,port_idx,tx_time):
		rx_pkt = self.nscmd.get_counter_port(port1_idx, self.nsconst. IDX_PORTCOUNTER_RX_GOODPKT)
		rx_pkt_byte = self.nscmd.get_counter_port(port1_idx, self.nsconst.  IDX_PORTCOUNTER_RX_BYTE)
		rx_pkt_rate = self.nscmd.get_counter_port(port1_idx, self.nsconst. IDX_PORTCOUNTER_RX_RATE_PKT)
		rx_byte_rate = self.nscmd.get_counter_port(port_idx, self.nsconst. IDX_PORTCOUNTER_RX_RATE_BYTE)
		rx_l2_rate = rx_pkt_byte * 8 / tx_time / 1_000_000
		rx_line_rate = rx_byte_rate / 1_000_000
		print(rx_pkt,rx_pkt_byte,rx_pkt_rate)

if __name__ == '__main__':
	# (0,3,1)
	# (0,3,2)
	cid_1 = 0
	bid_1 = 3
	pid_1 = 1
	cid_2 = 0
	bid_2 = 3
	pid_2 = 2
	cid_3 = 0
	bid_3 = 3
	pid_3 = 3
	cid_4 = 0
	bid_4 = 3
	pid_4 = 4
	# packet size
	pkt_len = 512
	# transmit rate
	utilization = 100
	trans_time = 9999999
	trans_pkts = 500

	# 1. Connect to Server & Reserve Ports
	instrument = NustreamCmd("192.168.1.8")
	instrument.Connect()

	media_list = instrument.GetMedia()
	for _idx,ele in enumerate(media_list):
		print(f"{ele}")

	# Reserve & Lock ports
	port1_idx = instrument.GetPortIdx(cid_1, bid_1, pid_1)
	port2_idx = instrument.GetPortIdx(cid_2, bid_2, pid_2)
	port3_idx = instrument.GetPortIdx(cid_3, bid_3, pid_3)
	port4_idx = instrument.GetPortIdx(cid_4, bid_4, pid_4)
	# lock port
	instrument.SetLockPort(cid_1, bid_1, pid_1)
	instrument.SetLockPort(cid_2, bid_2, pid_2)
	instrument.SetLockPort(cid_3, bid_3, pid_3)
	instrument.SetLockPort(cid_4, bid_4, pid_4)

	instrument.SetTxTimeConfig(trans_time)
	instrument.nscmd.config_tx_isimmediate(0)
	instrument.SetTxStartPort(port1_idx)
	instrument.SetTxStartPort(port2_idx)
	instrument.SetTxStartPort(port3_idx)
	instrument.SetTxStartPort(port4_idx)

	# clear counter before setting
	instrument.SetPortClearCounters(port1_idx)
	instrument.SetPortClearCounters(port2_idx)
	instrument.SetPortClearCounters(port3_idx)
	instrument.SetPortClearCounters(port4_idx)

	instrument.nscmd.transmit_pkts_sync()
	time_start = datetime.now()
	print("START")
	time.sleep(20)
	instrument.nscmd.transmit_pkts_sync_stop()
	time_end = datetime.now()

	time_diff = time_end - time_start
	hours, remainder = divmod(time_diff.total_seconds(), 3600)
	minutes, seconds = divmod(remainder, 60)
	time_diff_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

	time_diff_seconds = int(time_diff.total_seconds())
	print(time_diff_seconds)
	print("STOP")

	'''
	##########################################
	# Standard running step
	# 1. Connect to Server & Reserve Ports
	# 2. Initial Counter
	# 3. Config Tansmit Parameters
	# 4. Start Capture Packets
	# 5. Start Tansmit Packets
	# 6. Wait for Tansmit Packets
	# 7. Stop Capture Packets
	# 8. Show Captured Packets Infomation
	# 9. Release Ports and Disconnect
	##########################################

	# 1. Connect to Server & Reserve Ports
	instrument = NustreamCmd("192.168.1.8")
	instrument.Connect()

	#print(instrument.CheckConnection())

	media_list = instrument.GetMedia()
	for _idx,ele in enumerate(media_list):
		print(f"{ele}")

	# Reserve & Lock ports
	port1_idx = instrument.GetPortIdx(cid_1, bid_1, pid_1)
	port2_idx = instrument.GetPortIdx(cid_2, bid_2, pid_2)
	port3_idx = instrument.GetPortIdx(cid_3, bid_3, pid_3)
	port4_idx = instrument.GetPortIdx(cid_4, bid_4, pid_4)
	# lock port
	instrument.SetLockPort(cid_1, bid_1, pid_1)
	instrument.SetLockPort(cid_2, bid_2, pid_2)
	instrument.SetLockPort(cid_3, bid_3, pid_3)
	instrument.SetLockPort(cid_4, bid_4, pid_4)

	# 2. Initial Counter
	port1_media_info = instrument.GetPortMediaInfo(port1_idx)
	port2_media_info = instrument.GetPortMediaInfo(port2_idx)
	port3_media_info = instrument.GetPortMediaInfo(port3_idx)
	port4_media_info = instrument.GetPortMediaInfo(port4_idx)
	print(port1_media_info)
	print(port2_media_info)
	print(port3_media_info)
	print(port4_media_info)

	# clear counter before setting
	instrument.SetPortClearCounters(port1_idx)
	instrument.SetPortClearCounters(port2_idx)
	instrument.SetPortClearCounters(port3_idx)
	instrument.SetPortClearCounters(port4_idx)
	time.sleep(1)
	print("=== Show Clear RX result ===")
	instrument.GetRxCounterResult(port1_idx,1)
	instrument.GetRxCounterResult(port2_idx,1)
	instrument.GetRxCounterResult(port3_idx,1)
	instrument.GetRxCounterResult(port4_idx,1)
	

	# 3. Config Tansmit Parameters
	# mac address
	mac_1 = "00:22:A2:%02X:%02X:%02X"%(cid_1, bid_1, pid_1)
	mac_2 = "00:22:A2:%02X:%02X:%02X"%(cid_2, bid_2, pid_2)
	mac_3 = "00:22:A2:%02X:%02X:%02X"%(cid_3, bid_3, pid_3)
	mac_4 = "00:22:A2:%02X:%02X:%02X"%(cid_4, bid_4, pid_4)
	# ip address
	ip_1 = "192.168.%d.%d"%(bid_1, pid_1)
	ip_2 = "192.168.%d.%d"%(bid_2, pid_2)
	ip_3 = "192.168.%d.%d"%(bid_3, pid_3)
	ip_4 = "192.168.%d.%d"%(bid_4, pid_4)
	# start config

	instrument.SetPortTansmitConfig(pkt_len, utilization, 1, mac_1, mac_2, ip_1, ip_2, 0)
	#instrument.SetPortTansmitConfig(pkt_len, utilization, 1, mac_3, mac_4, ip_3, ip_4, 0)

	# set stream
	instrument.SetStreamNum(2)
	instrument.SetStream(port1_idx,2)
	instrument.SetStream(port2_idx,2)
	#instrument.SetStream(port3_idx,2)
	#instrument.SetStream(port4_idx,2)

	# 4. Start Capture Packets - capture from port 2
	#nscmd.capture_frames_start(port2_idx, nsconst.CAPTURE_ALL)

	# 5. Start Tansmit Packets - 0 means wait for a global transmit command
	# Start Tansmit Packets
	#instrument.SetTxTimeConfig(trans_time)
	instrument.SetTxPacketConfig(trans_pkts)
	instrument.nscmd.config_tx_isimmediate(0)
	instrument.SetTxStartPort(port1_idx)
	instrument.SetTxStartPort(port2_idx)
	instrument.SetTxStartPort(port3_idx)
	instrument.SetTxStartPort(port4_idx)
	time_start = datetime.now()

	# 6. Wait for Tansmit Packets
	print("Start:Wait Tansmit Packets")
	instrument.nscmd.transmit_pkts_sync()
	time.sleep(10)

	# 7. Stop Tansmit Packets
	# Stop Trans Packets
	instrument.nscmd.transmit_pkts_sync_stop()
	#instrument.SetTxStopPort(port1_idx)
	#instrument.SetTxStopPort(port2_idx)

	time_end = datetime.now()
	print("Stop:Wait Tansmit Packets")
	time.sleep(5)

	time_diff = time_end - time_start
	hours, remainder = divmod(time_diff.total_seconds(), 3600)
	minutes, seconds = divmod(remainder, 60)
	time_diff_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

	time_diff_seconds = int(time_diff.total_seconds())

	print("=== Show TX result ===")
	instrument.GetTxCounterResult(port1_idx,time_diff_seconds)
	instrument.GetTxCounterResult(port2_idx,time_diff_seconds)
	instrument.GetTxCounterResult(port3_idx,time_diff_seconds)
	instrument.GetTxCounterResult(port4_idx,time_diff_seconds)
	
	print("=== Show RX result ===")
	instrument.GetRxCounterResult(port1_idx,time_diff_seconds)
	instrument.GetRxCounterResult(port2_idx,time_diff_seconds)
	instrument.GetRxCounterResult(port3_idx,time_diff_seconds)
	instrument.GetRxCounterResult(port4_idx,time_diff_seconds)
	

	# 9. Release Ports and Disconnect
	instrument.nscmd.port_unlock()
	time.sleep(1)
	instrument.nscmd.server_disconnect()
	'''