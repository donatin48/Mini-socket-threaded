from os import path
import socket
import threading
import tkinter as tk
from tkinter import filedialog
from threading import Thread

port = 5000
host = ""

# get the file path
def get_file_path():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()
# create a network for send data
class Server(Thread):
    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.c = sock


    def send(self, data):
        with open(data, "rb") as file:
            while True:
                l = file.read(4096)
                while (l):
                    self.c.send(l)
                    l = file.read(4096)
                if not l:
                    self.c.close()
                    break  
        threads.remove(self)   
        print(f"File has been sent. thread count: {len(threads)}\n")
        self.c.close()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.bind((host, port))

path = get_file_path()
print("You Send: " + path)
threads = []
while True:
    try:
        tcpsock.listen(5)
        print("Waiting for incoming connections...\n") 
        (conn, (ip, port)) = tcpsock.accept()
        print(f"Connection established with {ip}")
        thread = Server(ip, port, conn)
        threading.Thread(target=thread.send, args=(path,)).start()
        threads.append(thread)
        print(f"Number of active threads: {len(threads)}")
    except Exception as e:
        print(f"Connection lost: {e}")
