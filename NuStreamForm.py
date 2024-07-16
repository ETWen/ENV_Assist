import os
import tkinter as tk
from tkinter import messagebox, ttk

from lib.NuStream_Util import NustreamCmd as NsCmd
from PIL import Image, ImageTk

import datetime

import win32gui
import win32ui
import win32con
import pygetwindow as gw
from ctypes import windll

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
    nustm_ip = "192.168.1.8"
    nustm_frame = NuStreamFrame(notebook, nustm_ip=nustm_ip)
    notebook.add(nustm_frame, text='NuStream')

class NuStreamFrame(tk.Frame):
    def __init__(self, master=None, nustm_ip="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.nustm_ip = nustm_ip
        self.nustm_ctrl = NuStreamCtrl(nustm_ip)
        self.locked_items = []
        self.locked_ports_cbp_id = []
        self.locked_ports_idx = []
        self.init_frame()
        self.load_resource()
        self.create_connection_frame()
        self.create_btn_ctrl_frame()
        self.create_show_lock_ports()

    def init_frame(self):
        self.configure(background='#303841')
        self.pack(fill=tk.BOTH, expand=True)

    def load_resource(self):
        base_dir = os.path.dirname(__file__)
        img_reserve_btn_path = os.path.join(base_dir, "resource", "img_reserve_btn.png")
        img_reserve_btn = Image.open(img_reserve_btn_path).resize((20, 20), Image.LANCZOS)
        self.img_reserve_btn = ImageTk.PhotoImage(img_reserve_btn)

        img_clear_btn_path = os.path.join(base_dir, "resource", "img_clear_btn.png")
        img_clear_btn = Image.open(img_clear_btn_path).resize((20, 20), Image.LANCZOS)
        self.img_clear_btn = ImageTk.PhotoImage(img_clear_btn)

        img_start_btn_path = os.path.join(base_dir, "resource", "img_start_btn.png")
        img_start_btn = Image.open(img_start_btn_path).resize((20, 20), Image.LANCZOS)
        self.img_start_btn = ImageTk.PhotoImage(img_start_btn)


        img_stop_btn_path = os.path.join(base_dir, "resource", "img_stop_btn.png")
        img_stop_btn = Image.open(img_stop_btn_path).resize((20, 20), Image.LANCZOS)
        self.img_stop_btn = ImageTk.PhotoImage(img_stop_btn)

        img_pause_btn_path = os.path.join(base_dir, "resource", "img_pause_btn.png")
        img_pause_btn = Image.open(img_pause_btn_path).resize((20, 20), Image.LANCZOS)
        self.img_pause_btn = ImageTk.PhotoImage(img_pause_btn)

        img_capture_btn_path = os.path.join(base_dir, "resource", "img_capture_btn.png")
        img_capture_btn = Image.open(img_capture_btn_path).resize((20, 20), Image.LANCZOS)
        self.img_capture_btn = ImageTk.PhotoImage(img_capture_btn)

    def create_connection_frame(self):
        self.frame_nustm_connect = tk.Frame(self, bg='#303841')
        self.frame_nustm_connect.pack(side=tk.TOP, fill=tk.BOTH)

        self.nustm_conn_indicator = tk.Canvas(self.frame_nustm_connect, width=20, height=20, bg='#303841', highlightthickness=0)
        self.nustm_conn_indicator.pack(side=tk.LEFT, padx=5, pady=5)
        self.indicator = self.nustm_conn_indicator.create_oval(2, 2, 18, 18, fill="red")

        self.lbl_nustm_connect = tk.Label(self.frame_nustm_connect, text="NuStream Connection:", bg='#303841', fg='white')
        self.lbl_nustm_connect.pack(side=tk.LEFT, padx=3, pady=3)
        self.entry_nustm_connect = tk.Entry(self.frame_nustm_connect, width=15)
        self.entry_nustm_connect.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry_nustm_connect.insert(tk.END, self.nustm_ip)
        self.btn_nustm_connect = tk.Button(self.frame_nustm_connect, text="Connect", command=self.update_nustm_ip)
        self.btn_nustm_connect.pack(side=tk.LEFT, padx=10, pady=10)

    def create_btn_ctrl_frame(self):
        self.frame_nustm_btn_ctrl = tk.Frame(self, bg='#303841')
        self.frame_nustm_btn_ctrl.pack(side=tk.TOP, fill=tk.BOTH)
        self.btn_nustm_reserve = tk.Button(self.frame_nustm_btn_ctrl, image=self.img_reserve_btn, command=self.update_reserve_module)
        self.btn_nustm_reserve.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_nustm_clear = tk.Button(self.frame_nustm_btn_ctrl, image=self.img_clear_btn, command=self.update_nustm_clear)
        self.btn_nustm_clear.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_nustm_stop = tk.Button(self.frame_nustm_btn_ctrl, image=self.img_stop_btn, command=self.update_nustm_stop)
        self.btn_nustm_stop.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_nustm_stop.config(state=tk.DISABLED)
        self.btn_nustm_start = tk.Button(self.frame_nustm_btn_ctrl, image=self.img_start_btn, command=self.update_nustm_start)
        self.btn_nustm_start.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_nustm_pause = tk.Button(self.frame_nustm_btn_ctrl, image=self.img_pause_btn, command=self.update_nustm_pause)
        self.btn_nustm_pause.pack(side=tk.LEFT, padx=10, pady=10)
        self.btn_nustm_pause.config(state=tk.DISABLED)
        self.btn_nustm_capture = tk.Button(self.frame_nustm_btn_ctrl, image=self.img_capture_btn, command=self.nustm_capture)
        self.btn_nustm_capture.pack(side=tk.LEFT, padx=10, pady=10)

    def create_show_lock_ports(self):
        self.frame_nustm_show_ports_title = tk.Frame(self, bg='#303841')
        self.frame_nustm_show_ports_title.pack(side=tk.TOP, fill=tk.BOTH)
        self.lbl_show_ports_title = tk.Label(self.frame_nustm_show_ports_title, text="Reserve/Lock Ports", bg='#303841', fg='white', font=("Arial", 16))
        self.lbl_show_ports_title.pack(side=tk.LEFT, padx=3, pady=3)
        self.frame_nustm_show_ports = tk.Frame(self, bg='#303841')
        self.frame_nustm_show_ports.pack(side=tk.TOP, fill=tk.BOTH)
        
        self.lbl_test = ["NA","NA","NA","NA"]
        for show_port_idx in (self.lbl_test):
            self.lbl_show_port = tk.Label(self.frame_nustm_show_ports, text=show_port_idx, bg='#303841', fg='white', anchor='w')
            self.lbl_show_port.pack(side=tk.TOP, padx=3, pady=3, fill='x')

    def update_connect_status(self):
        self.nustm_ctrl.nustm_flag = self.nustm_ctrl.check_nustm()

        color = "green" if self.nustm_ctrl.nustm_flag else "red"
        self.nustm_conn_indicator.itemconfig(self.indicator, fill=color)

        if self.nustm_ctrl.nustm_flag:
            self.btn_nustm_connect.config(state=tk.DISABLED)
            self.entry_nustm_connect.config(state=tk.DISABLED, bg='#303841')
        else:
            self.btn_nustm_connect.config(state=tk.NORMAL)
            self.entry_nustm_connect.config(state=tk.NORMAL, bg='white')

    def update_status(self):
        if self.nustm_ctrl.nustm_flag:
            print("Nu Connect")
            print(self.locked_items)
        else:
            print("Nu Not Connect")

    def update_nustm_ip(self):
        new_nustm_ip = self.entry_nustm_connect.get()
        result = self.nustm_ctrl.connect_to_nustm(new_nustm_ip)

    def update_reserve_module(self):
        if self.nustm_ctrl.nustm_flag:
            media_info = self.nustm_ctrl.nustream_media_get()
            self.reserve_release_module = ReserveReleaseModule(media_info, nustm_ctrl=self.nustm_ctrl, parent_frame=self)
            self.reserve_release_module.geometry("+400+200")
            self.reserve_release_module.mainloop()
        else:
            messagebox.showwarning("NuStream Connect Error", "Not Connect")

    def update_nustm_start(self):
        if self.locked_ports_idx:
            self.nustm_ctrl.nustream_ports_config(self.locked_items, self.locked_ports_cbp_id, self.locked_ports_idx)
            self.nustm_ctrl.nustream_traffic_start()
            self.btn_nustm_stop.config(state=tk.NORMAL)
            self.btn_nustm_start.config(state=tk.DISABLED)
            self.btn_nustm_pause.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("NuStream Ports Error", "Not Reserve/Lock Ports")

    def update_nustm_stop(self):
        if self.locked_ports_idx:
            self.nustm_ctrl.nustream_traffic_stop()
            self.btn_nustm_stop.config(state=tk.DISABLED)
            self.btn_nustm_start.config(state=tk.NORMAL)
            self.btn_nustm_pause.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("NuStream Ports Error", "Not Reserve/Lock Ports")

    def update_nustm_pause(self):
        if self.locked_ports_idx:
            self.nustm_ctrl.nustream_traffic_stop()
            self.btn_nustm_stop.config(state=tk.DISABLED)
            self.btn_nustm_start.config(state=tk.NORMAL)
            self.btn_nustm_pause.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("NuStream Ports Error", "Not Reserve/Lock Ports")

    def update_nustm_clear(self):
        if self.locked_ports_idx:
            self.nustm_ctrl.nustream_traffic_clear(self.locked_ports_idx)
        else:
            messagebox.showwarning("NuStream Ports Error", "Not Reserve/Lock Ports")

    def nustm_capture(self):
        window_title = "NuWIN-RM"  # Wnd name
        windows = gw.getWindowsWithTitle(window_title)

        if windows:
            window = windows[0]
            hwnd = window._hWnd

            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top

            hwindc = win32gui.GetWindowDC(hwnd)
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            memdc = srcdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(srcdc, width, height)
            memdc.SelectObject(bmp)
            memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

            bmp_info = bmp.GetInfo()
            bmp_str = bmp.GetBitmapBits(True)
            screenshot = Image.frombuffer(
                'RGB',
                (bmp_info['bmWidth'], bmp_info['bmHeight']),
                bmp_str, 'raw', 'BGRX', 0, 1
            )

            # Create the directory
            save_dir = os.path.join(os.getcwd(), "NuStreamImage")
            os.makedirs(save_dir, exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f"NuWIN-RM_capture_{timestamp}.png")
            screenshot.save(filename)
            messagebox.showinfo("Screenshot", f"Screenshot saved as {filename}")

            # Release resource
            memdc.DeleteDC()
            srcdc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
        else:
            messagebox.showwarning("Window Not Found", "NuWIN-RM window not found")


    def update_locked_ports(self,locked_items, locked_ports_cbp_id, locked_ports_idx):
        self.locked_items = locked_items
        self.locked_ports_cbp_id = locked_ports_cbp_id
        self.locked_ports_idx = locked_ports_idx
        for lock_port_idx in (self.locked_items):
            self.lbl_show_port = tk.Label(self.frame_nustm_show_ports, text=lock_port_idx, bg='#303841', fg='white', anchor='w')
            self.lbl_show_port.pack(side=tk.TOP, padx=3, pady=3, fill='x')


class NuStreamCtrl:
    def __init__(self,nustm_ip=""):
        self.nustm_ip = nustm_ip
        self.nustm_flag = False
        self.nustm_cmd = NsCmd(self.nustm_ip)
        self.locked_ports_idx = []

    def connect_to_nustm(self,new_ip):
        print("Connecting from NuStream...")
        self.nustm_ip = new_ip
        self.nustm_cmd = NsCmd(self.nustm_ip)
        self.nustm_cmd.Connect()

    def disconnect_nustm(self):
        print("Disconnecting from NuStream...")

    def check_nustm(self):
        try:
            return self.nustm_cmd.CheckConnection()
            #return True
        except Exception as e:
            self.nustm_flag = self.nustm_cmd.CheckConnection()
            print(f"An error occurred while checking chamber connection: {e}")
            return False
    def nustream_media_get(self):
        media_info = self.nustm_cmd.GetMedia()
        return media_info

    def nustream_traffic_start(self):
        #print("Start:Wait Tansmit Packets")
        self.nustm_cmd.nscmd.transmit_pkts_sync()

    def nustream_traffic_stop(self):
        #print("Stop:Wait Tansmit Packets")
        self.nustm_cmd.nscmd.transmit_pkts_sync_stop()
        #time.sleep(1)

    def nustream_traffic_clear(self,ports_idx):
        #print("Clear Tansmit Packets")
        for idx in ports_idx:
            self.nustm_cmd.SetPortClearCounters(idx)

    def nustream_ports_config(self, locked_items, locked_ports_cbp_id, locked_ports_idx):
        self.nustm_cmd.SetUnLockPort()

        self.locked_ports_cbp_id = locked_ports_cbp_id
        self.locked_ports_idx = locked_ports_idx

        # Lock Port
        for _, element in enumerate(self.locked_ports_cbp_id):
            cid, bid, pid = element
            self.nustm_cmd.SetLockPort(cid, bid, pid)

        for _, element in enumerate(self.locked_ports_idx):
            print(self.nustm_cmd.GetPortMediaInfo(element))

        self.nustm_cmd.SetTxTimeConfig(7776000)
        self.nustm_cmd.nscmd.config_tx_isimmediate(0)
        for _, element in enumerate(self.locked_ports_idx):
            self.nustm_cmd.SetTxStartPort(element)

class ReserveReleaseModule(tk.Tk):
    def __init__(self, media_info, nustm_ctrl, parent_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.master = master
        self.media_info = media_info
        self.locked_items = []
        self.nustm_ctrl = nustm_ctrl
        self.parent_frame = parent_frame
        self.title("Reserve/Release Module")
        self.geometry("520x250")
        self.resizable(False, False)

        self.lift()
        self.attributes("-topmost", True)
        self.after_idle(self.attributes, "-topmost", False)

        # Frame for the listboxes and buttons
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10)

        # Unlock Module Listbox with header and scrollbar
        unlock_label = ttk.Label(frame, text="Unlock Module (Chasis, Board, Port)")
        unlock_label.grid(row=0, column=0, padx=5, pady=5)

        self.unlock_listbox = tk.Listbox(frame, height=9, width=25, selectmode=tk.EXTENDED)
        self.unlock_listbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        unlock_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.unlock_listbox.yview)
        unlock_scrollbar.grid(row=1, column=1, sticky=tk.NS)

        self.unlock_listbox.config(yscrollcommand=unlock_scrollbar.set)

        # Unlock List
        for item in self.media_info:
            self.unlock_listbox.insert(tk.END, item)

        # Buttons for moving items between listboxes
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=2, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text=">>", command=self.add_module, width=3)
        self.add_button.grid(row=0, column=0, pady=2)

        self.remove_button = ttk.Button(button_frame, text="<<", command=self.remove_module, width=3)
        self.remove_button.grid(row=1, column=0, pady=2)

        # Lock Module Listbox with header and scrollbar
        lock_label = ttk.Label(frame, text="Lock Module (Chasis, Board, Port)")
        lock_label.grid(row=0, column=3, padx=5, pady=5)

        self.lock_listbox = tk.Listbox(frame, height=9, width=25, selectmode=tk.EXTENDED)
        self.lock_listbox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.NSEW)

        lock_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.lock_listbox.yview)
        lock_scrollbar.grid(row=1, column=4, sticky=tk.NS)

        self.lock_listbox.config(yscrollcommand=lock_scrollbar.set)

        # Apply and Cancel buttons
        button_frame_bottom = ttk.Frame(self)
        button_frame_bottom.pack(pady=5)

        self.apply_button = ttk.Button(button_frame_bottom, text="Apply", command=self.apply)
        self.apply_button.grid(row=0, column=0, padx=5)

        self.cancel_button = ttk.Button(button_frame_bottom, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=0, column=1, padx=5)

        if self.master:
            self.master.attributes("-disabled", True)
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_module(self):
        selected_items = self.unlock_listbox.curselection()
        for item in selected_items:
            self.lock_listbox.insert(tk.END, self.unlock_listbox.get(item))
        for item in reversed(selected_items):
            self.unlock_listbox.delete(item)

    def remove_module(self):
        selected_items = self.lock_listbox.curselection()
        for item in selected_items:
            self.unlock_listbox.insert(tk.END, self.lock_listbox.get(item))
        for item in reversed(selected_items):
            self.lock_listbox.delete(item)

    def apply(self):
        self.locked_items = self.lock_listbox.get(0, tk.END)
        self.media_info = [item for item in self.media_info if item not in self.locked_items]

        self.locked_ports_cbp_id = []
        for item in self.locked_items:
            port_info = item.split()[0]
            cid, bid, pid = map(int, port_info.strip("()").split(","))
            self.locked_ports_cbp_id.append((cid, bid, pid))

        self.locked_ports_idx = []
        for _, element in enumerate(self.locked_ports_cbp_id):
            cid, bid, pid = element
            port_idx = self.nustm_ctrl.nustm_cmd.GetPortIdx(cid, bid, pid)
            self.locked_ports_idx.append(port_idx)

        self.parent_frame.update_locked_ports(self.locked_items, self.locked_ports_cbp_id, self.locked_ports_idx)
        self.on_closing()

    def cancel(self):
        self.on_closing()

    def on_closing(self):
        if self.master:
            self.master.attributes("-disabled", False)
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("600x520")
    root.configure(background='#303841')
    root.resizable(False, False)

    create_notebook(root)

    root.mainloop()