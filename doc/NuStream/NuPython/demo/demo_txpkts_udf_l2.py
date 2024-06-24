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
pkt_len = 70
# packet count
pkt_count = 10
# transmit rate
utilization = 100
#udf payload
pktlist = [0xd8,0xfe,0xe3,0xc8,0xc2,0x7a,0x6c,0x62,0x6d,0xdf,0x99,0x98,0x08,0x00,0x45,0x00,0x00,0x34,0x4e,0x4c,0x40,0x00,0x80,0x06,0x7e,0x44,0xc0,0xa8,0x01,0x6f,0x7d,0xd1,0xee,0x4a,0xcb,0x3d,0x00,0x50,0xa9,0x2a,0x17,0x45,0x00,0x00,0x00,0x00,0x80,0x02,0x20,0x00,0x94,0xdf,0x00,0x00,0x02,0x04,0x05,0xb4,0x01,0x03,0x03,0x08,0x01,0x01,0x04,0x02]
payload = [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xFF]
# connect to server                    
nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
if (nscmd.server_connect("127.0.0.1")==0):
    print("Connect to server fail!")

# lock ports
nscmd.port_mark(cid_1, bid_1, pid_1)
#nscmd.port_mark(cid_2, bid_2, pid_2)
if (nscmd.port_lock(cid_1) == 0):
    print("Lock port1 fail!")
    nscmd.server_disconnect()
port1_idx = nscmd.get_portidx(cid_1, bid_1, pid_1)
#port2_idx = nscmd.get_portidx(cid_2, bid_2, pid_2)
# for correct speed
nscmd.read_info_link(port1_idx)
#nscmd.read_info_link(port2_idx)
# clear counter before setting
nscmd.clear_counter_port(port1_idx)
#nscmd.clear_counter_port(port2_idx)
# mac address
mac_1 = "00:22:A2:%02X:%02X:%02X"%(cid_1, bid_1, pid_1)
mac_2 = "00:22:A2:%02X:%02X:%02X"%(cid_2, bid_2, pid_2)
# start config
nscmd.config_stream_pktlen(pkt_len)
nscmd.config_stream_smac(mac_1)
nscmd.config_stream_dmac(mac_2)
nscmd.config_stream_utilization(utilization)
# protocol=1 means layer3, 2 means udp, 0 means layer2, 0xd means user define
# single stream
nscmd.config_stream_streamnum(2)

# stream1 - full packet
nscmd.config_stream_protocol(0xd)
nscmd.config_stream_udfpayload(pktlist)
nscmd.set_stream(port1_idx, 0)
# stream2 - just payload
nscmd.config_stream_protocol(0)
nscmd.config_stream_udfpayload(payload)
nscmd.set_stream(port1_idx, 1)

nscmd.config_tx_txpkts(pkt_count)
# 0-means wait for a global transmit command
nscmd.config_tx_isimmediate(1)
nscmd.transmit_pkts(port1_idx)
time.sleep(1)
nscmd.read_counter_port_once(port1_idx)
#nscmd.read_counter_port_once(port2_idx)
time.sleep(1)
print ("Port 1   Send:%i" % (nscmd.get_counter_port(port1_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)))
#print "Port 2   Received:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_UNICAST))

nscmd.port_unlock(cid_1)
nscmd.server_disconnect()
nscmd.log_close()

