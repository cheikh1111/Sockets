import threading
import socket
from datetime import datetime


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "0.0.0.0"
PORT = 12345
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.rcv(1024).decode("utf8")
            if not message:
                break
            current_time = datetime.now()
            current_time = current_time.strftime("%H : %M")
            print(current_time, message)
            for client in clients:
                if not client == client_socket:
                    client.send(message.encode)
        except Exception as e:
            print(e)
            break

    clients.remove(client_socket)
    client_socket.close()


while True:
    client_socket, client_address = server_socket.accept()
    current_time = datetime.now()
    current_time = current_time.strftime("%H : %M")
    print(current_time, "New connection from : %s" % (client_address))
    clients.append(client_socket)

    # Creating Client Socket
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
