from ctypes import *
import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst
import matplotlib.pyplot as plt
import numpy as np
import thread

nscmd = NuPython.NuStreamsModuleSetting()
nsconst = nuconst.NuStreamsConst()
        
class T451ConnectTest:
    def __init__(self):
        self.chassis_idx = 0
        self.slot1_idx = 0
        self.slot2_idx = 1
        self.groupid = 1
        self.lockstatus = 0
        self.unlockstatus = 1
        self.sample_rate = 2 # Hz
        self.isShowChart = False
        
        

    def ShowInstantVoltage(self, cidx, sidx):
        if self.sample_rate <= 10:
            plt.ion() ## Note this correction
            plt.xlabel('Item')
            plt.ylabel('Currency(0.1mA)')
            plt.grid(True)
            plt.ylim(-1, 150)
            # for Line Chart
            
            while self.isShowChart == True:
                plt.title('MinVolt : %.2f(V) / PeakVolt : %.2f(V) / MinCurr : %.2f(mA) / PeakCurr : %.2f(mA)' %(nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_volt_min*0.01, nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_volt_peak*0.01,nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_curr_min*0.1, nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_curr_peak*0.1))
                #t = np.arange(0.0, self.sample_rate*150, 1) # range 0~100, step = 1
                t = np.arange(0.0, nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_idx, 1) # range 0~100, step = 1
                #tmplist = nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_inst_curr[0:self.sample_rate*150]
                tmplist = nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_inst_curr[0:nscmd.t451_info_board[cidx].t451_board[sidx].report.counter_idx]
                plt.plot(t, tmplist)
                plt.show()
                plt.pause(0.5)
            plt.close()
            
        
    def StartTest(self):
        print("Connect to NuPOE Server.")
        if (nscmd.t451_server_connect("192.168.1.8")==0): # connect to server
            print("Connect to server fail!")

        # lock ports per slot
        print("Lock ports.")
        if (nscmd.t451_port_lock(self.chassis_idx, self.slot1_idx, self.lockstatus) == 0):
            print("Lock port1 fail!")
            nscmd.t451_server_disconnect()

        #if (nscmd.t451_port_lock(self.chassis_idx, slot2_idx, lockstatus) == 0):
        #    print("Lock port1 fail!")
        #    nscmd.t451_server_disconnect()
            
        # group mark
        nscmd.t451_port_mark(self.chassis_idx, self.slot1_idx)
        #nscmd.t451_port_mark(self.chassis_idx, slot2_idx, 1)
        nscmd.t451_set_group(0) # set all port to group 0
        nscmd.t451_set_group(self.groupid) # set all port to group 1
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
        nscmd.t451_config_tempthreshold(70) # temperature too high
        nscmd.t451_config_tempalert(nsconst.ENABLE)
        nscmd.t451_config_reporttype(nsconst.T451_CFG_REPORT_BOTH)
        nscmd.t451_config_voltpoweron(4800) # 0.01v
        nscmd.t451_config_voltpoweroff(500)
        nscmd.t451_config_voltpowergood(3600)
        nscmd.t451_config_voltpowerunder(3500)
        nscmd.t451_config_voltpowertoohigh(5700)
        # LLDP config.
        nscmd.t451_config_lldpenable(nsconst.DISABLE)
        # Connect config.
        nscmd.t451_config_conn_loadingflag(0xf) 
        nscmd.t451_config_conn_timeout(10000) # ms
        nscmd.t451_config_conn_waittime(1000) # ms
        # Set Config.
        nscmd.t451_set_test(self.chassis_idx, self.slot1_idx)
        time.sleep(1)
        nscmd.t451_gcounter_read_start(self.groupid, self.sample_rate) # start counter - group
        time.sleep(1)
        # relay off per slot
        print("Start connect test-1.")
        nscmd.t451_open_relay(self.chassis_idx, self.slot1_idx, 1)
        time.sleep(1)
        self.isShowChart = True
        # start connect test
        #thread.start_new_thread(self.ShowInstantVoltage, (self.chassis_idx, self.slot1_idx,))
        nscmd.t451_start_connect(self.chassis_idx, self.slot1_idx)
        
        #print("Start connect test-2.")
        #nscmd.t451_open_relay(self.chassis_idx, self.slot2_idx, 0)
        #time.sleep(1)
        #nscmd.t451_start_connect(self.chassis_idx, self.slot2_idx)

        print("Waiting for 10 sec.")
        time.sleep(10)
        
        
        #self.isShowChart = False
        # relay off per slot
        nscmd.t451_open_relay(self.chassis_idx, self.slot1_idx, 0)
        time.sleep(1)
        #nscmd.t451_open_relay(self.chassis_idx, self.slot2_idx, 0)

        # stop counter - group
        nscmd.t451_gcounter_read_stop(self.groupid)
        # stop test - group
        print("Stop test.")
        nscmd.t451_gstop_test(self.groupid)
        print("Show connect test report...")
        nscmd.t451_report_connect(self.chassis_idx, self.slot1_idx)
        # relay off - group
        nscmd.t451_gopen_relay(self.groupid, 0)
        time.sleep(1)
        
        print("Unlock port.")
        if (nscmd.t451_port_lock(self.chassis_idx, self.slot1_idx, self.unlockstatus) == 0):
            print("UnLock port1 fail!")
            nscmd.t451_server_disconnect()

        #if (nscmd.t451_port_lock(self.chassis_idx, slot2_idx, unlockstatus) == 0):
        #    print("UnLock port1 fail!")
        #    nscmd.t451_server_disconnect()
        time.sleep(1)
        print("Disconnect.")
        nscmd.t451_server_disconnect()
        self.ShowInstantVoltage(self.chassis_idx, self.slot1_idx)
		
t451test = T451ConnectTest()
t451test.StartTest()
