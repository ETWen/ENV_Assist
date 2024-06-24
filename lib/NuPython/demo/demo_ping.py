from ctypes import *
import time,sys,traceback
import NuPython
import nuconst

cid_1 = 0
bid_1 = 4
pid_1 = 1

cid_2 = 0
bid_2 = 4
pid_2 = 2

# ping ip, mac
ping_sip = "192.168.4.1"
ping_dip = "192.168.4.2"
ping_gip = "192.168.4.254"
mac_1 = "00:22:A2:%02X:%02X:%02X"%(cid_1, bid_1, pid_1)
mac_2 = "00:22:A2:%02X:%02X:%02X"%(cid_2, bid_2, pid_2)

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


# Port2 ARP config
nscmd.config_arp_enablenode(0, True)
nscmd.config_arp_mac(0, mac_2)
nscmd.config_arp_ipv4(0, ping_dip)
nscmd.config_arp_gateway(0, ping_gip)
# start ARP
nscmd.arp_reply_start(port2_idx)
time.sleep(1)
# ping config
nscmd.config_ping_sip(ping_sip)
nscmd.config_ping_dip(ping_dip)
nscmd.config_ping_gip(ping_gip)
nscmd.config_ping_smac(mac_1)
# start ping
nscmd.pingv4_send(port1_idx)
time.sleep(5)
nscmd.arp_reply_stop(port1_idx)
nscmd.arp_reply_stop(port2_idx)
nscmd.port_unlock()
nscmd.server_disconnect()

