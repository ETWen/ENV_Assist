from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst

cid_1 = 2
bid_1 = 7
pid_1 = 1

cid_2 = 2
bid_2 = 7
pid_2 = 2

# packet size
pkt_len = 128
# packet count
pkt_count = 1000
# transmit rate
utilization = 100

# connect to server                    
nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")

# lock ports-for NS900
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
nscmd.config_stream_streamnum(2)
# protocol=1 means layer3, 2 means udp, 0 means layer2
nscmd.config_stream_protocol(0)
# vlan setting
nscmd.config_stream_enable_vlan(1)
nscmd.config_stream_vlan_id(100)
nscmd.config_stream_vlan_pri(7)
# set stream-1
nscmd.set_stream(port1_idx, 0)
# set stream-2, set vlan priority to 3
nscmd.config_stream_vlan_pri(3)
nscmd.set_stream(port1_idx, 1)

nscmd.config_tx_txpkts(pkt_count)
# 0-means wait for a global transmit command
nscmd.config_tx_isimmediate(1)
nscmd.transmit_pkts(port1_idx)
# wait for transmit
time.sleep(1)
nscmd.read_counter_port_once(port1_idx)
nscmd.read_counter_port_once(port2_idx)
# wait for read counter
time.sleep(2)
print ("Port 1   Send:%i" % (nscmd.get_counter_port(port1_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)))
print ("Port 2   Received:%i, VLAN:%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_UNICAST), nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_VLAN)))

nscmd.port_unlock()
time.sleep(1)
nscmd.server_disconnect()
nscmd.log_close()

