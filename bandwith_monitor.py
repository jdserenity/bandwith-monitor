import psutil, time; 

class BandwithMonitor():
    def __init__(self, window):
        self.stop = False
        self.window = window
    
    def get_network_usage(self):
        net_io = psutil.net_io_counters()
        return net_io.bytes_sent, net_io.bytes_recv

    def monitor(self):
        self.stop = False
        last_bytes_sent, last_bytes_recv = self.get_network_usage()

        while not self.stop:
            time.sleep(1)
            current_bytes_sent, current_bytes_recv = self.get_network_usage()
            
            # Dividing by 1024 converts bytes to kilobytes: 1 kilobyte = 1024 bytes
            upload_speed = int((current_bytes_sent - last_bytes_sent) / 1024)  # KB/s
            download_speed = int((current_bytes_recv - last_bytes_recv) / 1024)  # KB/s

            # print(f"Upload: {upload_speed} KB/s, Download: {download_speed} KB/s")

            # Update GUI Elements
            self.window.write_event_value('-UPDATE-', (upload_speed, download_speed))

            last_bytes_sent, last_bytes_recv = current_bytes_sent, current_bytes_recv
    
    def stop_monitoring(self):
        self.stop = True