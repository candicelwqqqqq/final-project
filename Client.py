import socket

HOST='127.0.0.1'
PORT=5000

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

while True:
    choice=input('Enter 1 to login, 2 to register: ')
    
    if choice=='1':
        username=input('Enter username: ')
        password=input('Enter password: ')
        message=f'LOGIN {username} {password}'
        client_socket.send(message.encode())
        response=client_socket.recv(1024).decode()
        print(response)
        if response.startswith('You are authenticated'):
            break
        
    elif choice=='2':
        username=input('Enter username: ')
        password=input('Enter password: ')
        password_confirm=input('Enter confirm password: ')
        message=f'REGISTER {username} {password} {password_confirm}'
        client_socket.send(message.encode())
        response=client_socket.recv(1024).decode()
        print(response)
        if response=='Registration Successful':
            break
        
    else:
        print('Invalid choice')

client_socket.send('EXIT'.encode())
client_socket.close()