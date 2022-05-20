# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

from fileinput import filename
from inspect import modulesbyfile
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
    is_connected=True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE).decode()
        print('data',data_recevived)
        remote_string = str(data_recevived)
        remote_command = remote_string.split()
        print('remote:',remote_command)
        command = remote_command[0]        
        print('command',command)
        if (command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode())
            print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
            client_connection.close()
            is_connected=False
            break
        else:
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
                    
                    header = 'HTTP/1.1 200 OK\r\n'
                        
                    if(requesting_source.endswith('.jpg') or requesting_source.endswith('.jpeg')):
                            mimetype = 'image/jpg'
                    elif(requesting_source.endswith('.css')):
                            mimetype = 'text/css'
                    elif(requesting_source.endswith('.pdf')):
                            mimetype = 'application/pdf'
                    else:
                            mimetype = 'text/html'
                    header += 'Content-Type: '+str(mimetype)+'\r\n\r\n'
                    #header += 'Content-Length: '+len(str(response))+'\r\n\r\n'

                except Exception as e:
                    header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    response= '<html><body>Error 404: File not Found</body></html>'.encode()
                final_response = header.encode()
                final_response += response            
                client_connection.sendall(final_response)
                
            

            elif (command == constants.DELETE):
                os.remove(requesting_source)
                response = '100 DELETED\n'
                client_connection.sendall(response.encode())

            elif(data_recevived==constants.POST or data_recevived==constants.PUT):  
                print("Entra")             
                savefile = requesting_source
                fd = os.open(savefile,os.O_RDWR)
                print('savefile:',savefile)
                print('fd:',fd)
                file = data_recevived.split(b'\r\n\r\n')
                print('file: ',file)
                completeFile=os.path.join(savefile,file)
                try:
                    with open(filename, "rb") as f:
                        while True:
                            bytes_read = f.read(constants.RECV_BUFFER_SIZE)
                            if not bytes_read:
                                break
                            header = 'HTTP/1.1 200 OK\r\n'
                            header += 'Content-Length: '+len(str(f))+'\r\n\r\n'
                            completeFile.update(len(bytes_read))
                        #s.close()
                except Exception as e:
                    header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    response= '<html><body>Error 404: File not Found</body></html>'.encode()
                final_response = header.encode()    
                client_connection.sendall(final_response)
                
            elif (command == constants.HEAD):
                if(myfile == '' or myfile=='/'):
                    myfile='index.html'
                    
                try:
                    file = open(myfile,'rb')
                    response = file.read()
                    file.close()
                    
                    header = 'HTTP/1.1 200 OK\r\n'
                        
                    if(requesting_source.endswith('.jpg')):
                            mimetype = 'image/jpg'
                    elif(requesting_source.endswith('.css')):
                            mimetype = 'text/css'
                    elif(requesting_source.endswith('.pdf')):
                            mimetype = 'application/pdf'
                    else:
                            mimetype = 'text/html'
                    header += 'Content-Type: '+str(mimetype)+'\r\n\r\n'
                    #header += 'Content-Length: '+len(str(response))+'\r\n\r\n'

                except Exception as e:
                    header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    response= '<html><body>Error 404: File not Found</body></html>'.encode()
                final_response = header.encode()                          
                client_connection.sendall(final_response)
            

            else:
                response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
                client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))         


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