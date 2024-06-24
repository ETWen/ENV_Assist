#!/usr/bin/python
# -*- encoding: utf-8 -*-
from ctypes import *

import time,sys,traceback
import ctypes
import NuPython
import time
import nuconst

python_ver = 2
if sys.version_info < (3, 0):
    import Tkinter as tk
    import tkMessageBox as msgbox
    python_ver = 2
else:
    import tkinter as tk
    from tkinter import messagebox as msgbox
    python_ver = 3
    
class SinglePort:
    def __init__(self):
        self.chassis_id = 0
        self.board_id = 1
        self.port_id = 1
            
class SampleUIApp(tk.Tk):
    # initial
    
    nscmd = NuPython.NuStreamsModuleSetting()
    nsconst = nuconst.NuStreamsConst()
    
    
    def __init__(self):
        self.offset_btnx = 4
        self.portlist = []
        tk.Tk.__init__(self)
        self.after_idle(self.doUpdateIdle)
        self.protocol("WM_DELETE_WINDOW", self.doWindowClosing)
        self.title("Test Python GUI")
        self.resizable(0,0)
        self.drawTestUI()

    
        
    def drawTestUI(self):
        ##### declare #####
        # string
        self.str_serverip = tk.StringVar(self, value="127.0.0.1")
        self.str_pktlen = tk.StringVar(self, value="256")
        self.str_pktnum = tk.StringVar(self, value="1000")
        self.str_txutil = tk.StringVar(self, value="50")
        # editor
        #editor_ip = tk.Text(self, bd =2, width=18, height=1.4)
        self.editor_ip = tk.Entry(self, bd =2, textvariable=self.str_serverip)
        self.editor_pktlen = tk.Entry(self, bd =2, textvariable=self.str_pktlen)
        self.editor_pktnum = tk.Entry(self, bd =2, textvariable=self.str_pktnum)
        self.editor_txutil = tk.Entry(self, bd =2, textvariable=self.str_txutil)
        self.editor_result_tx = tk.Entry(self, bd =2, state = "disabled")
        self.editor_result_rx = tk.Entry(self, bd =2, state = "disabled")
        #log
        self.logbox = tk.Text(self, width=40, height=7)
        self.logscrollbar = tk.Scrollbar(self)
        self.logbox.config(yscrollcommand= self.logscrollbar.set)
        self.logscrollbar.config(command= self.logbox.yview)
        
        
        # button
        self.button_connect = tk.Button(self, text ="Connect", width = 9, command = self.doConnect)
        self.button_run = tk.Button(self, text ="Run", height = 3, width = 9, command = self.doRun)
        # label text
        self.label_null = tk.Label(self, text="")
        self.label_serverip = tk.Label(self, text="Server IP :")
        self.label_src = tk.Label(self, text="Source Port")
        self.label_dest = tk.Label(self, text="Destination Port")
        self.label_pktlen = tk.Label(self, text="Packet length(bytes) :")
        self.label_pktnum = tk.Label(self, text="Packet number(s) :")
        self.label_txutil = tk.Label(self, text="Tx utilization(%) :")
        self.label_result = tk.Label(self, text="Result :")
        self.label_result_tx = tk.Label(self, text="Tx(packets) :")
        self.label_result_rx = tk.Label(self, text="Rx(packets) :")
        self.label_log = tk.Label(self, text="Log :")
        #selectmode=tk.MULTIPLE當作參數可以選多行. exportselection=0可以讓多個grid不會因為focus消失而沒選
        #listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, exportselection=0)
        self.listbox_src = tk.Listbox(self, exportselection=0)
        #self.listbox_src.insert(0,"(0,3,1)")
        self.listbox_dest = tk.Listbox(self, exportselection=0)
        #self.listbox_dest.insert(0,"(0,3,1)")
        
        ##### /declare #####

        # layout
        ridx = 0
        self.label_serverip.grid(column=0, row=ridx)
        self.editor_ip.grid(column=1, row=ridx)
        self.button_connect.grid(column=2, row=ridx, padx = self.offset_btnx)
        ridx += 1
        self.label_null.grid(column=0, row=ridx)
        ridx += 1
        self.label_src.grid(column=0, row=ridx, sticky=tk.W)
        self.label_dest.grid(column=1, row=ridx, sticky=tk.W)
        ridx += 1
        self.listbox_src.grid(column=0, row=ridx)
        self.listbox_dest.grid(column=1, row=ridx)
        ridx += 1
        self.label_null.grid(column=0, row=ridx)
        ridx += 1
        self.label_pktlen.grid(column=0, row=ridx, sticky=tk.W, padx = self.offset_btnx)
        self.editor_pktlen.grid(column=1, row=ridx)
        self.button_run.grid(column=2, row=ridx, rowspan=3)
        ridx += 1
        self.label_pktnum.grid(column=0, row=ridx, sticky=tk.W, padx = self.offset_btnx)
        self.editor_pktnum.grid(column=1, row=ridx)
        ridx += 1
        self.label_txutil.grid(column=0, row=ridx, sticky=tk.W, padx = self.offset_btnx)
        self.editor_txutil.grid(column=1, row=ridx)
        ridx += 1
        self.label_result.grid(column=0, row=ridx, sticky=tk.W)
        ridx += 1
        self.label_result_tx.grid(column=0, row=ridx, sticky=tk.W, padx = self.offset_btnx)
        self.editor_result_tx.grid(column=1, row=ridx)
        ridx += 1
        self.label_result_rx.grid(column=0, row=ridx, sticky=tk.W, padx = self.offset_btnx)
        self.editor_result_rx.grid(column=1, row=ridx)
        ridx += 1
        self.label_log.grid(column=0, row=ridx, sticky=tk.W)
        ridx += 1
        self.logbox.grid(column=0, row=ridx, columnspan = 2, sticky=tk.W)
        self.logscrollbar.grid(column=2, row=ridx, rowspan=2,  sticky=tk.N+tk.S+tk.W)
        # dialog size
        self.geometry('370x500')
    ##### functions #####
    def doUpdateIdle(self):
        self.after(100, self.doUpdateIdle)
        
    def doConnect(self):
        if (self.nscmd.server_connect(self.editor_ip.get())==0):
            self.logbox.insert(tk.END, "Connect to server fail!\n")
        else:
            self.logbox.insert(tk.END, "Server Connected.\n")
        time.sleep(1)
        if self.nscmd.total_port_num > 0:
            for pidx in range(self.nscmd.total_port_num):
                if self.nscmd.ns_info_portlist[pidx].board_id != 1 and self.nscmd.ns_info_portlist[pidx].board_id != 18:
                    tmpPort = SinglePort()
                    tmpPort.chassis_id = self.nscmd.ns_info_portlist[pidx].chassis_id
                    tmpPort.board_id = self.nscmd.ns_info_portlist[pidx].board_id
                    tmpPort.port_id = self.nscmd.ns_info_portlist[pidx].port_id
                    self.portlist.append(tmpPort)
                    portstr = "(" + str(self.nscmd.ns_info_portlist[pidx].chassis_id)+","+str(self.nscmd.ns_info_portlist[pidx].board_id)+","+str(self.nscmd.ns_info_portlist[pidx].port_id)+")"
                    self.listbox_src.insert(tk.END, portstr)
                    self.listbox_dest.insert(tk.END, portstr)
                    self.logbox.insert(tk.END, "Insert port "+portstr+" to list\n")
                else:
                    self.logbox.insert(tk.END, "Control module no need to insert.\n")
                

    def doRun(self):
        # Step 1. lock port
        # Step 2. read link status and clear counter
        # Step 3. set config to port
        # Step 4. transmit packet
        # Step 5. show result
        # Step 6. unlock port
        # lock ports
        
        idx_src = int(self.listbox_src.curselection()[0])
        idx_dest = int(self.listbox_dest.curselection()[0])
        # Step 1. lock port
        self.nscmd.port_mark(self.portlist[idx_src].chassis_id, self.portlist[idx_src].board_id, self.portlist[idx_src].port_id)
        self.nscmd.port_mark(self.portlist[idx_dest].chassis_id, self.portlist[idx_dest].board_id, self.portlist[idx_dest].port_id)
        self.logbox.insert(tk.END, "lock ports\n")
        if (self.nscmd.port_lock() == 0):
            self.logbox.insert(tk.END, "lock port1 fail!\n")
            self.nscmd.server_disconnect()
        port1_idx = self.nscmd.get_portidx(self.portlist[idx_src].chassis_id, self.portlist[idx_src].board_id, self.portlist[idx_src].port_id)
        port2_idx = self.nscmd.get_portidx(self.portlist[idx_dest].chassis_id, self.portlist[idx_dest].board_id, self.portlist[idx_dest].port_id)
        
        # Step 2. read link status and clear counter
        # for correct speed
        self.logbox.insert(tk.END, "read link status and clear counter\n")
        self.nscmd.read_info_link(port1_idx)
        self.nscmd.read_info_link(port2_idx)
        # clear counter before setting
        self.nscmd.clear_counter_port(port1_idx)
        self.nscmd.clear_counter_port(port2_idx)
        
        # Step 3. set config to port
        self.logbox.insert(tk.END, "set configuration to port\n")
        # mac address
        mac_1 = "00:22:A2:%02X:%02X:%02X"%(self.portlist[idx_src].chassis_id, self.portlist[idx_src].board_id, self.portlist[idx_src].port_id)
        mac_2 = "00:22:A2:%02X:%02X:%02X"%(self.portlist[idx_dest].chassis_id, self.portlist[idx_dest].board_id, self.portlist[idx_dest].port_id)
        # start config
        self.nscmd.config_stream_pktlen(int(self.editor_pktlen.get()))
        self.nscmd.config_stream_smac(mac_1)
        self.nscmd.config_stream_dmac(mac_2)
        self.nscmd.config_stream_utilization(float(self.editor_txutil.get()))
        # protocol=1 means layer3, 2 means udp, 0 means layer2
        self.nscmd.config_stream_protocol(0)
        # single stream
        self.nscmd.config_stream_streamnum(1)
        self.nscmd.set_stream(port1_idx, 0)
        self.nscmd.config_tx_txpkts(int(self.editor_pktnum.get()))
        
        self.logbox.insert(tk.END, "start to transmit\n")
        # Step 4. transmit packet
        # 0-means wait for a global transmit command
        self.nscmd.config_tx_isimmediate(1)
        self.nscmd.transmit_pkts(port1_idx)
        time.sleep(1)
        
        self.logbox.insert(tk.END, "show result\n")
        # Step 5. show result
        self.nscmd.read_counter_port_once(port1_idx)
        self.nscmd.read_counter_port_once(port2_idx)
        time.sleep(1)
        #1. Change the state of the widget to NORMAL
        #2. Insert the text, and then
        #3. Change the state back to DISABLED
        self.editor_result_tx.configure(state="normal")
        self.editor_result_tx.delete(0, tk.END)
        tmpstr = "%d" %self.nscmd.get_counter_port(port1_idx, self.nsconst.IDX_PORTCOUNTER_TX_PKT)
        self.editor_result_tx.insert(tk.END, tmpstr)
        self.editor_result_tx.configure(state="disabled")
        self.logbox.insert(tk.END, "Tx : "+tmpstr+"\n")
        self.editor_result_rx.configure(state="normal")
        self.editor_result_rx.delete(0, tk.END)
        tmpstr = "%d" %self.nscmd.get_counter_port(port2_idx, self.nsconst.IDX_PORTCOUNTER_RX_UNICAST)
        self.editor_result_rx.insert(tk.END, tmpstr)
        self.editor_result_rx.configure(state="disabled")
        self.logbox.insert(tk.END, "Rx : "+tmpstr+"\n")
        
        self.logbox.insert(tk.END, "unlock ports\n")
        self.nscmd.port_unlock()
        self.logbox.insert(tk.END, "done...\n")
        
    def doWindowClosing(self):
        if msgbox.askyesno("Quit", "Do you want to quit?"):
            self.logbox.insert(tk.END, "Server disconnecting...\n")
            self.nscmd.server_disconnect()
            self.logbox.insert(tk.END, "OK. Bye~\n")
            self.destroy()
    ##### /functions #####


# draw window
testwin = SampleUIApp()
testwin.mainloop() 