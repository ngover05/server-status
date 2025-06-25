from scapy.all import sniff, IP, TCP
import time
import math
import urllib.request
import threading
import GUI

class backend:
    def __init__(self):
        # Dictionary to keep track of connection status of different IPs
        self.connection_status = {}
        # Boolean to track internet connectivity
        self.was_offline = False
        # Server ip. Stored in text file so I don't dox myself on github
        with open("ip.txt", "r") as f:
            self.ip = f.read()

        # tkinter GUI
        self.GUI = GUI.GUI()

        # Threads for the three main functions of the application
        self.t1 = threading.Thread(target=self.uptime_thread_run)
        self.t2 = threading.Thread(target=self.connection_thread_run)
        self.t3 = threading.Thread(target=self.start_network_monitor)

        self.t1.start()
        self.t2.start()
        self.t3.start()

        self.GUI.start_mainloop()

    # Thread function that updates the uptime every second
    def uptime_thread_run(self):
        while True:
            self.update_uptime()
            time.sleep(1)
    
    # Thread function that updates the internet connectivity every half-second
    def connection_thread_run(self):
        while True:
            self.update_connected()
            time.sleep(0.5)

    # Returns a tuple with different components of the uptime
    def get_uptime(self):
        uptime = time.clock_gettime(time.CLOCK_BOOTTIME)
        seconds = uptime % 60
        uptime = uptime / 60
        minutes = uptime % 60
        uptime = uptime / 60
        hours = uptime % 24
        days = uptime / 24
        return (math.floor(seconds), math.floor(minutes), math.floor(hours), math.floor(days))

    # Returns the current time
    def get_time(self):
        return time.strftime("%H:%M:%S on %B %d")

    # Returns whether or not the computer is online
    def is_online(self):
        try:
            # Ping google to test connection
            urllib.request.urlopen('http://google.com')
            return True
        except:
            return False
    
    # Send the uptime to the GUI to be updated
    def update_uptime(self):
        self.GUI.update_uptime(self.get_uptime())
    
    # Tells the GUI if an update to online status is needed
    def update_connected(self):
        if self.is_online():
            # If we were previously offline (connection restored)
            if self.was_offline:
                self.create_internet_log()
                self.was_offline = False
        else :
            # If we were previously online (connection lost)
            if not self.was_offline:
                self.create_internet_log()
                self.was_offline = True
    
    # Logs a change in internet connectivity and returns the text
    def create_internet_log(self):
        with open("history.log", "a") as f:
            # If we were previously offline (connection restored)
            if self.was_offline:
                string = f"Internet connection restored at {self.get_time()}\n"
            # If we were previously online (connection lost)
            else:
                string = f"Internet connection lost at {self.get_time()}\n"
            # Write to the log file
            f.write(string)
        # Write to the log display on the application
        self.GUI.update_online(self.was_offline, string)

    # Starts the scapy network sniffer
    def start_network_monitor(self):
        sniff(prn=self.handle_packet, iface="tailscale0", filter="ip and tcp port 5000")

    # Handles network packet
    def handle_packet(self, packet):
        if IP in packet:
            flags = packet[TCP].flags
            # If we just sent a SYN/ACK packet to an IP we weren't previously connected to
            # (If we just made a new connection)
            if flags == 'SA' and self.connection_status.get(packet[IP].dst) != True:
                self.connection_status[packet[IP].dst] = True
                self.create_connection_log(packet[IP].dst, flags)
            # If we just received a FIN/ACK packet from an IP we were previously connected to
            # (If someone just disconnected)
            elif packet[IP].src != self.ip and flags == 'FA' and self.connection_status.get(packet[IP].src) != False:
                self.connection_status[packet[IP].src] = False
                self.create_connection_log(packet[IP].src, flags)
    
    # Logs a connection or disconnection and returns the text
    def create_connection_log(self, IP, flag):
        with open("history.log", "a") as f:
            if flag == 'SA':
                string = f"Connection established with {IP} at {self.get_time()}\n"
            else:
                string = f"Connection closed with {IP} at {self.get_time()}\n"
            # Write to the log file
            f.write(string)
        # Write to the log display on the application
        self.GUI.connection_log(string)

backend()