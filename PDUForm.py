import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageGrab


from lib.PDU_Utils import PDUCmd as PDUCmd

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
    def __init__(self, master=None ,pdu_ip="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pdu_model = None
        self.pdu_ip = pdu_ip
        self.pdu_ctrl = None
        self.init_frame()
        self.load_resource()
        self.create_connection_frame()
        self.create_portstatus_frame()

    def init_frame(self):
        self.configure(background='#303841')
        self.pack(fill=tk.BOTH, expand=True)

    def load_resource(self):
        base_dir = os.path.dirname(__file__)
        img_pdu_off_path = os.path.join(base_dir, "resource", "img_pdu_off.jpg")
        img_pdu_off = Image.open(img_pdu_off_path).resize((40, 40), Image.LANCZOS)
        self.img_pdu_off = ImageTk.PhotoImage(img_pdu_off)

        img_pdu_on_path = os.path.join(base_dir, "resource", "img_pdu_on.jpg")
        img_pdu_on = Image.open(img_pdu_on_path).resize((40, 40), Image.LANCZOS)
        self.img_pdu_on = ImageTk.PhotoImage(img_pdu_on)

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
        model_list = ["iPoMan II","iPoMan III"]
        self.combobox_model = ttk.Combobox(self.frame_pdu_connect, state='readonly', values=model_list)
        self.combobox_model.pack(side=tk.LEFT, padx=10, pady=10)
        self.combobox_model.set(model_list[0])

    def create_portstatus_frame(self):
        self.frame_port_name = tk.Frame(self, bg='#303841')
        self.frame_port_name.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_status = tk.Frame(self, bg='#303841')
        self.frame_port_status.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_button = tk.Frame(self, bg='#303841')
        self.frame_port_button.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_current = tk.Frame(self, bg='#303841')
        self.frame_port_current.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_power = tk.Frame(self, bg='#303841')
        self.frame_port_power.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.frame_divider = ttk.Separator(self, orient='vertical')
        self.frame_divider.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.frame_port_name2 = tk.Frame(self, bg='#303841')
        self.frame_port_name2.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_status2 = tk.Frame(self, bg='#303841')
        self.frame_port_status2.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_button2 = tk.Frame(self, bg='#303841')
        self.frame_port_button2.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_current2 = tk.Frame(self, bg='#303841')
        self.frame_port_current2.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.frame_port_power2 = tk.Frame(self, bg='#303841')
        self.frame_port_power2.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.status_list = []
        self.current_list = []
        self.power_list = []

        for i in range(1, 7):
            current_label = tk.Label(self.frame_port_name, text=f"Port {i}", bg="#303841", fg="white", anchor="center", justify="center", font=("Arial", 10))
            current_label.pack(side=tk.TOP, padx=10, pady=21)
            status_label = tk.Label(self.frame_port_status, image=self.img_pdu_off, bg="#303841", width=40, height=40, compound=tk.TOP)
            status_label.pack(side=tk.TOP, padx=10, pady=10)
            self.status_list.append(status_label)

            # Add toggle button
            toggle_button = PduToggleBtn(self.frame_port_button, "on.png", "off.png", i, self.pdu_ctrl)
            toggle_button.pack(side=tk.TOP, padx=10, pady=10)

            current_label = tk.Label(self.frame_port_current, text="NA", bg="#303841", fg="white", anchor="center", justify="center", font=("Arial", 10))
            current_label.pack(side=tk.TOP, padx=10, pady=21)
            self.current_list.append(current_label)

            power_label = tk.Label(self.frame_port_power, text="NA", bg="#303841", fg="white", anchor="center", justify="center", font=("Arial", 10))
            power_label.pack(side=tk.TOP, padx=10, pady=21)
            self.power_list.append(power_label)

        for i in range(7, 13):
            current_label = tk.Label(self.frame_port_name2, text=f"Port {i}", bg="#303841", fg="white", anchor="center", justify="center", font=("Arial", 10))
            current_label.pack(side=tk.TOP, padx=10, pady=21)
            status_label = tk.Label(self.frame_port_status2, image=self.img_pdu_off, bg="#303841", width=40, height=40, compound=tk.TOP)
            status_label.pack(side=tk.TOP, padx=10, pady=10)
            self.status_list.append(status_label)

            # Add toggle button
            toggle_button = PduToggleBtn(self.frame_port_button2, "on.png", "off.png", i, self.pdu_ctrl)
            toggle_button.pack(side=tk.TOP, padx=10, pady=10)

            current_label = tk.Label(self.frame_port_current2, text="NA", bg="#303841", fg="white", anchor="center", justify="center", font=("Arial", 10))
            current_label.pack(side=tk.TOP, padx=10, pady=21)
            self.current_list.append(current_label)

            power_label = tk.Label(self.frame_port_power2, text="NA", bg="#303841", fg="white", anchor="center", justify="center", font=("Arial", 10))
            power_label.pack(side=tk.TOP, padx=10, pady=21)
            self.power_list.append(power_label)


    def update_pdu_ip(self):
        self.pdu_model = self.combobox_model.get()
        self.pdu_ip = self.entry_pdu_connect.get()
        print(self.pdu_model,self.pdu_ip)
        self.pdu_ctrl = PduCtrl(self.pdu_model,self.pdu_ip)

    def update_connect_status(self):
        self.pdu_ctrl = PduCtrl(self.pdu_model,self.pdu_ip)
        self.pdu_ctrl.pdu_flag = self.pdu_ctrl.check_pdu()

        color = "green" if self.pdu_ctrl.pdu_flag else "red"
        self.pdu_conn_indicator.itemconfig(self.indicator, fill=color)

        if self.pdu_ctrl.pdu_flag:
            self.btn_pdu_connect.config(state=tk.DISABLED)
            self.entry_pdu_connect.config(state=tk.DISABLED, bg='#303841')
        else:
            self.btn_pdu_connect.config(state=tk.NORMAL)
            self.entry_pdu_connect.config(state=tk.NORMAL, bg='white')

    def get_indicator_status(self):
        return self.pdu_conn_indicator.itemcget(self.indicator, "fill")

class PduCtrl:
    def __init__(self,model="",pdu_ip=""):
        self.pdu_model = model
        self.pdu_ip = pdu_ip
        self.pdu_flag = False
        self.pdu_cmd = PDUCmd(self.pdu_model,self.pdu_ip)

    def check_pdu(self):
        print(self.pdu_model,self.pdu_ip)
        try:
            return self.pdu_cmd.CheckConnection()
        except Exception as e:
            self.pdu_flag = self.pdu_flag.CheckConnection()
            print(f"An error occurred while checking chamber connection: {e}")
            return False

class PduToggleBtn(tk.Button):
    def __init__(self, parent, on_image_path, off_image_path, port_number, pdu_ctrl, *args, **kwargs):
        self.is_on = False  # Keep track of the button state on/off
        self.port_number = port_number  # Store the port number
        self.pdu_ctrl = pdu_ctrl  # Store the PduCtrl instance

        # Load Images
        self.on_image = ImageTk.PhotoImage(Image.open(on_image_path).resize((50, 38), Image.LANCZOS))
        self.off_image = ImageTk.PhotoImage(Image.open(off_image_path).resize((50, 38), Image.LANCZOS))
        super().__init__(parent, image=self.off_image, command=self.switch, *args, **kwargs)

    def switch(self):
        # Determine if on or off
        if self.pdu_ctrl == None:
            messagebox.showwarning("PDU Connect Error", "Not Connect")
        else:
            if self.is_on:
                self.config(image=self.off_image)
                self.is_on = False
                self.pdu_ctrl.SetPduPortOff(self.port_number)  # Turn off the port
            else:
                self.config(image=self.on_image)
                self.is_on = True
                self.pdu_ctrl.SetPduPortOn(self.port_number)  # Turn on the port

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Summary Window")
    root.geometry("600x520")
    root.configure(background='#303841')
    root.resizable(False, False)

    create_notebook(root)

    root.mainloop()