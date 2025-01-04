import subprocess
import time
import os

def monitor_connections(interval=5):
    """
    Monitor active network connections on a Linux device.
    sudo apt install net-tools
    Args:
        interval (int): Time in seconds between monitoring iterations.
    This script will show you TCP/UDP in IPv4 and IPv6 active on your system. 
    """
    try:
        while True:
            # Clear the terminal screen
            os.system('clear')

            # Run netstat command to display active network connections
            result = subprocess.run(['netstat', '-tunap'], text=True, capture_output=True)

            if result.returncode == 0:
                print("Active Connections (netstat -tunap):\n")
                print(result.stdout)
            else:
                print("Error executing netstat. Make sure the command is installed and you have sufficient permissions.")
            
            # Wait for the specified interval before the next iteration
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    monitor_connections(interval=5)
