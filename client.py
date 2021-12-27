import socket
import tkinter as tk
from tkinter import filedialog
import os
from tqdm import tqdm

SEPARATOR = "<SEPARATOR>"
CHUNK_SIZE = 4096
ip = ""
port = 5000
if not ip:
    ip = str(input("Enter IP: "))

# create a network for receive data
class Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def choice_path(self) -> str:
        root = tk.Tk()
        root.withdraw()
        return filedialog.asksaveasfilename()


    def receive(self):
        # receive the filename and file size from the server
        temp = self.s.recv(CHUNK_SIZE).decode()
        filename, filesize = temp.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        # print the information in gigabytes
        print(f"Receiving {filename} of size {round(filesize/1024/1024,2)} MB\n")
        if len(filename) > 25: # if the filename is too long reduce it
            filename_print = filename[:25] + "..."
        else:
            filename_print = filename
        # start receiving the file from the server
        reponse = str(input("Do you want to change the name of the file? (y/n)\n"))
        if reponse == "y":
            path = self.choice_path()
            if not path :
                print("No file selected.")
                input()
                exit()
        else:
            path = os.path.join(os.getcwd(), filename)
        print("\n")
        progression = tqdm(range(filesize), f"Receiving {filename_print}", unit="B", unit_scale=True, unit_divisor=1024)
        
        with open(path, "wb") as file:
            while True:
                data = self.s.recv(4096)
                # print(f"data: \n {data}")
                if not data:
                    break
                file.write(data)
                progression.update(len(data))
        

print("Connecting to server...")
client = Client(ip, port)
print("Connection established.")

try :
    client.receive()
    print("Successfully received file.")
except Exception as e:
    print(f"Connection lost: {e}")

input()


