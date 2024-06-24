import NuPython

server_ip = "127.0.0.1"
nscmd = NuPython.NuStreamsModuleSetting()
print("Connect to server.")
if (nscmd.server_connect(server_ip)==0):
    print("Connect to server fail!")
else:
    print("Connected...")
print("Disconnect.")
nscmd.server_disconnect()
nscmd.log_close()
