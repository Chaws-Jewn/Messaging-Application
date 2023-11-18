import socket, threading

clients = []

def start_server():
    server_address = ("127.0.0.1", 5555)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    print(f"Server started on {server_address[0]}:{server_address[1]}")

    while True:
        accept_client(server)

def accept_client(server):
    server.listen(20)

    while True:
        client_socket, client_addr = server.accept()
        username = client_socket.recv(1024).decode("utf-8").strip()
        stop = False
        response = b"success"
        if len(clients) < 1:
            client_socket.sendall(response)
            stop = True

        # Check matching client usernames
        else:
            for x in clients:
                if x[0] == username:
                    response = (b"failed")

            client_socket.sendall(response)
            if response == b"success":
                stop = True

        # Collect user information
        if stop:
            clients.append([username, client_socket])
            send_message_to_clients(f"{clients[len(clients)-1][0]} joined the chat")
            print(f"Client [{clients[len(clients)-1][0]}] connected successfully at {client_addr[0]}:{client_addr[1]}")
            print(f"Active Clients: {len(clients)}")
            threading.Thread(target=receive_message, args=(client_socket, )).start()
            break
            
        # Close socket to allow reconnection
        else:
            client_socket.close()

def receive_message(client):
    try:
        while True:
            # Find the username of the client (sender)
            user = ""
            for i in range(len(clients)):
                if clients[i][1] == client:
                    user = clients[i][0]
                    break
            message = f"[{user}]: {client.recv(1024).decode("utf-8")}"

            # Send message to clients if a message is received
            send_message_to_clients(message)

    except Exception as e:
        # if program is killed by host, remove user data and close connection
        username = ""
        if str(e) == "[WinError 10054] An existing connection was forcibly closed by the remote host":
            for i in range(len(clients)):
                if clients[i][1] == client:
                    username = clients[i][0]
                    print(f"Client [{username}] disconnected from the server")
                    clients.pop(i)
                    break
            client.close()
            message = f"{username} left the chat"
            send_message_to_clients(message)
            print(f"Active Clients: {len(clients)}")

def send_message_to_clients(message):
    # Send message to all clients
    for i in clients:
        i[1].sendall(message.encode("utf-8"))

start_server()
