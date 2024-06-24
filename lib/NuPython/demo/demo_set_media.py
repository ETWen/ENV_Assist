from ctypes import *
import NuPython
import time
import nuconst

cid_1 = 0
bid_1 = 3
pid_1 = 1

nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
if (nscmd.server_connect("127.0.0.1")==0):
    print("Connect to server fail!")
else:
    print("Connect to server")

nscmd.port_mark(cid_1, bid_1, pid_1)
if (nscmd.port_lock() == 0):
    print("Lock port1 fail!")
    nscmd.server_disconnect()

nscmd.config_media_speed(nsconst.MEDIA_SPEED_100M)
nscmd.config_media_duplex(nsconst.MEDIA_DUPLEX_FULL)
nscmd.config_media_nego(nsconst.MEDIA_NEGO_AUTO)
pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
print("Change media type")
nscmd.set_media(pidx)
time.sleep(3)
nscmd.read_info_link(pidx)
print ("Media speed = " + nscmd.get_media_speed(pidx))
print ("Media duplex = " + nscmd.get_media_duplex(pidx))
print ("Media negotiation = " + nscmd.get_media_autonego(pidx))
nscmd.port_unlock()
nscmd.server_disconnect()
nscmd.log_close()
