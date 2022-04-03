import socket
import threading

nickname = input("Choose a nickname: ") # ask for nickname
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 45678)) # connect to server; check IP & port!!!

stop_thread = False

# receiving messages from server; messages from other clients go via the server
def receive():
    while True:
        global stop_thread
        if stop_thread: # if wrong password loop is stopped
            break 

        try:
            message = client.recv(1024).decode('ascii') #receiving messages from server
            if message == 'NICKNAME': # if server asks for 'NICKNAME'
                client.send(nickname.encode('ascii')) # sending nickname
                next_message = client.recv(1024).decode('ascii') # receiving from server
                if next_message == 'PASSWORD': # if server wants a password
                    client.send(password.encode(1024)) # send server password to check
                    if client.recv(1024).decode('ascii') == 'REFUSE': # disconnet if wrong
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread = True

            else:
                print(message)
        except:
            print("An error accurred!")
            client.close()
            break

# always waiting for a new message; if one sent, then runs again and waits
def write():
    while True:
        if stop_thread: # if wrong password, see above
            break
        message = f'{nickname}: {input("")}' # enable client to write message; terminated by klicking enter
        if message[len(nickname)+2:].startswith('/'): # cut out nickname, colon and space (--> +2)
            
            if nickname == 'admin':

                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii')) # skip username, colon, space and /kick (--> +2+6)
                
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
                    
            else:
                print("Commands can only be executed by the admin!")
        
        else:
            client.send(message.encode('ascii'))

# enabling receive & write function at the same time 
receive_thread = threading.Thread(target=receive) # applied to receive function
receive_thread.start

write_thread = threading.Thread(target=write) # applied to write funciton
write_thread.start