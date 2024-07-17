import os
import tkinter as tk
from tkinter import messagebox, ttk

from lib.PDUutils import PDUCtrl as PduCmd

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
    pdu_ip = "192.168.1.20"
    pdu_frame = PduFrame(notebook, pdu_ip=pdu_ip)
    notebook.add(pdu_frame, text='PDU')

class PduFrame(tk.Frame):
    def __init__(self, master=None, pdu_ip="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pdu_ip = pdu_ip
        self.init_frame()
        self.create_connection_frame()

    def init_frame(self):
        self.configure(background='#303841')
        self.pack(fill=tk.BOTH, expand=True)

    def create_connection_frame(self):
        self.frame_pdu_connect = tk.Frame(self, bg='#303841')
        self.frame_pdu_connect.pack(side=tk.TOP, fill=tk.BOTH)

        self.pdu_conn_indicator = tk.Canvas(self.frame_pdu_connect, width=20, height=20, bg='#303841', highlightthickness=0)
        self.pdu_conn_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator = self.pdu_conn_indicator.create_oval(2, 2, 18, 18, fill="red")

        self.lbl_pdu_connect = tk.Label(self.frame_pdu_connect, text="NuStream Connection:", bg='#303841', fg='white')
        self.lbl_pdu_connect.pack(side=tk.LEFT, padx=3, pady=3)
        self.entry_pdu_connect = tk.Entry(self.frame_pdu_connect, width=15)
        self.entry_pdu_connect.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry_pdu_connect.insert(tk.END, self.pdu_ip)
        self.btn_pdu_connect = tk.Button(self.frame_pdu_connect, text="Connect", command=self.update_pdu_ip)
        self.btn_pdu_connect.pack(side=tk.LEFT, padx=10, pady=10)

    def update_pdu_ip(self):
        new_pdu_ip = self.entry_pdu_connect.get()
        #result = self.nustm_ctrl.connect_to_nustm(new_nustm_ip)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Summary Window")
    root.geometry("600x520")
    root.configure(background='#303841')
    root.resizable(False, False)

    create_notebook(root)

    root.mainloop()