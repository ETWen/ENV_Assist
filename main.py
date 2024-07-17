import tkinter as tk
from tkinter import messagebox, Menu, ttk
import time
import configparser
import threading

from lib.ENV_Config import PROFILE_PLOT_SETTING as PROF_PLT_SET
from lib.Chamber_Util import ChamberCmd as ChbCmd
from lib.NuStream_Util import NustreamCmd as NsCmd

import ChamberForm as ChbForm
import NuStreamForm as NustmForm
import PDUForm as PduForm

PROGRAM_NAME = "ENV Assist"
CODE_VERSION = "1.0.1"
PYTHON_VERSION = "3.12"
BUILD_DATE = "2024-06-20"

class SummaryFrame(tk.Frame):
    def __init__(self, master=None,chamber_frame=None,nustream_frame=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.chamber_frame = chamber_frame
        self.nustream_frame = nustream_frame
        self.init_frame()
        self.create_connection_frame()

    def init_frame(self):
        self.configure(background='#303841')
        self.pack(fill=tk.BOTH, expand=True)

    def create_connection_frame(self):
        self.frame_dev_connect = tk.Frame(self, bg='#303841')
        self.frame_dev_connect.pack(side=tk.TOP, fill=tk.BOTH)

        self.frame_dev_chb = tk.Frame(self, bg='#303841')
        self.frame_dev_chb.pack(side=tk.TOP, fill=tk.BOTH)
        self.dev_chb_indicator = tk.Canvas(self.frame_dev_chb, width=20, height=20, bg='#303841', highlightthickness=0)
        self.dev_chb_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator_chb = self.dev_chb_indicator.create_oval(2, 2, 18, 18, fill="red")
        self.lbl_dev_chb = tk.Label(self.frame_dev_chb, text="Instrument Chamber", bg='#303841', fg='white', font=("Arial", 10), anchor='w')
        self.lbl_dev_chb.pack(side=tk.TOP, padx=3, pady=3, fill='x')

        self.frame_dev_nustm = tk.Frame(self, bg='#303841')
        self.frame_dev_nustm.pack(side=tk.TOP, fill=tk.BOTH)
        self.dev_nustm_indicator = tk.Canvas(self.frame_dev_nustm, width=20, height=20, bg='#303841', highlightthickness=0)
        self.dev_nustm_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator_nustm = self.dev_nustm_indicator.create_oval(2, 2, 18, 18, fill="red")
        self.lbl_dev_nustm = tk.Label(self.frame_dev_nustm, text="Instrument NuStream", bg='#303841', fg='white', font=("Arial", 10), anchor='w')
        self.lbl_dev_nustm.pack(side=tk.TOP, padx=3, pady=3, fill='x')

        self.frame_dev_pdu = tk.Frame(self, bg='#303841')
        self.frame_dev_pdu.pack(side=tk.TOP, fill=tk.BOTH)
        self.dev_pdu_indicator = tk.Canvas(self.frame_dev_pdu, width=20, height=20, bg='#303841', highlightthickness=0)
        self.dev_pdu_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator_pdu = self.dev_pdu_indicator.create_oval(2, 2, 18, 18, fill="red")
        self.lbl_dev_pdu = tk.Label(self.frame_dev_pdu, text="Instrument PDU", bg='#303841', fg='white', font=("Arial", 10), anchor='w')
        self.lbl_dev_pdu.pack(side=tk.TOP, padx=3, pady=3, fill='x')

    def update_dev_indicator(self):
        if self.chamber_frame:
            chamber_status = self.chamber_frame.get_indicator_status()
            self.dev_chb_indicator.itemconfig(self.indicator_chb, fill=chamber_status)
        if self.nustream_frame:
            nustream_status = self.nustream_frame.get_indicator_status()
            self.dev_nustm_indicator.itemconfig(self.indicator_nustm, fill=nustream_status)

class CombinedStatusUpdater:
    def __init__(self, window_form , summary_frame, chamber_frame,nustream_frame,pdu_frame):
        self.window_form = window_form
        self.summary_frame = summary_frame
        self.chamber_frame = chamber_frame
        self.nustream_frame = nustream_frame
        self.pdu_frame = pdu_frame
        self.keep_running = True

    def start(self):
        self.update_chamber_thread = threading.Thread(target=self.update_chamber_status)
        self.update_chamber_thread.daemon = True
        self.update_chamber_thread.start()

        self.nustream_conn_update_thread = threading.Thread(target=self.update_nustream_connect_status)
        self.nustream_conn_update_thread.daemon = True
        self.nustream_conn_update_thread.start()

        self.nustream_update_thread = threading.Thread(target=self.update_nustream_status)
        self.nustream_update_thread.daemon = True
        self.nustream_update_thread.start()

        self.nustream_sum_conn_thread = threading.Thread(target=self.update_sum_conn_status)
        self.nustream_sum_conn_thread.daemon = True
        self.nustream_sum_conn_thread.start()

    def update_chamber_status(self):
        while self.keep_running:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.window_form.lbl_pc_time.config(text=f" {current_time}")
            self.chamber_frame.update_status()
            time.sleep(1)

    def update_nustream_connect_status(self):
        while self.keep_running:
            self.nustream_frame.update_connect_status()
            time.sleep(1)

    def update_nustream_status(self):
        while self.keep_running:
            self.nustream_frame.update_status()
            time.sleep(1)

    def update_sum_conn_status(self):
        while self.keep_running:
            self.summary_frame.update_dev_indicator()
            time.sleep(1)


    def stop(self):
        self.keep_running = False

class WindowForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_variables() 
        self.init_window()
        self.create_menu()
        self.create_status_frame()
        self.create_notebook()

    def init_variables(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.chamber_ip = config['setting']['Chamber_IP']
        self._chamber_port = "57732"
        self.chamber_ctrl = ChbForm.ChamberCtrl()
        self.nustm_ip = config['setting']['NuStream_IP']
        self.pdu_ip = config['setting']['PDU_IP']
        #self.nustm_pkt_len = config['Nustream CONFIG']['pkt_len']
        #self.nustm_utilization = config['Nustream CONFIG']['pkt_len']

    def init_window(self):
        self.title(f"{PROGRAM_NAME} V{CODE_VERSION}")
        self.geometry("600x650")
        self.configure(background='#303841')
        self.minsize(600, 650)
        #self.resizable(False, False)

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
        menu_help.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=menu_help)
        self.config(menu=self.menubar)

    def create_status_frame(self):
        self.frame_status = tk.Frame(self, bg='#303841', bd=2, relief=tk.SUNKEN)
        self.frame_status.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbl_pc_time = tk.Label(self.frame_status, text="", bg='#303841', fg='white')
        self.lbl_pc_time.pack(side=tk.RIGHT, padx=3, pady=3)

    def create_notebook(self):
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

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.nb_summary = tk.Frame(self.notebook, bg='#303841')
        self.nb_chamber = tk.Frame(self.notebook, bg='#303841')
        self.nb_nustream = tk.Frame(self.notebook, bg='#303841')
        self.nb_pdu = tk.Frame(self.notebook, bg='#303841')

        self.notebook.add(self.nb_summary, text='Summary')
        self.notebook.add(self.nb_chamber, text='Chamber')
        self.notebook.add(self.nb_nustream, text='NuStream')
        self.notebook.add(self.nb_pdu, text='PDU')

        self.chamber_frame = ChbForm.ChamberFrame(self.nb_chamber, self.chamber_ip)
        self.chamber_frame.pack(expand=True, fill='both')

        self.nustream_frame = NustmForm.NuStreamFrame(self.nb_nustream, self.nustm_ip)
        self.nustream_frame.pack(expand=True, fill='both')

        self.pdu_frame = PduForm.PduFrame(self.nb_pdu, self.pdu_ip)
        self.pdu_frame.pack(expand=True, fill='both')

        self.summary_frame = SummaryFrame(self.nb_summary,chamber_frame=self.chamber_frame ,nustream_frame=self.nustream_frame)
        self.summary_frame.pack(expand=True, fill='both')

    def update_chamber_status(self, status_info):
        self.chamber_frame.update_status(status_info)

    def about(self):
        messagebox.showinfo(f"About {PROGRAM_NAME}", f"{PROGRAM_NAME} V{CODE_VERSION} \n {BUILD_DATE}")


if __name__ == "__main__":
    root = WindowForm()

    updater = CombinedStatusUpdater(root, root.summary_frame, root.chamber_frame, root.nustream_frame, root.pdu_frame)
    updater.start()

    root.mainloop()
    updater.stop()