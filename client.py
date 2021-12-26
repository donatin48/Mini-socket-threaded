import socket

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

    def receive(self,extension):
        with open(f"received_file{extension}", "wb") as file:
            while True:
                data = self.s.recv(4096)
                # print(f"data: \n {data}")
                if not data:
                    break
                file.write(data)
        

print("Connecting to server...")
client = Client(ip, port)
print("Connection established.")
extension = str(input("Enter file extension: "))
if extension[0] != ".":
    extension = "." + extension
client.receive(extension)
print("Successfully received file.")
input()


