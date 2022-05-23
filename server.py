import socket
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
server.bind(ADDRESS)


# Atendemos al cliente (nueva conexion)
def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")

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
    server.listen()
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