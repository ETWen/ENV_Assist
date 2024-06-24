from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst
import matplotlib.pyplot as plt
import numpy as np
import thread

chassis_idx = 0
slot1_idx = 0
slot2_idx = 1
groupid = 1
lockstatus = 0
unlockstatus = 1

nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()


isShowChart = False
def ShowInstantVoltage(cidx, sidx):
    t = np.arange(0.0, 50.0, 1) # range 0~100, step = 1
    # for Line Chart
    plt.ion() ## Note this correction
    plt.xlabel('Item (s)')
    plt.ylabel('Value')
    plt.title('Python Line Chart: Plotting numbers')
    plt.grid(True)
    while isShowChart == True:
        plt.plot(t, nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_inst_curr)
        plt.show()
        plt.pause(0.05)
        

print("Connect to NuPOE Server.")
if (nscmd.t451_server_connect("192.168.1.8")==0): # connect to server
    print("Connect to server fail!")

# lock ports per slot
print("Lock ports.")
if (nscmd.t451_port_lock(chassis_idx, slot1_idx, lockstatus) == 0):
    print("Lock port1 fail!")
    nscmd.t451_server_disconnect()

#if (nscmd.t451_port_lock(chassis_idx, slot2_idx, lockstatus) == 0):
#    print("Lock port1 fail!")
#    nscmd.t451_server_disconnect()
    
# group mark
nscmd.t451_port_mark(chassis_idx, slot1_idx, 1)
#nscmd.t451_port_mark(chassis_idx, slot2_idx, 1)
nscmd.t451_set_group(0) # set all port to group 0
nscmd.t451_set_group(groupid) # set all port to group 1
time.sleep(1)
# Set test config 
# General config.
print("Set test config.")
nscmd.t451_config_poeclass(0)
nscmd.t451_config_duttype(nsconst.T451_CFG_DUTTYPE_PSE)
nscmd.t451_config_alternative(nsconst.T451_CFG_ALTER_1236)
nscmd.t451_config_cabletype(nsconst.T451_CFG_CABLE_CAT5)
nscmd.t451_config_cablelen(1)
nscmd.t451_config_copperloss(0)
nscmd.t451_config_poweralert(nsconst.ENABLE)
nscmd.t451_config_overheadthr(70) # temperature too high
nscmd.t451_config_overheadalert(nsconst.ENABLE)
nscmd.t451_config_reporttype(nsconst.T451_CFG_REPORT_BOTH)
nscmd.t451_config_voltpoweron(4800) # 0.01v
nscmd.t451_config_voltpoweroff(500)
nscmd.t451_config_voltpowergood(3600)
nscmd.t451_config_voltpowerunder(3500)
nscmd.t451_config_voltpowertoohigh(5700)
# Shortcurcite config.
nscmd.t451_config_short_timeout(3000) # ms
# Set Config.
nscmd.t451_set_test(chassis_idx, slot1_idx)
time.sleep(1)
nscmd.t451_gcounter_read_start(groupid,1000) # start counter - group
time.sleep(1)
# relay off per slot
print("Start short circuit test.")
nscmd.t451_open_relay(chassis_idx, slot1_idx, 1)
time.sleep(1)
isShowChart = True
#thread.start_new_thread(ShowInstantVoltage, (chassis_idx, slot1_idx,))
# start short circuit test
nscmd.t451_start_shorttest(chassis_idx, slot1_idx)

#print("Start short circuit test-2.")
#nscmd.t451_open_relay(chassis_idx, slot2_idx, 0)
#time.sleep(1)
#nscmd.t451_start_shorttest(chassis_idx, slot2_idx)

print("Waiting for 6 sec.")
time.sleep(6)
isShowChart = False
# relay off per slot
nscmd.t451_open_relay(chassis_idx, slot1_idx, 0)
time.sleep(1)
#nscmd.t451_open_relay(chassis_idx, slot2_idx, 0)

# stop counter - group
nscmd.t451_gcounter_read_stop(groupid)
# stop test - group
print("Stop test.")
nscmd.t451_gstop_test(groupid)
print("Show connect test report...")
nscmd.t451_report_connect(chassis_idx, slot1_idx)
print("Show short circuit test report...")
nscmd.t451_report_shortcircuit(chassis_idx, slot1_idx)
# relay off - group
nscmd.t451_gopen_relay(groupid, 0)
time.sleep(1)
print("Unlock port.")
if (nscmd.t451_port_lock(chassis_idx, slot1_idx, unlockstatus) == 0):
    print("UnLock port1 fail!")
    nscmd.t451_server_disconnect()

#if (nscmd.t451_port_lock(chassis_idx, slot2_idx, unlockstatus) == 0):
#    print("UnLock port1 fail!")
#    nscmd.t451_server_disconnect()
time.sleep(1)
print("Disconnect.")
nscmd.t451_server_disconnect()