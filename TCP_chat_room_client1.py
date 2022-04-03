import socket
import threading

nickname = input("Choose a nickname: ") # ask for nickname

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 45678)) # connect to server; check IP & port!!!

# receiving messages from server; messages from other clients go via the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii') #receiving messages from server
            if message == 'NICKNAME': # if server asks for 'NICKNAME'
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error accurred!")
            client.close()
            break

# always waiting for a new message; if one sent, then runs again and waits
def write():
    while True:
        message = f'{nickname}: {input("")}' # enable client to write message; terminated by klicking enter
        client.send(message.encode('ascii'))

# enabling receive & write function at the same time 
receive_thread = threading.Thread(target=receive) # applied to receive function
receive_thread.start

write_thread = threading.Thread(target=write) # applied to write funciton
write_thread.start