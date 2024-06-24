from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst

cid_1 = 0
bid_1 = 7
pid_1 = 1

cid_2 = 0
bid_2 = 7
pid_2 = 2

cid_3 = 0
bid_3 = 7
pid_3 = 3

pkt_len = 128
pkt_count = 0 #continue
utilization = 50 # transmit rate
timeout_flood = 5000

nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
print("Connect to Server")
if (nscmd.server_connect("192.168.1.16")==0):
    print("Connect to Server Fail!")

# lock ports
nscmd.port_mark(cid_1, bid_1, pid_1)
nscmd.port_mark(cid_2, bid_2, pid_2)
nscmd.port_mark(cid_3, bid_3, pid_3)

if (nscmd.port_lock() == 0):
    print("Lock Port Fail!")
    nscmd.server_disconnect()
port1_idx = nscmd.get_portidx(cid_1, bid_1, pid_1)
port2_idx = nscmd.get_portidx(cid_2, bid_2, pid_2)
port3_idx = nscmd.get_portidx(cid_3, bid_3, pid_3)
# for correct speed
nscmd.read_info_link(port1_idx)
nscmd.read_info_link(port2_idx)

# port learning
print("Port Learning")
nscmd.port_learning(port1_idx, 0, 64, 10)
nscmd.port_learning(port2_idx, 0, 64, 10)

# clear counter before setting
nscmd.clear_counter_port(port1_idx)
nscmd.clear_counter_port(port2_idx)
nscmd.clear_counter_port(port3_idx)

time.sleep(1)
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
print("Start Testing")
# do loop
for loopnum in range(timeout_flood):
    #print ("Sec:%i" % (loopnum+1))
    nscmd.read_counter_port_once(port2_idx)
    nscmd.read_counter_port_once(port3_idx)
    time.sleep(1)
    count_flood = nscmd.get_counter_port(port3_idx, nsconst.IDX_PORTCOUNTER_RX_UNICAST)
    #print ("Port 2   Rx-unicast:\t%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_UNICAST)))
    print ("(Sec.:%d) Monitor Port Rx(unicast):\t%i\r" % (loopnum+1, count_flood), end='')
    if count_flood > 0:
        print ("\nDevice AgingTime:%d" % (loopnum+1))
        break

nscmd.port_unlock()
print("Finish!")
    
nscmd.server_disconnect()
nscmd.log_close()