from status_manager import *

def create_internet_log(type):
    with open("history.log", "a") as f:
        # if we were previously offline (connection restored)
        if type:
            string = f"Connection restored at {get_time()}"
        # if we were previously online (connection lost)
        else:
            string = f"Connection lost at {get_time()}"
        f.write(string)
    return string