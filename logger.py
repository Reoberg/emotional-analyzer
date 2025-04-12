import time
import threading

class Logger:
    #Initialize the logger 
    def __init__(self, log_file):
            self.log_file = log_file
            self.lock = threading.Lock()  # Ensuring thread-safe writes

    #Logging every download and check if its downloaded succesfully
    def log(self, url, download_success):
        timestamp = time.strftime("%H:%M, %d %B %Y")
        log_entry = f'"Timestamp": {timestamp}, "URL": "{url}", "Download": {download_success}\n'
        with self.lock:
            with open(self.log_file, 'a') as file:
                file.write(log_entry)