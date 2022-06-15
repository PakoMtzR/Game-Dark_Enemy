from distutils.log import error
import socket

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.1.160.124" 
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            #reply = self.client.recv(1024).decode()
            #return reply
        except socket.error as e:
            print(e)
            #return str(e)
    
    def update(self):
        try:
            self.client.send(str.encode("status"))
            data = self.client.recv(1024).decode()
            status = data.split(' ')
            return status

        except socket.error as e:
            print(e)
