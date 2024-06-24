import NuPython
import time
cid_1 = 0
bid_1 = 1
pid_1 = 1

nscmd = NuPython.NuStreamsModuleSetting()
if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")

pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
print("Read board information:")
nscmd.read_info_board(pidx)
time.sleep(1)
print ("Slot %d" % (bid_1))
print ("  hw ver. = ", nscmd.get_version_hw(bid_1))
print ("  fw ver. = ", nscmd.get_version_fw(bid_1))
print ("  prom ver. = ", nscmd.get_version_prom(bid_1))
print ("  cardtype = ", nscmd.get_modelname(bid_1))

bid_1 = 3
pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
nscmd.read_info_board(pidx)
time.sleep(1)
print ("Slot %d" % (bid_1))
print ("  hw ver. = ", nscmd.get_version_hw(bid_1))
print ("  fw ver. = ", nscmd.get_version_fw(bid_1))
print ("  prom ver. = ", nscmd.get_version_prom(bid_1))
print ("  cardtype = ", nscmd.get_modelname(bid_1))

bid_1 = 7
pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
nscmd.read_info_board(pidx)
time.sleep(1)
print ("Slot %d" % (bid_1))
print ("  hw ver. = ", nscmd.get_version_hw(bid_1))
print ("  fw ver. = ", nscmd.get_version_fw(bid_1))
print ("  prom ver. = ", nscmd.get_version_prom(bid_1))
print ("  cardtype = ", nscmd.get_modelname(bid_1))

bid_1 = 10
pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
nscmd.read_info_board(pidx)
time.sleep(1)
print ("Slot %d" % (bid_1))
print ("  hw ver. = ", nscmd.get_version_hw(bid_1))
print ("  fw ver. = ", nscmd.get_version_fw(bid_1))
print ("  prom ver. = ", nscmd.get_version_prom(bid_1))
print ("  cardtype = ", nscmd.get_modelname(bid_1))
nscmd.server_disconnect()
nscmd.log_close()
