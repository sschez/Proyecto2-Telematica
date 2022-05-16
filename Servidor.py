# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

import socket
import threading
import constants
import os

# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = constants.IP_SERVER

def main():
    print("***********************************")
    print("Server is running...")
    print("Dir IP:",server_address )
    print("Port:", constants.PORT)
    server_execution()
    
# Handler for manage incomming clients conections...

def handler_client_connection(client_connection,client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE)
        remote_string = str(data_recevived.decode(constants.ENCONDING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(command)
        
        if (command == constants.HELO):
            response = '100 OK\n'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        elif (command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            is_connected = False
        elif (command == constants.GET):
            data_to_send = input('Input data to get:')
            request = command + ' ' + data_to_send + ' ' + 'HTTP/1.1\r\nHost: '+ server_socket + '\r\n\r\n'
            client_connection.send(request.encode())
            #Recieve GET and save File
            response = client_connection.recv(4000000).split(b"\r\n\r\n")
            print(response[0].decode())
            #200 or 404
            status_code = response[0].decode().split(' ')[1]
            if(status_code=='200'):
                #time.sleep(2)
                file_recieve = response[1]
                #print(file_recieve.decode())
                if(data_to_send.lstrip('/' == (''))):
                    data_to_send = 'html/index.html'
                file = open("./Cliente/"+data_to_send,'wb')
                file.write(file_recieve)
                file.close()
            if(data_to_send.endswith('.jpg')): 
                mimetype = 'image/jpg'
            elif(data_to_send.endswith('.pdf')):
                mimetype = 'application/pdf'
            else:
                mimetype = 'text.html'
            header+='Content-Type'+str(mimetype)+'\n\n'
        elif (command == constants.DATA):
            response = "300 DRCV\n"
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        else:
            response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
    
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()

#Function to start server process...
def server_execution():
    tuple_connection = (server_address,constants.PORT)
    server_socket.bind(tuple_connection)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()

if __name__ == "__main__":
    main()