import socket

HEADER = 64 # bits
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.000.00.0"
#SERVER = socket.gethostbyname(socket.gethostname()) # <-- Automatico
ADDRESS = (SERVER, PORT)


client = socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    print(client.recv('####').decode(FORMAT))

send("Hola amigo!")
send(DISCONNECT_MESSAGE)