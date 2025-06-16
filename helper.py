import time
from datetime import datetime

def generate_time_based_name(prefix="file", use_microseconds=False):
    now = datetime.now()
    if use_microseconds:
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")  # includes microseconds
    else:
        timestamp = now.strftime("%Y%m%d_%H%M%S")  # up to seconds
    return f"{prefix}_{timestamp}"