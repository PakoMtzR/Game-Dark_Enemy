import socket 
from _thread import *
import sys

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555
HEADER = 1024 # bits
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# print(SERVER)

# Creamos un socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Viculamos nuestro servidor
try:
    server.bind(ADDRESS)
except socket.error as e:
    str(e)

players_address = []
player1_status = ["live", -10]
player2_status = ["live", -10]

def convert_data(player_status:list):
    data = str(player_status[0]) + ' ' + str(player_status[1])
    return data


# Funcion que nos permite atender al cliente (jugadores)
def threaded_client(connection, player, address):
    print(f"[NEW CONNECTION] {address} player {player} connected.")
    connection.send(str.encode("Connected"))
    players_address.append(address)

    reply = ""
    while True:
        try:
            data = connection.recv(HEADER)
            reply = data.decode(FORMAT)

            if not data:
                print("Disconnected")
                players_address.remove(address)
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

                if players_address.index(address) == 0:
                    if reply == "dead":
                        player1_status[0] = reply
                        connection.sendto(str.encode("win"), players_address[1])
                    
                    elif reply == "status":
                        status = convert_data(player2_status)
                        connection.sendto(str.encode(status), players_address[1])
                        player2_status[1] = -10

                else:
                    if reply == "dead":
                        player2_status[0] = reply
                        connection.sendto(str.encode("win"), players_address[0])
                    
                    elif reply == "status":
                        status = convert_data(player1_status)
                        connection.sendto(str.encode(status), players_address[0])
                        player1_status[1] = -10    
            
            #connection.sendall(str.encode(reply))
        
        except:
            break

    print("Lost Connection")
    connection.close()


def start_server():

    print("[STARTING] Server is starting...")
    server.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")

    current_Player = 0
    while True:
        connection, address = server.accept()
        print("Connected to:", address)
        start_new_thread(threaded_client, (connection, current_Player, address))
        current_Player += 1

# Arrancamos el servidor
start_server()

'''
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
'''