import threading
import socket

host = '127.0.0.1' # localhost --> host of replit?
port = 45678 # can be (almost) any port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating server
server.bind((host, port)) # bind server to ip address
server.listen() # listening mode --> new connections?

clients = [] # clients list
nicknames = [] # chosen nicknames

# sending message to all clients connected
def broadcast(message):
    for client in clients:
        client.send(message) # send function from socket

# communication with clients --> if client sends a message, then broadcast it to all clients
# if something doesn't work, cut client from connection & remove from list
def handle(client):
    while True:
        try:
            message = client.recv(1024) # receive function from socket, at most 1024 bytes
            broadcast(message)
        except:
            index = clients.index(client) # which client?
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nicknames)

            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            break

def receive():
    while True:
        client, address = server.accept() # as long as running accepting all connections
        print(f"Connected with {str(address)}") # tell admin new client is connected

        client.send('NICKNAME'.encode('ascii')) # ask client for nickname
        nickname = client.recv(1024).decode('ascii') #receive nickname
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}.') # tell admin client's nickname
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # tell clients new client joined
        client.send('Connected ti the server!'.encode('ascii')) # tell new client cnneciton was successful

        thread = threading.Thread(target=handle, args=(client,)) # handeling clients simultaneously; one thread per client
        thread.start()

print("Server is listening...")
receive() # run receive method