import socket
# from _thread import *
import threading    # Nos permite ejecutar lineas de codigo de forma asincrona

HEADER = 64 # bits
PORT = 5050

# Obtiene la Dirección IPv4:
# SERVER = "192.000.1.00" <-- Manual
SERVER = socket.gethostbyname(socket.gethostname()) # <-- Automatico
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# print(SERVER)

# Creamos un socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vinculamos el servidor
try:
    server.bind(ADDRESS)
except socket.error as e:
    print(str(e))

current_Id = "0"

# Atendemos al cliente (nueva conexion)
def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")

    global current_Id
    connection.send(str.encode(current_Id))
    current_Id = "1"
    reply = ''

    connected = True
    while connected:
        msg_lenght = connection.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = connection.recv(msg_lenght).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{address}] --> {msg}")
            connection.send("Message recived".encode(FORMAT))
    
    connection.close()


def start():
    server.listen(2) # Solo escucharemos 2 clientes porque el juego solo es de 2.
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Esperara hasta que alguien se conecte y obtendra la direccion y 
        # creara un objeto conexion que nos permita enviar informacion de regreso
        connection, address = server.accept()

        new_connection = threading.Thread(target=handle_client, args=(connection, address))
        new_connection.start()

        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()