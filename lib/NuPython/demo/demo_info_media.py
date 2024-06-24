import NuPython

cid_1 = 0
bid_1 = 4
pid_1 = 1

nscmd = NuPython.NuStreamsModuleSetting()
if (nscmd.server_connect("127.0.0.1")==0):
    print("Connect to server fail!")

nscmd.port_mark(cid_1, bid_1, pid_1)
if (nscmd.port_lock() == 0):
    print("Lock port1 fail!")
    nscmd.server_disconnect()

pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
print("Read media information:")
nscmd.read_info_link(pidx)
print ("Media speed = " + nscmd.get_media_speed(pidx))
print ("Media duplex = " + nscmd.get_media_duplex(pidx))
print ("Media negotiation = " + nscmd.get_media_autonego(pidx))
nscmd.port_unlock()
nscmd.server_disconnect()
nscmd.log_close()
