import NuPython

nscmd = NuPython.NuStreamsModuleSetting()

if (nscmd.server_connect("192.168.1.8")==0):
    print("Connect to server fail!")
else:
    print("Connected to server!")

for idx in range(32):
	nscmd.power_off(idx)
nscmd.power_on(3)
nscmd.power_on(1)
nscmd.power_on(7)
nscmd.set_slot_power()
nscmd.server_disconnect()
print("Disconnected.")
nscmd.log_close()
