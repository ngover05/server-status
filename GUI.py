import tkinter as tk
from tkinter import ttk

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

        self.connected_lbl = ttk.Label(self.online_frame, font=('Arial', 48), text="Online")
        self.connected_lbl.grid(row=0, column=1)

        self.log_frame = ttk.Frame(self.root)
        self.log_frame.pack(fill='x', pady=100)

        self.log_lbl = ttk.Label(self.log_frame, font=('Arial', 18), text="Logs")
        self.log_lbl.pack(anchor=tk.NW)

        self.log_box = tk.Text(self.log_frame, font=('Arial', 18), state='disabled')
        self.log_box.pack(fill=tk.X)      
    
    def start_mainloop(self):
        self.root.mainloop()

    def update_online(self, was_offline, log_text):
        if was_offline:
            self.log_box.config(state='normal')
            self.log_box.insert(tk.INSERT, log_text)
            self.log_box.config(state='disabled')
            self.connected_lbl.config(text="Online")
        else:
            self.log_box.config(state='normal')
            self.log_box.insert(tk.INSERT, log_text)
            self.log_box.config(state='disabled')
            self.connected_lbl.config(text="Offline")
    
    def update_uptime(self, uptime):
        self.uptime_lbl.config(text=f"Uptime: {uptime[3]}d, {uptime[2]}h, {uptime[1]}m, {uptime[0]}s")
    
    def connection_log(self, log_text):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.INSERT, log_text)
        self.log_box.config(state='disabled')