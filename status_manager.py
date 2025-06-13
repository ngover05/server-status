import time
import math
import urllib.request

def get_uptime():
    uptime = time.clock_gettime(time.CLOCK_BOOTTIME)
    seconds = uptime % 60
    uptime = uptime / 60
    minutes = uptime % 60
    uptime = uptime / 60
    hours = uptime % 24
    days = uptime / 24
    return (math.floor(seconds), math.floor(minutes), math.floor(hours), math.floor(days))

def get_time():
    return time.strftime("%H:%M:%S on %B %d")

def is_online():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False