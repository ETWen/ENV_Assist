from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst
cid_1 = 0
bid_1 = 4
pid_1 = 1

cid_2 = 0
bid_2 = 4
pid_2 = 2

# packet size
pkt_len = 128
# packet count
pkt_count = 1000
# transmit rate
utilization = 10

##########################################
#  Standard running step
#  1. Connect to Server & Reserve Ports
#  2. Initial Counter
#  3. Config Tansmit Parameters
#  4. Start Capture Packets
#  5. Start Tansmit Packets
#  6. Wait for Tansmit Packets
#  7. Stop Capture Packets
#  8. Show Captured Packets Infomation
#  9. Release Ports and Disconnect
##########################################

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
#  for correct speed
nscmd.read_info_link(port1_idx)
nscmd.read_info_link(port2_idx)
#  clear counter before setting
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
nscmd.config_stream_pktlen(pkt_len)
nscmd.config_stream_smac(mac_1)
nscmd.config_stream_dmac(mac_2)
nscmd.config_stream_sip(ip_1)
nscmd.config_stream_dip(ip_2)
nscmd.config_stream_utilization(utilization)
# protocol=1 means layer3, 2 means udp, 0 means layer2
nscmd.config_stream_protocol(1)
# single stream
nscmd.config_stream_streamnum(1)
nscmd.set_stream(port1_idx, 0)
nscmd.config_tx_txpkts(pkt_count)

# 4. Start Capture Packets - capture from port 2
nscmd.capture_frames_start(port2_idx, nsconst.CAPTURE_ALL)

# 5. Start Tansmit Packets - 0 means wait for a global transmit command
nscmd.config_tx_isimmediate(1)
nscmd.transmit_pkts(port1_idx)

# 6. Wait for Tansmit Packets
time.sleep(2)

# 7. Stop Capture Packets - capture packets immediately, so control stop time by self
nscmd.capture_frames_stop(port2_idx, 100)
time.sleep(1)

# 8. Show Captured Packets Infomation
# combine packets into a pcap file, call tshrak to process the pcap file to a xml file. 
# then analysis xml file. 
nscmd.show_packet_content(port2_idx, 1)
nscmd.show_packet_info(port2_idx, 1)

#  9. Release Ports and Disconnect
nscmd.port_unlock()
nscmd.server_disconnect()


