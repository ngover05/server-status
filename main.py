import tkinter as tk
from tkinter import ttk
from status_manager import *

class GUI:
    def __init__(self):
        self.root = tk.Tk()

        # self.root.attributes('-fullscreen', True)
        self.root.geometry("1920x1080")
        self.root.title("Server Status")

        # Uptime label
        self.uptime_lbl = ttk.Label(self.root, font=('Arial', 48))
        self.uptime_lbl.pack(anchor=tk.NW, padx=10, pady=10)

        # Frame to hold connectivity status
        self.online_frame = ttk.LabelFrame(self.root)
        self.online_frame.columnconfigure(0, weight=1)
        self.online_frame.columnconfigure(1, weight=1)
        self.online_frame.pack(anchor=tk.NE, padx=10, pady=10)

        self.online_lbl = ttk.Label(self.online_frame, font=('Arial', 48), text="Connectivity status: ")
        self.online_lbl.grid(row=0, column=0)

        self.connected_lbl = ttk.Label(self.online_frame, font=('Arial', 48))
        self.connected_lbl.grid(row=0, column=1)

        self.log_frame = ttk.Frame(self.root)

        self.update_uptime()
        self.was_offline = False # Used to check if we need to log a restoration in internet connection
        self.update_connected()

        self.root.mainloop()
    
    def update_uptime(self):
        uptime = get_uptime()
        self.uptime_lbl.config(text=f"Uptime: {uptime[3]}d, {uptime[2]}h, {uptime[1]}m, {uptime[0]}s")
        self.uptime_lbl.after(1000, self.update_uptime)
    
    def update_connected(self):
        if is_online():
            if self.was_offline:
                pass
            self.connected_lbl.config(text="Online")
        else :
            self.connected_lbl.config(text="Offline")
            self.was_offline = True
        self.connected_lbl.after(1000, self.update_connected)


GUI()