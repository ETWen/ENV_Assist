import NuPython
import time
nscmd = NuPython.NuStreamsModuleSetting()

if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")
else:
    print("Connected to server!")

nscmd.get_slot_power()
time.sleep(1)
#default is 16 slots, get only 10 slots(for Nustreams-900)
print("Power status:", nscmd.map_powershow[0:10])
nscmd.server_disconnect()
print("Disconnected.")
nscmd.log_close()
