import time

import NuPython
import nuconst

class myNustream(object):
	def __init__(self):
		self._ip = _ip
		self.nscmd = NuPython.NuStreamsModuleSetting()
		self.nsconst = nuconst.NuStreamsConst()
		if (nscmd.server_connect(self._ip)==0):
			print("Connect to server fail!")

	def getMedia()
		pidx = 0
		port_info_list = []
		while pidx < len(nscmd.ns_info_portlist):
		if nscmd.ns_info_portlist[pidx].boardID != 1 and nscmd.ns_info_portlist[pidx].boardID != 18:
			# Format the data as a string
			port_info = '(%d,%d,%d) Speed:%s, Duplex:%s, AutoNegotiation:%s' % (
				nscmd.ns_info_portlist[pidx].chassisID, 
				nscmd.ns_info_portlist[pidx].boardID, 
				nscmd.ns_info_portlist[pidx].portID, 
				nscmd.get_media_speed(pidx), 
				nscmd.get_media_duplex(pidx), 
				nscmd.get_media_autonego(pidx)
			)
			port_info_list.append(port_info)
		pidx += 1

		return port_info

	def setTransConfig()
		


# (0,3,1)
# (0,3,2)
cid_1 = 0
bid_1 = 3
pid_1 = 1
cid_2 = 0
bid_2 = 3
pid_2 = 2
# packet size
pkt_len = 512
# transmit rate
utilization = 100



if __name__ == '__main__':

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
	# Get the source port
	'''
	nscmd = NuPython.NuStreamsModuleSetting()
	nsconst = nuconst.NuStreamsConst()
	print ('\n<---------- Media Type ---------->')
	pidx = 0
	while pidx < len(nscmd.ns_info_portlist):
		if nscmd.ns_info_portlist[pidx].boardID != 1 and nscmd.ns_info_portlist[pidx].boardID != 18:
			print ('(%d,%d,%d) Speed:%s, Duplex:%s, AutoNegotiation:%s' %(nscmd.ns_info_portlist[pidx].chassisID, 
			nscmd.ns_info_portlist[pidx].boardID, nscmd.ns_info_portlist[pidx].portID, nscmd.get_media_speed(pidx), 
			nscmd.get_media_duplex(pidx), nscmd.get_media_autonego(pidx)))
			pidx += 1
	nscmd.port_unlock()
	time.sleep(1)
	'''

	# 1. Connect to Server & Reserve Ports
	nscmd = NuPython.NuStreamsModuleSetting()
	nsconst = nuconst.NuStreamsConst()
	if (nscmd.server_connect("127.0.0.1")==0):
		print("Connect to server fail!")
	# reserve ports
	nscmd.port_mark(cid_1, bid_1, pid_1)
	nscmd.port_mark(cid_2, bid_2, pid_2)
	if (nscmd.port_lock() == 0):
		print("Lock port1 fail!")
		nscmd.server_disconnect()
	port1_idx = nscmd.get_portidx(cid_1, bid_1, pid_1)
	port2_idx = nscmd.get_portidx(cid_2, bid_2, pid_2)

	# 2. Initial Counter
	# for correct speed
	nscmd.read_info_link(port1_idx)
	nscmd.read_info_link(port2_idx)
	# clear counter before setting
	nscmd.clear_counter_port(port1_idx)
	nscmd.clear_counter_port(port2_idx)

	# 3. Config Tansmit Parameters
	# mac address
	mac_1 = "00:22:A2:%02X:%02X:%02X"%(cid_1, bid_1, pid_1)
	mac_2 = "00:22:A2:%02X:%02X:%02X"%(cid_2, bid_2, pid_2)
	# ip address
	ip_1 = "192.168.%d.%d"%(bid_1, pid_1)
	ip_2 = "192.168.%d.%d"%(bid_2, pid_2)
	# start config
	nscmd.config_stream_pktlen(pkt_len)				# Packet length
	nscmd.config_stream_utilization(utilization)	# Rate
	nscmd.config_stream_enable_xtag(1)				# X-Tag
	nscmd.config_stream_dmac(mac_2)					# MAC address - DA
	nscmd.config_stream_smac(mac_1)					# MAC address - SA
	nscmd.config_stream_dip(ip_2)					# IP address - DIP
	nscmd.config_stream_sip(ip_1)					# IP address - SIP
	
	
	# protocol=1 means layer3, 2 means udp, 0 means layer2
	nscmd.config_stream_protocol(1)
	# single stream
	nscmd.config_stream_streamnum(1)
	nscmd.set_stream(port1_idx, 0)
	nscmd.set_stream(port2_idx, 0)

	# 4. Start Capture Packets - capture from port 2
	nscmd.capture_frames_start(port2_idx, nsconst.CAPTURE_ALL)

	# 5. Start Tansmit Packets - 0 means wait for a global transmit command
	nscmd.config_tx_isimmediate(1)
	nscmd.transmit_pkts(port1_idx)
	nscmd.transmit_pkts(port2_idx)
	# 6. Wait for Tansmit Packets
	time.sleep(2)
	# 7. Stop Tansmit Packets
	nscmd.config_tx_isimmediate(1)
	nscmd.transmit_pkts_stop(port1_idx)
	nscmd.transmit_pkts_stop(port2_idx)
	time.sleep(1)
	# 8. Show Captured Packets
	tx_p1_s1 = nscmd.get_counter_stream_tx_pkts(port1_idx, 0)
	rx_p1_s1 = nscmd.get_counter_stream_rx_pkts(port1_idx, 0)
	tx_p1_s1_bytes = nscmd.get_counter_stream_tx_bytes(port1_idx, 0)
	rx_p1_s1_bytes = nscmd.get_counter_stream_rx_bytes(port1_idx, 0)

	tx_p2_s1 = nscmd.get_counter_stream_tx_pkts(port2_idx, 0)
	rx_p2_s1 = nscmd.get_counter_stream_rx_pkts(port2_idx, 0)
	tx_p2_s1_bytes = nscmd.get_counter_stream_tx_bytes(port2_idx, 0)
	rx_p2_s1_bytes = nscmd.get_counter_stream_rx_bytes(port2_idx, 0)

	print ("Port 1 Stream:1 Send:%i Received:%i" % (tx_p1_s1, rx_p1_s1))
	print ("Port 2 Stream:1 Send:%i Received:%i" % (tx_p2_s1, rx_p2_s1))

	# 9. Release Ports and Disconnect
	nscmd.port_unlock()
	nscmd.server_disconnect()