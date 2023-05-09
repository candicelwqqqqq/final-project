import socket
import threading

HOST='127.0.0.1'
PORT=5000

MIN_PASSWORD_LENGTH=8
ALLOWED_CHARACTERS=set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

users={}

server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

def handle_client(conn, addr):
    print(f'New connection from {addr}')
    
    while True:
        message=conn.recv(1024).decode()
        if not message:
            break
        parts=message.split()
        command=parts[0]
        
        if command=='REGISTER':
            username=parts[1]
            password=parts[2]
            password_confirm=parts[3]
            
            if len(password)<MIN_PASSWORD_LENGTH:
                response='Password too short. Must be at least 8 characters.'
            elif not set(password).issubset(ALLOWED_CHARACTERS):
                response='Password contains invalid characters. Must only contain letters and numbers.'
            elif username in users:
                response='Username already exists. Please choose a different username.'
            elif password!=password_confirm:
                response='Passwords do not match. Please try again.'
            else:
                users[username]=password
                response='Registration Successful'
            
            conn.send(response.encode())
            
        elif command=='LOGIN':
            username=parts[1]
            password=parts[2]
            if username in users and users[username] == password:
                response=f'You are authenticated, Welcome {username}'
            else:
                response='Please enter correct username password'
            conn.send(response.encode())
            
        elif command=='EXIT':
            conn.close()
            print(f'Connection from {addr} closed')
            break
        
        else:
            response='Invalid command'
            conn.send(response.encode())

server_socket.listen()

while True:
    conn, addr=server_socket.accept()
    thread=threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()