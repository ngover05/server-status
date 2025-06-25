from status_manager import *
from scapy.all import *

def create_internet_log(type):
    with open("history.log", "a") as f:
        # if we were previously offline (connection restored)
        if type:
            string = f"Connection restored at {get_time()}\n"
        # if we were previously online (connection lost)
        else:
            string = f"Connection lost at {get_time()}\n"
        f.write(string)
    return string

def start_network_monitor():
    sniff(prn=handle_packet)

def handle_packet(packet):
    pass