import tkinter as tk
from tkinter import messagebox, ttk

from lib.Chamber_Util import ChamberCmd as ChbCmd

def create_notebook(root):
    style = ttk.Style()
    style.theme_create('custom_theme', parent='alt', settings={
        'TNotebook': {
            'configure': {
                'tabmargins': [2, 5, 2, 0]
            }
        },
        'TNotebook.Tab': {
            'configure': {
                'padding': [5, 1],
                'background': '#4F565E',
                'foreground': '#C6C2C4'
            },
            'map': {
                'background': [('selected', '#303841')],
                'foreground': [('selected', 'white')],
                'expand': [('selected', [1, 1, 1, 0])]
            }
        }
    })
    style.theme_use('custom_theme')

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    chamber_ip = "127.0.0.1"
    chamber_frame = ChamberFrame(notebook, chamber_ip=chamber_ip)
    notebook.add(chamber_frame, text='Chamber')

class ChamberFrame(tk.Frame):
    def __init__(self, master=None, chamber_ip="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.chamber_ctrl = ChamberCtrl(chamber_ip)
        self.chamber_ip = chamber_ip
        self.init_frame()
        self.create_connection_frame()
        self.create_monitor_frames()
        self.create_program_frames()
        self.create_chamber_ctrl_frames()
        self.create_constant_frames()
        self.create_operation_frames()

    def init_frame(self):
        self.configure(background='#303841')
        self.pack(fill=tk.BOTH, expand=True)

    def create_connection_frame(self):
        self.frame_chamber_connect = tk.Frame(self, bg='#303841')
        self.frame_chamber_connect.pack(side=tk.TOP, fill=tk.BOTH)

        self.chb_conn_indicator = tk.Canvas(self.frame_chamber_connect, width=20, height=20, bg='#303841', highlightthickness=0)
        self.chb_conn_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator = self.chb_conn_indicator.create_oval(2, 2, 18, 18, fill="red")

        self.lbl_chb_connect = tk.Label(self.frame_chamber_connect, text="Chamber Connection:", bg='#303841', fg='white')
        self.lbl_chb_connect.pack(side=tk.LEFT, padx=3, pady=3)
        self.entry_chb_connect = tk.Entry(self.frame_chamber_connect, width=15)
        self.entry_chb_connect.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry_chb_connect.insert(tk.END, self.chamber_ip)
        self.btn_chb_connect = tk.Button(self.frame_chamber_connect, text="Connect", command=self.update_chamber_ip)
        self.btn_chb_connect.pack(side=tk.LEFT, padx=10, pady=10)
        #self.btn_chb_disconnect = tk.Button(self.frame_chamber_connect, text="Disconnect", command=self.chamber_ctrl.disconnect_chamber)
        #self.btn_chb_disconnect.pack(side=tk.LEFT, padx=10, pady=10)

    def get_indicator_status(self):
        return self.chb_conn_indicator.itemcget(self.indicator, "fill")

    def create_monitor_frames(self):
        self.frame_chamber_title = self.create_frame_title("Chamber Status", 16)
        self.frame_chbst_montitle = self.create_frame_title("Monitor Status", 10)
        self.frame_chb_mon = tk.Frame(self, bg='#303841', bd=2, relief=tk.RAISED)
        self.frame_chb_mon.pack(fill='x')
        self.lbl_chb_time = tk.Label(self.frame_chb_mon, text="Time : 0000-00-00 00:00:00", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_time.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        self.lbl_chb_meas_temp_humi = tk.Label(self.frame_chb_mon, text=f"Measure Temp : --\t\t Measure Humi : --", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_meas_temp_humi.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        self.lbl_chb_status = tk.Label(self.frame_chb_mon, text=f"Mode : --\t\t\t Alarms : --", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_status.pack(side=tk.TOP, padx=3, pady=3, fill='x')

    def create_program_frames(self):
        self.frame_chbst_prgtitle = self.create_frame_title("Program Status", 10)

        self.frame_chamber_status = tk.Frame(self, bg='#303841', bd=2, relief=tk.RAISED)
        self.frame_chamber_status.pack(fill='x')

        self.lbl_chb_prg1 = tk.Label(self.frame_chamber_status, text=f"PRG No.-\t\t PRG Name: - \t\t -", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_prg1.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        self.lbl_chb_prg2 = tk.Label(self.frame_chamber_status, text=f"Step -- / -- \t\t Repeat --", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_prg2.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        self.lbl_chb_prg3 = tk.Label(self.frame_chamber_status, text=f"Temp: -- / -- \t\t Humi: -- / --", bg='#303841', fg='white', anchor='w')
        self.lbl_chb_prg3.pack(side=tk.TOP, padx=3, pady=3, fill='x')

    def create_chamber_ctrl_frames(self):
        self.frame_chamber_ctrl = tk.Frame(self, bg='#303841')
        self.frame_chamber_ctrl.pack(side=tk.TOP, fill=tk.BOTH)
        self.lbl_chamber_ctrl_title = tk.Label(self.frame_chamber_ctrl, text="Chamber Ctrl", bg='#303841', fg='white', font=("Arial", 16), anchor='w')
        self.lbl_chamber_ctrl_title.pack(side=tk.TOP, padx=3, pady=3, fill='x')
        self.lbl_prg_load_title = tk.Label(self.frame_chamber_ctrl, text="Program Load", bg='#303841', fg='white', font=("Arial", 10), anchor='w')
        self.lbl_prg_load_title.pack(side=tk.TOP, padx=3, pady=3, fill='x')

        self.frame_prg_ctrl = tk.Frame(self.frame_chamber_ctrl, bg='#303841')
        self.frame_prg_ctrl.pack(side=tk.TOP, fill=tk.BOTH)

        self.lbl_prgload = tk.Label(self.frame_prg_ctrl, text="PRGM No.", bg='#303841', fg='white', font=("Arial", 10))
        self.lbl_prgload.pack(side=tk.LEFT, padx=10, pady=3)
        self.entry_prgload_num = tk.Entry(self.frame_prg_ctrl, width=3)
        self.entry_prgload_num.pack(side=tk.LEFT, padx=1, pady=3)
        self.btn_prgload = tk.Button(self.frame_prg_ctrl, text="Load", command=self.update_chamber_loadprgm)
        self.btn_prgload.pack(side=tk.LEFT, padx=10, pady=3)
        self.btn_prgrun = tk.Button(self.frame_prg_ctrl, text="PRGM RUN", command=self.update_chamber_runprgm, width=15, height=2)
        self.btn_prgrun.pack(side=tk.LEFT, padx=10, pady=5)
        self.btn_prgpause = tk.Button(self.frame_prg_ctrl, text="PRGM Pause", command=self.update_chamber_pauseprgm, width=15, height=2)
        self.btn_prgpause.pack(side=tk.LEFT, padx=10, pady=5)

    def create_constant_frames(self):
        self.lbl_const_title = tk.Label(self.frame_chamber_ctrl, text="CONSTANT Control", bg='#303841', fg='white', font=("Arial", 10), anchor='w')
        self.lbl_const_title.pack(side=tk.TOP, padx=3, pady=3, fill='x')

        self.frame_const_ctrl = tk.Frame(self.frame_chamber_ctrl, bg='#303841')
        self.frame_const_ctrl.pack(side=tk.TOP, fill=tk.BOTH)
        self.lbl_const_temp = tk.Label(self.frame_const_ctrl, text="  TEMP :", bg='#303841', fg='white', anchor='w', font=("Arial", 10))
        self.lbl_const_temp.pack(side=tk.LEFT, padx=3, pady=3, fill='x')
        self.entry_const_temp = tk.Entry(self.frame_const_ctrl, width=4)
        self.entry_const_temp.pack(side=tk.LEFT, padx=3, pady=3)
        self.entry_const_temp.insert(tk.END, "25")
        self.lbl_const_humi = tk.Label(self.frame_const_ctrl, text="HUMI :", bg='#303841', fg='white', anchor='w', font=("Arial", 10))
        self.lbl_const_humi.pack(side=tk.LEFT, padx=3, pady=3, fill='x')
        self.entry_const_humi = tk.Entry(self.frame_const_ctrl, width=4)
        self.entry_const_humi.pack(side=tk.LEFT, padx=3, pady=3)
        self.btn_const_mode = tk.Button(self.frame_const_ctrl, text="MODE:CONSTANT", command=self.update_chamber_runconst, width=30)
        self.btn_const_mode.pack(side=tk.LEFT, padx=3, pady=3)

    def create_operation_frames(self):
        self.frame_chb_opreate = tk.Frame(self.frame_chamber_ctrl, bg='#303841')
        self.frame_chb_opreate.pack(side=tk.TOP, fill='x', ipadx=100)

        self.lbl_chb_const_title = tk.Label(self.frame_chb_opreate, text="Chamber OPERATE", bg='#303841', fg='white', anchor='w', font=("Arial", 10))
        self.lbl_chb_const_title.pack(side=tk.TOP, padx=3, pady=15, fill='x', expand=True)

        # Create a grid layout for the buttons
        self.btn_poweron = tk.Button(self.frame_chb_opreate, text="Power On", command=self.update_operate_poweron, width=15, height=2, bg='#00FF00')
        self.btn_poweron.pack(side=tk.LEFT, padx=15)

        self.btn_mode_stby = tk.Button(self.frame_chb_opreate, text="Mode:Standby", command=self.update_operate_standby, width=15, height=2, bg='#FFEB99')
        self.btn_mode_stby.pack(side=tk.LEFT, padx=15)

        self.btn_poweroff = tk.Button(self.frame_chb_opreate, text="Power Off", command=self.update_operate_poweroff, width=15, height=2, bg='#FF0000', font = ("Arial", 9, "bold"))
        self.btn_poweroff.pack(side=tk.LEFT, padx=15)

    def create_frame_title(self, text, font_size):
        frame = tk.Frame(self, bg='#303841')
        frame.pack(fill='x')
        lbl = tk.Label(frame, text=text, bg='#303841', fg='white', font=("Arial", font_size))
        lbl.pack(side=tk.LEFT, padx=3, pady=3)
        return frame

    def update_status(self):
        #print("Update Chamber Frame")
        self.chamber_ctrl.chamber_flag = self.chamber_ctrl.check_chamber()
        
        color = "green" if self.chamber_ctrl.chamber_flag else "red"
        self.chb_conn_indicator.itemconfig(self.indicator, fill=color)

        if self.chamber_ctrl.chamber_flag:
            self.btn_chb_connect.config(state=tk.DISABLED)
            self.entry_chb_connect.config(state=tk.DISABLED, bg='#303841')
        else:
            self.btn_chb_connect.config(state=tk.NORMAL)
            self.entry_chb_connect.config(state=tk.NORMAL, bg='white')

    def update_chamber_ip(self):
        new_chamber_ip = self.entry_chb_connect.get()               # Get entry IP
        result = self.chamber_ctrl.connect_to_chamber(new_chamber_ip)        # Send the IP to class ChamberCtrl

    def update_chamber_loadprgm(self):
        new_chamber_prgmno = self.entry_prgload_num.get()
        result = self.chamber_ctrl.chamber_load_prgm(new_chamber_prgmno)
        if result is not True:
            messagebox.showwarning("Program Load Error", result)


    def update_chamber_runprgm(self):
        new_chamber_prgmno = self.entry_prgload_num.get()
        result = self.chamber_ctrl.chamber_prgm_run(new_chamber_prgmno)
        if result is not True:
            messagebox.showwarning("Program Run Error", result)

    def update_chamber_pauseprgm(self):
        result = self.chamber_ctrl.chamber_prgm_pause()
        if result is not True:
            messagebox.showwarning("Program Pause Error", result)

    def update_chamber_runconst(self):
        new_chamber_const_temp = self.entry_const_temp.get()
        new_chamber_const_humi = self.entry_const_humi.get()
        result = self.chamber_ctrl.chamber_constant_run(new_chamber_const_temp,new_chamber_const_humi)
        if result is not True:
            messagebox.showwarning("Constant Run Error", result)

    def update_operate_poweron(self):
        result = self.chamber_ctrl.chamber_operate_poweron()
        if result is not True:
            messagebox.showwarning("Chamber Operate Error", result)

    def update_operate_standby(self):
        result = self.chamber_ctrl.chamber_operate_standby()
        if result is not True:
            messagebox.showwarning("Chamber Operate Error", result)

    def update_operate_poweroff(self):
        result = self.chamber_ctrl.chamber_operate_poweroff()
        if result is not True:
            messagebox.showwarning("Chamber Operate Error", result)

class ChamberCtrl:
    def __init__(self,chamber_ip=""):
        self._chamber_port = "57732"
        self.chamber_ip = chamber_ip
        self.chamber_flag = False
        self.chamber_cmd = ChbCmd(self.chamber_ip,self._chamber_port)

    def connect_to_chamber(self,new_ip):
        self.chamber_ip = new_ip
        self.chamber_cmd = ChbCmd(self.chamber_ip, self._chamber_port)
        self.chamber_cmd.connect()

    def disconnect_chamber(self):
        print("Disconnecting from chamber...")

    def check_chamber(self):
        try:
            return self.chamber_cmd.CheckConnection()
            #return True
        except Exception as e:
            self.chamber_flag = self.chamber_cmd.CheckConnection()
            print(f"An error occurred while checking chamber connection: {e}")
            return False

    def chamber_load_prgm(self,new_prgmno):
        print("Load Program from chamber...")
        if not self.chamber_flag:
            return "Not Connect"
        if not new_prgmno.isdigit():
            return "Invalid program number. Please enter a numeric value."

        new_prgmno = int(new_prgmno)
        if not (1 <= new_prgmno <= 40):
            return "Program number should be between 1 and 40."

        try:
            prgm_data_parts, prgm_stp_lst = self.chamber_cmd.GetProgInfo(new_prgmno)
        except Exception as e:
            return f"Illegal data. Please check the data response from chamber. PRGM DATA?, RAM:{new_prgmno}"

        if prgm_data_parts == "NA:DATA NOT READY":
            return f"Chamber PRGM:{new_prgmno} not setting."
        self.chamber_cmd.PlotProgProfile(new_prgmno, prgm_data_parts[1], prgm_stp_lst)
        return True

    def chamber_prgm_run(self,new_prgmno):
        print("Run Program from chamber...")
        if not self.chamber_flag:
            return "Not Connect"
        if not new_prgmno.isdigit():
            return "Invalid program number. Please enter a numeric value."

        new_prgmno = int(new_prgmno)
        if not (1 <= new_prgmno <= 40):
            return "Program number should be between 1 and 40."

        response = self.chamber_cmd.SetProgRun(new_prgmno)
        if response == "NA:DATA NOT READY":
            return f"Chamber PRGM:{new_prgmno} not setting."
        return True

    def chamber_prgm_pause(self):
        print("Pause Program from chamber...")
        if not self.chamber_flag:
            return "Not Connect"
        self.chamber_cmd.SetProgPause()
        return True

    def chamber_constant_run(self,const_temp,const_humi):
        print("Run Mode Constant...")
        if not self.chamber_flag:
            return "Not Connect"
        if not const_temp.isdigit() or (const_humi and not const_humi.isdigit()):
            return "Invalid temperature or humidity. Please enter numeric values."
        const_temp = int(const_temp)
        const_humi = int(const_humi) if const_humi else None
        if not (-45 <= const_temp <= 100):
            return "Temp should be -45 - 100C"
        if const_humi is None:
            print("Temp")
            self.chamber_cmd.SetConstTempRun(const_temp)
            return True
        if 0 <= const_humi <= 100:
            print("Temp + Humi")
            self.chamber_cmd.SetConstTempRun(const_temp)
            self.chamber_cmd.SetConstHumiRun(const_humi)
            return True
        return "Humi should be 0% - 100%"

    def chamber_operate_poweron(self):
        print("Operate Mode PowerOn...")
        if not self.chamber_flag:
            return "Not Connect"

    def chamber_operate_standby(self):
        print("Operate Mode Standby...")
        if not self.chamber_flag:
            return "Not Connect"

    def chamber_operate_poweroff(self):
        print("Operate Mode PowerOff...")
        if not self.chamber_flag:
            return "Not Connect"



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("600x620")
    root.configure(background='#303841')
    #root.resizable(False, False)
    #root.state('zoomed')

    create_notebook(root)

    root.mainloop()