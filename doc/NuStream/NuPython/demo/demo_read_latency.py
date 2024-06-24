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
pkt_len = 512
# packet count
pkt_count = 100000
# transmit rate
utilization = 10

# connect to server                    
nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()

if (nscmd.server_connect("127.0.0.1")==0):
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
# clear stream counter before setting
nscmd.clear_counter_stream(port1_idx)
nscmd.clear_counter_stream(port2_idx)

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
# multi-stream, number >= 2
nscmd.config_stream_streamnum(2)
nscmd.set_stream(port1_idx, 0)
nscmd.set_stream(port1_idx, 1)
# config rx stream
nscmd.set_config_rxstream(port2_idx)
nscmd.config_tx_txpkts(pkt_count)
# 0-means wait for a global transmit command
nscmd.config_tx_isimmediate(1)
nscmd.transmit_pkts(port1_idx)
time.sleep(1)
nscmd.read_counter_stream_once(port2_idx)
nscmd.read_counter_stream_once(port2_idx)
time.sleep(1)
# latency value is vaild while packet transmitting
rx_s1 = nscmd.get_counter_stream_rx_latency(port2_idx, 0)
rx_s2 = nscmd.get_counter_stream_rx_latency(port2_idx, 1)
print "Port 1   Send:%i" % (nscmd.get_counter_port(port1_idx, nsconst.IDX_PORTCOUNTER_TX_PKT))
print "Port 2 Stream 1 Latency:%i" % (rx_s1)
print "Port 2 Stream 2 Latency:%i" % (rx_s2)

nscmd.port_unlock()
nscmd.server_disconnect()
nscmd.log_close()

