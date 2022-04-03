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
            msg = message = client.recv(1024) # receive function from socket, at most 1024 bytes
            if msg.decode('ascii').startswith('KICK'): # check if client message starts with KICK; only admin (see client code)                 
                if nicknames[clients.index(client)] == 'admin': # check if client is allowed to use command
                    name_to_kick = msg.decode('ascii')[5:] # 5 because of 4 letters
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin': # check if client is allowed to use command
                    name_to_ban = msg.decode('ascii')[4:] # 4 because of 3 letters
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f: # add banned username to ban list
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refuse!'.encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
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

        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASSWORD'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'echo': # usually password is hashed... 
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue # forget about this failed try and continue with other connection attemps

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}.') # tell admin client's nickname
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # tell clients new client joined
        client.send('Connected ti the server!'.encode('ascii')) # tell new client cnneciton was successful

        thread = threading.Thread(target=handle, args=(client,)) # handeling clients simultaneously; one thread per client
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name) # check which client
        client_to_kick = clients[name_index] # "define" client
        clients.remove(client_to_kick) # remove client from list
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close() # close connection to client
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))



print("Server is listening...")
receive() # run receive method