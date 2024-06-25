import tkinter as tk
from tkinter import messagebox, Menu
import time
import configparser
import threading

from lib.ENV_Config import PROFILE_PLOT_SETTING as PROF_PLT_SET
from lib.Chamber_Util import ChamberCmd as ChbCmd

PROGRAM_NAME = "ENV Assist"
CODE_VERSION = "1.0.0"
PYTHON_VERSION = "3.12"
BUILD_DATE = "2024-06-20"

class DbgWindowForm:
    def __init__(self, parent):
        self.parent = parent
        self.flag_dbg_mode = True
        self.keep_running = True
        self.create_debug_window()

    def create_debug_window(self):
        if hasattr(self.parent, 'flag_connect') and self.parent.flag_connect:
            # Define a function to handle window closing
            def on_close():
                self.keep_running = False
                self.flag_dbg_mode = False
                dbg_wnd.destroy()

            def send_command(event=None):
                command = entry_dbg_send.get()
                self.parent.chamber.write(command)
                entry_dbg_send.delete(0, tk.END)

            # Open a new window (Toplevel) for debug mode
            dbg_wnd = tk.Toplevel(self.parent)
            dbg_wnd.title("Debug Mode Window")
            dbg_wnd.geometry("400x300")

            # Create a Text widget for displaying debug information
            frame_read = tk.Frame(dbg_wnd, bg='#303841', bd=2, relief=tk.SUNKEN)
            frame_read.pack(side=tk.TOP, fill=tk.X)
            dbg_textbox = tk.Text(frame_read, bg="#222831", fg="white", insertbackground="white", selectbackground="#4ecca3", selectforeground="white", width=40, height=15)
            dbg_textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            dbg_textbox.config(state=tk.DISABLED)

            # Create a scrollbar and attach it to the Text widget
            scrollbar = tk.Scrollbar(frame_read, orient=tk.VERTICAL, command=dbg_textbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            dbg_textbox.config(yscrollcommand=scrollbar.set)

            frame_send = tk.Frame(dbg_wnd, bg='#303841', bd=2, relief=tk.SUNKEN)
            frame_send.pack(side=tk.BOTTOM, fill=tk.X)
            entry_dbg_send = tk.Entry(frame_send, width=400)
            entry_dbg_send.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

            # Start reading data into the textbox
            self.dbg_reading_start(dbg_textbox)

            entry_dbg_send.bind("<Return>", send_command)

            # Set the protocol to handle window closing event
            dbg_wnd.protocol("WM_DELETE_WINDOW", on_close)
        else:
            messagebox.showwarning("Connect Error", "Please connect to the chamber.")

    def dbg_reading(self, textbox):
        while self.keep_running:
            data = self.parent.chamber.read_until_terminator()
            self.print_to_textbox(textbox, data)

    def print_to_textbox(self, textbox, data):
        if self.keep_running:
            textbox.config(state=tk.NORMAL)
            data_str = str(data)
            if data is not None:
                textbox.insert(tk.END, data_str + '\n')
                textbox.config(state=tk.DISABLED)
                textbox.see(tk.END)

    def dbg_reading_start(self, textbox):
        self.read_thread = threading.Thread(target=self.dbg_reading, args=(textbox,))
        self.read_thread.daemon = True
        self.read_thread.start()

class ChamberCtrl:
    def __init__(self, chamber_ip, chamber_port):
        self.chamber_ip = chamber_ip
        self.chamber_port = chamber_port
        self.chamber = None
        self.flag_connect = False

    def connect_to_chamber(self):
        self.chamber = ChbCmd(self.chamber_ip, self.chamber_port)
        self.flag_connect = self.chamber.connect()
        return self.flag_connect

    def disconnect_chamber(self):
        if self.flag_connect:
            self.chamber.disconnect()
            self.flag_connect = False
        return self.flag_connect

    def chamber_load_prgm(self, prg_num):
        if self.flag_connect:
            if prg_num.isdigit():
                prg_num = int(prg_num)
                if 1 <= prg_num <= 40:
                    prgm_data_parts, prgm_stp_lst = self.chamber.GetProgInfo(prg_num)
                    if prgm_data_parts != "NA:DATA NOT READY":
                        self.chamber.PlotProgProfile(prg_num, prgm_data_parts[1], prgm_stp_lst)
                        return True
                    else:
                        return "Chamber PRGM:{} not setting.".format(prg_num)
                else:
                    return "Program number should be between 1 and 30."
            else:
                return "Invalid program number. Please enter a numeric value."
        return "Not connected"

    def chamber_prgm_run(self, prg_num):
        if self.flag_connect:
            if prg_num.isdigit():
                prg_num = int(prg_num)
                if 1 <= prg_num <= 40:
                    prgm_data_parts, prgm_stp_lst = self.chamber.SetProgRun(prg_num)
                    if prgm_data_parts != "NA:DATA NOT READY":
                        self.chamber.SetProgRun(prg_num)
                        return True
                    else:
                        return "Chamber PRGM:{} not setting.".format(prg_num)
                else:
                    return "Program number should be between 1 and 30."
            else:
                return "Invalid program number. Please enter a numeric value."
        return "Not connected"

class WindowForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_variables() 
        self.init_window()
        self.create_menu()
        self.create_status_frame()
        self.create_connection_frame()
        self.create_monitor_frames()
        self.create_program_frames()
        self.create_constant_frames()
        self.create_operation_frames()
        self.update_status()

    def init_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.chamber_ip = config['setting']['Chamber_IP']

    def init_variables(self):
        self._chamber_port = "57732"
        self.chamber_ctrl = ChamberCtrl(self.chamber_ip, self._chamber_port)
        self.flag_dbg_mode = False

    def init_window(self):
        self.title(f"{PROGRAM_NAME} V{CODE_VERSION}")
        self.geometry("600x520")
        self.configure(background='#303841')
        self.resizable(False, False)

    def create_menu(self):
        self.menubar = Menu(self)
        menu_file = Menu(self.menubar, tearoff=0)
        menu_file.add_command(label="Unused", command=None)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=None)
        self.menubar.add_cascade(label="File", menu=menu_file)

        menu_ctrl = Menu(self.menubar, tearoff=0)
        menu_ctrl.add_command(label="Chb Time Sync", command=None)

        menu_help = Menu(self.menubar, tearoff=0)
        menu_help.add_command(label="Debug mode", command=self.debug_mode)
        menu_help.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=menu_help)
        self.config(menu=self.menubar)

    def create_status_frame(self):
        self.frame_status = tk.Frame(self, bg='#303841', bd=2, relief=tk.SUNKEN)
        self.frame_status.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbl_pc_time = tk.Label(self.frame_status, text="", bg='#303841', fg='white')
        self.lbl_pc_time.pack(side=tk.RIGHT, padx=3, pady=3)

    def create_connection_frame(self):
        self.frame_chamber_connect = tk.Frame(self, bg='#303841')
        self.frame_chamber_connect.pack(side=tk.TOP, fill=tk.BOTH)

        self.canvas_indicator = tk.Canvas(self.frame_chamber_connect, width=20, height=20, bg='#303841', highlightthickness=0)
        self.canvas_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator = self.canvas_indicator.create_oval(2, 2, 18, 18, fill="red")

        self.lbl_chb_connect = tk.Label(self.frame_chamber_connect, text="Chamber Connection:", bg='#303841', fg='white')
        self.lbl_chb_connect.pack(side=tk.LEFT, padx=3, pady=3)
        self.entry_chb_connect = tk.Entry(self.frame_chamber_connect, width=15)
        self.entry_chb_connect.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry_chb_connect.insert(tk.END, self.chamber_ip)
        self.btn_chb_connect = tk.Button(self.frame_chamber_connect, text="Connect", command=self.connect_to_chamber)
        self.btn_chb_connect.pack(side=tk.LEFT, padx=10, pady=10)

    def create_monitor_frames(self):
        self.frame_chamber_title = self.create_frame_title("Chamber Status", 16)
        self.frame_chbst_montitle = self.create_frame_title("Monitor Status", 10)

        self.frame_chb_mon = tk.Frame(self, bg='#303841', bd=2, relief=tk.RAISED)
        self.frame_chb_mon.pack(fill='x')
        self.lbl_chb_time = tk.Label(self.frame_chb_mon, text="Time : 0000-00-00 00:00:00", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_time.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        self.lbl_chb_monlst = [self.create_monitor_label(self.frame_chb_mon) for _ in range(2)]

    def create_program_frames(self):
        self.frame_chbst_prgtitle = self.create_frame_title("Program Status", 10)

        self.frame_chamber_status = tk.Frame(self, bg='#303841', bd=2, relief=tk.RAISED)
        self.frame_chamber_status.pack(fill='x')
        self.lbl_chbst_prg = [self.create_monitor_label(self.frame_chamber_status) for _ in range(3)]

        self.frame_prgload_title = self.create_frame_title("Program Load\t              CONSTANT MODE", 16)

        self.frame_prgload = tk.Frame(self, bg='#303841')
        self.frame_prgload.pack(side=tk.LEFT, fill='y')
        self.frame_prgload_entry = tk.Frame(self.frame_prgload, bg='#303841')
        self.frame_prgload_entry.pack(side=tk.TOP, fill='x')

        self.lbl_prgload = tk.Label(self.frame_prgload_entry, text="PRGM No.", bg='#303841', fg='white', font=("Arial", 10))
        self.lbl_prgload.pack(side=tk.LEFT, padx=3, pady=3)
        self.entry_prgload_num = tk.Entry(self.frame_prgload_entry, width=3)
        self.entry_prgload_num.pack(side=tk.LEFT, padx=3, pady=3)
        self.btn_prgload = tk.Button(self.frame_prgload_entry, text="Load", command=self.chamber_load_prgm)
        self.btn_prgload.pack(side=tk.LEFT, padx=3, pady=3)

        self.btn_prgrun = tk.Button(self.frame_prgload, text="PRGM RUN", command=self.chamber_prgm_run, width=15, height=2)
        self.btn_prgrun.pack(side=tk.TOP, padx=5, pady=5)
        self.btn_prgpause = tk.Button(self.frame_prgload, text="PRGM Pause", command=None, width=15, height=2)
        self.btn_prgpause.pack(side=tk.TOP, padx=5, pady=5)

    def create_constant_frames(self):
        self.frame_chb_const_title = tk.Frame(self, bg='#303841')
        self.frame_chb_const_title.pack(fill='x')

        self.lbl_const_temp = tk.Label(self.frame_chb_const_title, text="  TEMP :", bg='#303841', fg='white', anchor='w', font=("Arial", 10))
        self.lbl_const_temp.pack(side=tk.LEFT, padx=3, pady=3, fill='x')
        self.entry_const_temp = tk.Entry(self.frame_chb_const_title, width=4)
        self.entry_const_temp.pack(side=tk.LEFT, padx=3, pady=3)
        self.lbl_const_humi = tk.Label(self.frame_chb_const_title, text="HUMI :", bg='#303841', fg='white', anchor='w', font=("Arial", 10))
        self.lbl_const_humi.pack(side=tk.LEFT, padx=3, pady=3, fill='x')
        self.entry_const_humi = tk.Entry(self.frame_chb_const_title, width=4)
        self.entry_const_humi.pack(side=tk.LEFT, padx=3, pady=3)
        self.btn_const_mode = tk.Button(self.frame_chb_const_title, text="MODE:CONSTANT", command=None, width=30)
        self.btn_const_mode.pack(side=tk.LEFT, padx=3, pady=3, expand=True)

    def create_operation_frames(self):
        self.frame_chb_opreate = tk.Frame(self, bg='#303841')
        self.frame_chb_opreate.pack(side=tk.TOP, fill='x', ipadx=100)

        self.lbl_chb_const_title = tk.Label(self.frame_chb_opreate, text="Chamber OPERATE", bg='#303841', fg='white', anchor='center', font=("Arial", 16))
        self.lbl_chb_const_title.pack(side=tk.TOP, padx=3, pady=15, fill='x', expand=True)

        # Create a grid layout for the buttons
        self.btn_poweron = tk.Button(self.frame_chb_opreate, text="Power On", command=None, width=15, height=2, bg='#00FF00')
        self.btn_poweron.pack(side=tk.LEFT, padx=15)

        self.btn_mode_stby = tk.Button(self.frame_chb_opreate, text="Mode:Standby", command=None, width=15, height=2, bg='#FFEB99')
        self.btn_mode_stby.pack(side=tk.LEFT, padx=15)

        self.btn_poweroff = tk.Button(self.frame_chb_opreate, text="Power Off", command=None, width=15, height=2, bg='#FF0000', font = ("Arial", 9, "bold"))
        self.btn_poweroff.pack(side=tk.LEFT, padx=15)

    def create_frame_title(self, text, font_size):
        frame = tk.Frame(self, bg='#303841')
        frame.pack(fill='x')
        lbl = tk.Label(frame, text=text, bg='#303841', fg='white', font=("Arial", font_size))
        lbl.pack(side=tk.LEFT, padx=3, pady=3)
        return frame

    def create_monitor_label(self, parent):
        lbl = tk.Label(parent, text="", bg='#303841', fg='white', anchor='w')
        lbl.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        return lbl

    def connect_to_chamber(self):
        self.chamber_ctrl.chamber_ip = self.entry_chb_connect.get()
        if self.chamber_ctrl.connect_to_chamber():
            self.btn_chb_connect.config(state=tk.DISABLED)
            self.entry_chb_connect.config(state=tk.DISABLED, bg='#303841')
            self.update_indicator(True)
        else:
            self.update_indicator(False)

    def disconnect_chamber(self):
        if self.chamber_ctrl.disconnect_chamber():
            self.update_indicator(False)

    def check_chamber(self):
        try:
            return self.chamber_ctrl.chamber.CheckConnection()
        except Exception as e:
            print(f"An error occurred while checking chamber connection: {e}")
            return False

    def update_indicator(self, status):
        color = "green" if status else "red"
        self.canvas_indicator.itemconfig(self.indicator, fill=color)

    def update_status(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.lbl_pc_time.config(text=f" {current_time}")
        
        if not self.chamber_ctrl.flag_connect or self.flag_dbg_mode:
            self.after(1000, self.update_status)
            return

        try:
            if not self.check_chamber():
                self.update_indicator(False)
                print("Chamber is disconnected. Updating flag and UI.")
                self.chamber_ctrl.flag_connect = False
                self.btn_chb_connect.config(state=tk.NORMAL)
                self.entry_chb_connect.config(state=tk.NORMAL, bg='white')
                messagebox.showwarning("Connection Lost", "The connection to the chamber has been lost.")
                self.after(1000, self.update_status)
                return

            chb_time_str = self.chamber_ctrl.chamber.GetChbTime()
            self.lbl_chb_time.config(text=f"Time : {chb_time_str}")

            chbst_prgnum = self.chamber_ctrl.chamber.GetProgStat()
            chbst_prgset = self.chamber_ctrl.chamber.GetProgSet()
            chbst_mon = self.chamber_ctrl.chamber.GetCondition()

            self.lbl_chb_monlst[0].config(text=f"Measure Temp : {chbst_mon[0]}\t\t Measure Humi : {chbst_mon[1]}")
            self.lbl_chb_monlst[1].config(text=f"Mode : {chbst_mon[2]}\t\t Alarms : {chbst_mon[3]}")

            self.lbl_chbst_prg[0].config(text=f"PRG No.{chbst_prgset[0]}\t\t PRG Name: {chbst_prgset[1]} \t\t {chbst_prgnum[3]}")
            self.lbl_chbst_prg[1].config(text=f"Step {chbst_prgnum[0]} / {chbst_prgnum[1]} \t\t Repeat {chbst_prgnum[2]}")
            self.lbl_chbst_prg[2].config(text=f"Temp: {chbst_prgset[2]} / {chbst_prgset[4]} \t\t Humi: {chbst_prgset[3]} / {chbst_prgset[5]}")

        except Exception as e:
            print(f"An error occurred while updating status: {e}")

        finally:
            self.after(1000, self.update_status)

    '''
    def update_status(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.lbl_pc_time.config(text=f" {current_time}")
        if self.chamber_ctrl.flag_connect and not self.flag_dbg_mode:
            if self.check_chamber():
                self.update_indicator(True)
            else:
                self.update_indicator(False)
                print("Chamber is disconnected. Updating flag and UI.")
                self.chamber_ctrl.flag_connect = False
                self.btn_chb_connect.config(state=tk.NORMAL)
                self.entry_chb_connect.config(state=tk.NORMAL, bg='white')
                messagebox.showwarning("Connection Lost", "The connection to the chamber has been lost.")
                return

        try:
            chb_time_str = self.chamber_ctrl.chamber.GetChbTime()
            self.lbl_chb_time.config(text=f"Time : {chb_time_str}")

            chbst_prgnum = self.chamber_ctrl.chamber.GetProgStat()
            chbst_prgset = self.chamber_ctrl.chamber.GetProgSet()
            chbst_mon = self.chamber_ctrl.chamber.GetCondition()

            self.lbl_chb_monlst[0].config(text=f"Measure Temp : {chbst_mon[0]}\t\t Measure Humi : {chbst_mon[1]}")
            self.lbl_chb_monlst[1].config(text=f"Mode : {chbst_mon[2]}\t\t Alarms : {chbst_mon[3]}")

            self.lbl_chbst_prg[0].config(text=f"PRG No.{chbst_prgset[0]}\t\t PRG Name: {chbst_prgset[1]} \t\t {chbst_prgnum[3]}")
            self.lbl_chbst_prg[1].config(text=f"Step {chbst_prgnum[0]} / {chbst_prgnum[1]} \t\t Repeat {chbst_prgnum[2]}")
            self.lbl_chbst_prg[2].config(text=f"Temp: {chbst_prgset[2]} / {chbst_prgset[4]} \t\t Humi: {chbst_prgset[3]} / {chbst_prgset[5]}")

        except Exception as e:
            print(f"An error occurred while updating status: {e}")

        self.after(1000, self.update_status)
    '''

    def chamber_load_prgm(self):
        prg_num = self.entry_prgload_num.get()
        result = self.chamber_ctrl.chamber_load_prgm(prg_num)
        if result is not True:
            messagebox.showwarning("Program Load Error", result)

    def chamber_prgm_run(self):
        prg_num = self.entry_prgload_num.get()
        result = self.chamber_ctrl.chamber_prgm_run(prg_num)
        if result is not True:
            messagebox.showwarning("Program Run Error", result)

    def chamber_prgm_pause(self):
        result = self.chamber_ctrl.chamber_prgm_pause()
        if result is not True:
            messagebox.showwarning("Program Pause Error", result)

    def debug_mode(self):
        self.debug_window = DbgWindowForm(self.chamber_ctrl.flag_connect)

    def about(self):
        messagebox.showinfo(f"About {PROGRAM_NAME}", f"{PROGRAM_NAME} V{CODE_VERSION} \n {BUILD_DATE}")

if __name__ == "__main__":
    app = WindowForm()
    app.mainloop()
