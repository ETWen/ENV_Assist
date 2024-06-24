import NuPython
import time
cid_1 = 0
bid_1 = 9
pid_1 = 1

nscmd = NuPython.NuStreamsModuleSetting()
if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")

pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
print("Read EEPROM information:")
nscmd.read_license_board(pidx)
time.sleep(1)
print ("Slot %d MAC addr = "%bid_1 + nscmd.get_macaddr(bid_1))
print ("Slot %d serial number = "%bid_1 + nscmd.get_serialnum(bid_1))
print ("Slot %d manual date = "%bid_1 + nscmd.get_manudate(bid_1))
print ("Slot %d license mode = "%bid_1 + nscmd.get_license_mode(bid_1))
print ("Slot %d license date = "%bid_1 + nscmd.get_license_date(bid_1))

bid_1 = 10
pidx = nscmd.get_portidx(cid_1, bid_1, pid_1)
nscmd.read_license_board(pidx)
time.sleep(1)
print ("Slot %d MAC addr = "%bid_1 + nscmd.get_macaddr(bid_1))
print ("Slot %d serial number = "%bid_1 + nscmd.get_serialnum(bid_1))
print ("Slot %d manual date = "%bid_1 + nscmd.get_manudate(bid_1))
print ("Slot %d license mode = "%bid_1 + nscmd.get_license_mode(bid_1))
print ("Slot %d license date = "%bid_1 + nscmd.get_license_date(bid_1))

nscmd.server_disconnect()
nscmd.log_close()
