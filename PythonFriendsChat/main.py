import subprocess
import time
import sys


def start_server():
    print("Starte Server...")
    subprocess.Popen([sys.executable, "server.py"])
    time.sleep(1)  #waiting start Server listen

def start_client():
    print("Starte Client...") #Start client
    subprocess.Popen([sys.executable, "client.py"])
    time.sleep(0.3)

if __name__ == "__main__":
    start_server()
    start_client()
    start_client()