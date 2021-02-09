import threading
import socket

# IP Address of the server (LocalHost)
host = '127.0.0.1'        

# Don't pick any reserved or well known ports.
port = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()         

clients = []        
nicknames = []

# send msg to all clients currently connected to server
def broadcast(message):
    for client in clients:
        client.send(message)

# receive msg from client and broadcast it back to all clients. When a client is added, we also add nickname
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left chat".encode('ascii'))
            nicknames.remove(nickname)
            break


# server.accept() is running all the time, if it gets a connection it returns client and address. Running one thread for each client connected at the same time.

def receive():
      while True:
          client, address = server.accept()
          # printed on server not broadcast
          print(f"Connected with {str(address)}")

          client.send('SYN'.encode('ascii'))
          nickname = client.recv(1024).decode('ascii')
          nicknames.append(nickname)
          clients.append(client)

          print(f"Nickname of the client is {nickname}")
          broadcast(f"{nickname} joined the chat".encode('ascii'))
          client.send("Connected to the server".encode('ascii'))

          thread = threading.Thread(target=handle, args=(client,))
          thread.start()

print("Server is listening...")
receive()
