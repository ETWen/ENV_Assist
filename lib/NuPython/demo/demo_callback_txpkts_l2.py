from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst

cid_1 = 0
bid_1 = 10
pid_1 = 1

cid_2 = 0
bid_2 = 10
pid_2 = 2

# packet size
pkt_len = 64
# packet count
pkt_count = 1000
# transmit rate
utilization = 100

loop_count = 1

def callback_function(cid, bid, pid, reportid):
    # user callback
    if reportid == 0x300:
        print(f"Report(TxEnd): ({cid}, {bid}, {pid})")
    elif reportid == 0x400:
        print(f"Report(LinkChange): ({cid}, {bid}, {pid})")

# connect to server                    
nscmd = NuPython.NuStreamsModuleSetting(callback_function)
nsconst = nuconst.NuStreamsConst()
if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")

# lock ports
nscmd.port_mark(cid_1, bid_1, pid_1)
nscmd.port_mark(cid_2, bid_2, pid_2)

# do loop
for loopnum in range(loop_count):
    print ("Loop:%i" % (loopnum+1))
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
    #nscmd.config_stream_enable_randomlen(1)
    nscmd.set_stream(port1_idx, 0)
    nscmd.config_tx_txtime(10)
    # 0-means wait for a global transmit command
    nscmd.config_tx_isimmediate(1)
    nscmd.transmit_pkts(port1_idx)
    print ("(%i,%i,%i), pktlen = %i, pkt/sec=%i" % (cid_1, bid_1, pid_1, nscmd.stream_pktlen, nscmd.counter_per_sec))

    #nscmd.config_tx_txpkts()

    # for port flow control
    #nscmd.config_port_flowctrl_tx(1)
    #nscmd.config_port_flowctrl_rx(1)

    #nscmd.transmit_pkts_sync()
    time.sleep(12)
    nscmd.read_counter_port_once(port1_idx)
    nscmd.read_counter_port_once(port2_idx)
    time.sleep(1)
    print ("===Counter Report===")
    print (" Port 1   Tx:%i" % (nscmd.get_counter_port(port1_idx, nsconst.IDX_PORTCOUNTER_TX_PKT)))
    print ("Port 2   Rx-xtag:\t%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_XTAG)))
    print ("Port 2   Rx-size64:\t%i" % (nscmd.get_counter_port(port2_idx, nsconst.IDX_PORTCOUNTER_RX_64)))
    
    
    nscmd.port_unlock()
nscmd.server_disconnect()
nscmd.log_close()

