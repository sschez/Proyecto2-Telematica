# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

from inspect import modulesbyfile
import socket
import threading

from numpy import source
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
        print("prueba")
        data_recevived = client_connection.recv(1024).decode(constants.ENCONDING_FORMAT)
        print(data_recevived)
        remote_string = str(data_recevived)
        #remote_string = str(data_recevived.decode(constants.ENCONDING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        requesting_source= remote_command[1]

        print('Client request', requesting_source)

        myfile = requesting_source.split('?')[0]
        myfile = myfile.lstrip('/')

        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(command)
        
        if (command == constants.GET):
            if(myfile == '' or myfile=='/'):
                myfile='index.html'
            try:
                file = open(myfile,'rb')
                response = file.read()
                file.close()
                
                header = 'HTTP/1.1 200 OK\n'
                    
                if(requesting_source.endswith('.jpg')):
                        mimetype = 'image/jpg'
                elif(requesting_source.endswith('.css')):
                        mimetype = 'text/css'
                elif(requesting_source.endswith('.pdf')):
                        mimetype = 'application/pdf'
                else:
                        mimetype = 'text/html'
                header += 'Contentt Type: '+str(mimetype)+'\r\n'
                header += 'Content-Length: '+len(response)+'\r\n\r\n'

            except Exception as e:
                header = 'HTTP/1.1 404 Not Found\n\n'
                response= '<html><body>Error 404: File not Found</body></html>'.encode(constants.ENCONDING_FORMAT)
            final_response = header.encode(constants.ENCONDING_FORMAT)
            final_response += response            
            client_connection.sendall(final_response)
            print(final_response)
            #client_connection.close()

        elif (command == constants.DELETE):
            os.remove(source)
            response = '200 DELETED\n'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        elif (command == constants.HEAD):
            data = client_connection.recv(200)
            client_connection.send(b'HTTP/1.0 200 OK\r\n')
            client_connection.send(b"Content-Type: text/html\r\n\r\n")
            client_connection.send(b'<html><body><h1>Hello World</body></html>')
            client_connection.send(b"Resp: " + data)
            client_connection.close()
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