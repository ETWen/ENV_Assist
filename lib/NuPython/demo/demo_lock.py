import NuPython

cid_1 = 0
bid_1 = 2
pid_1 = 1

nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()

if (nscmd.server_connect("127.0.0.1")==0):
    print("Connect to server fail!")
else:
    print("Connected to server!")

nscmd.port_mark(cid_1, bid_1, pid_1)
if (nscmd.port_lock() == 0):
    print("Lock port1 fail!")
    nscmd.server_disconnect()
else:
    print("Locked port1!")




nscmd.port_unlock()
print("UnLocked port1!")
nscmd.server_disconnect()
print("Disconnected.")
nscmd.log_close()
