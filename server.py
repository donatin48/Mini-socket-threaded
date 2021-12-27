from re import A
import socket
import threading
import tkinter as tk
from tkinter import filedialog
from threading import Thread
import os
from tqdm import tqdm


port = 5000
host = ""
SEPARATOR = "<SEPARATOR>"
CHUNK_SIZE = 4096

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


    def send(self, path):
        try : 
            # send the filename and file size to the client
            filename = path.split("/")[-1]
            filesize = os.path.getsize(path)
            self.c.send(f"{filename}{SEPARATOR}{filesize}".encode())
            if len(filename) > 25: # if the filename is too long reduce it
                filename_print = filename[:25] + "..."
            else:
                filename_print = filename
            # if   
            progression = tqdm(range(filesize), f"Sending {filename_print}", unit="B", unit_scale=True, unit_divisor=1024)
            # print("\n")
            with open(path, "rb") as file:
                while True:
                    
                    l = file.read(CHUNK_SIZE)
                    while (l):
                        self.c.send(l)
                        l = file.read(CHUNK_SIZE)
                        progression.update(len(l))
                    if not l:
                        self.c.close()
                        threads.remove(self)   
                        progression.close()
                        break  
                    
            self.c.close()
            print(f"File has been sent. thread count: {len(threads)}\n")
        except Exception as e:
            print(f"\nError in thread n°{threads.index(self)}:  {e}")
            self.c.close()
            threads.remove(self)
            progression.close()
            print(f"Threads count: {len(threads)}\n")
            

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.bind((host, port))

path = get_file_path()
if not path:
    print("No file selected.")
    input()
    exit()
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
        if e.errno == 10054:
            print("Connection lost with client.")
        print(f"Connection lost: {e}")
