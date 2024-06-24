from ctypes import *
import time,sys,traceback
import NuPython
import nuconst

cid_1 = 0
bid_1 = 4
pid_1 = 1

# ping ip, mac
mac_1 = "00:22:A2:%02X:%02X:%02X"%(cid_1, bid_1, pid_1)

# connect to server                    
nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
if (nscmd.server_connect("127.0.0.1")==0):
    print("Connect to server fail!")
# lock ports
nscmd.port_mark(cid_1, bid_1, pid_1)
if (nscmd.port_lock() == 0):
    print("Lock port1 fail!")
    nscmd.server_disconnect()
port1_idx = nscmd.get_portidx(cid_1, bid_1, pid_1)

# Port dhcp config
nscmd.config_dhcp_mac(mac_1)
# start dhcp
nscmd.dhcp_set(port1_idx)
nscmd.dhcp_discovery(port1_idx)
time.sleep(6)
nscmd.port_unlock()
nscmd.server_disconnect()

