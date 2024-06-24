from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst

cid_1 = 2
bid_1 = 8
pid_1 = 1

cid_2 = 2
bid_2 = 8
pid_2 = 2

# packet size
pkt_len = 64
# packet count
pkt_count = 1000
# transmit rate
utilization = 100

# connect to server                    
nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()

if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")

# lock ports
nscmd.port_mark(cid_1, bid_1, pid_1)
nscmd.port_mark(cid_2, bid_2, pid_2)
if (nscmd.port_lock() == 0):
    print("Lock port1 fail!")
    nscmd.server_disconnect()
port1_idx = nscmd.get_portidx(cid_1, bid_1, pid_1)
port2_idx = nscmd.get_portidx(cid_2, bid_2, pid_2)
# for correct speed
nscmd.read_info_link(port1_idx)
nscmd.read_info_link(port2_idx)
# clear counter before setting
nscmd.clear_counter_port(port1_idx)
nscmd.clear_counter_port(port2_idx)
# mac address
mac_1 = "00:22:A2:%02X:%02X:%02X"%(cid_1, bid_1, pid_1)
mac_2 = "00:22:A2:%02X:%02X:%02X"%(cid_2, bid_2, pid_2)
# start config
nscmd.config_stream_pktlen(pkt_len)
nscmd.config_stream_smac(mac_1)
nscmd.config_stream_dmac(mac_2)
nscmd.config_stream_utilization(utilization)
# protocol=1 means layer3, 2 means udp, 0 means layer2
nscmd.config_stream_protocol(0)
# single stream
nscmd.config_stream_streamnum(1)
nscmd.set_stream(port1_idx, 0)
nscmd.config_tx_txpkts(pkt_count)
# 0-means wait for a global transmit command
nscmd.config_tx_isimmediate(1)
nscmd.transmit_pkts(port1_idx)
time.sleep(1)
nscmd.read_counter_port_once(port2_idx)
time.sleep(1)
print ("Port 2   Received - Boradcst:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_BORADCAST)))
print ("Port 2   Received - Unicast:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_UNICAST)))
print ("Port 2   Received - Undersize:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_UNDERSIZE)))
print ("Port 2   Received - Oversize:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_OVERSIZE)))
print ("Port 2   Received - Goodpkts:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_GOODPKT)))
print ("Port 2   Received - 64 byte:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_64)))
print ("Port 2   Received - 65-127 byte:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_65_127)))
print ("Port 2   Received - 128-255 byte:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_128_255)))
print ("Port 2   Received - 256-511 byte:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_256_511)))
print ("Port 2   Received - 512-1023 byte:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_512_1023)))
print ("Port 2   Received - 1024-1522 byte:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_1024_1522)))
print ("Port 2   Received - XTAG:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_XTAG)))
print ("Port 2   Received - Total bytes:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_BYTE)))
print ("Port 2   Received - Byte rate:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_RATE_BYTE)))
print ("Port 2   Received - Packet rate:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_RATE_PKT)))
print ("Port 2   Received - Packet rate:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_RATE_PKT)))


nscmd.port_unlock()
nscmd.server_disconnect()
nscmd.log_close()

