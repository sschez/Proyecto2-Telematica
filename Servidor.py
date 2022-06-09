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
        data = client_connection.recv(constants.RECV_BUFFER_SIZE).split(b'\r\n\r\n')
        data_recevived= data[0].decode()
        #print('data:',data[1])
        #print('data_r:',data_recevived)
        #print(data_recevived)
        #print('data',data_recevived)        
        remote_string = str(data_recevived)
        #print('rs:',remote_string)
        remote_command = remote_string.split()
        #print('remote:',remote_command)
        command = remote_command[0]

        if (remote_string== constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode())
            print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
            is_connected=False
            client_connection.close()
            break
        else:
            savefile = remote_command[1].split('/')
            format = savefile[len(savefile)-1]
            #print('savefile',savefile)
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
                    elif(requesting_source.endswith('.doc')):
                            mimetype = 'application/msword'
                    elif(requesting_source.endswith('.csv')):
                            mimetype = 'text/csv'
                    elif(requesting_source.endswith('.mpeg')):
                            mimetype = 'video/mpeg'
                    elif(requesting_source.endswith('.exe')):
                            mimetype = 'application/exe'
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
                try:
                    os.remove(requesting_source)
                    response = '100 DELETED\n'
                except Exception as e:
                    response = 'HTTP/1.1 404 Not Found\r\n\r\n'
                client_connection.sendall(response.encode())

            elif(command==constants.POST):  
                #print("Entra")  
                #print(remote_string)
                #savefile = requesting_source
                #savefile = requesting_source.split('/')
                #format = savefile[1:len(savefile)]
                #print(format)
                #fd = os.open(str(format),os.O_RDWR|os.O_CREAT)
                #print('fd:',fd)
                #print(format)
                if(format.endswith('.jpg') or format.endswith('.jpeg')):
                    #print("Entro")
                    file = data[1]
                    #print('file: ',file)
                    #completeFile=os.path.join(str(savefile),str(file))
                    try:
                        newfile = open(remote_command[1],"wb")
                        newfile.write(file)
                        newfile.close()

                        header = 'HTTP/1.1 200 OK\r\n\r\n'
                    except Exception as e:
                        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                        response= '<html><body>Error 404: File not Found</body></html>'.encode()
                    print(header)
                    client_connection.sendall(header.encode())
                elif(format.endswith('.pdf')):
                    #print("Entro")
                    file = data[1]
                    #print('file: ',file)
                    try:
                        newfile = open(remote_command[1],"wb")
                        newfile.write(file)
                        newfile.close()
                        header = 'HTTP/1.1 200 OK\r\n\r\n'
                    except Exception as e:
                        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                        response= '<html><body>Error 404: File not Found</body></html>'.encode()
                    print(header)
                    client_connection.sendall(header.encode())
                else:                    
                    file = data[1]
                    #print('file: ',file)
                    try:
                        newfile = open(remote_command[1],"wb")
                        newfile.write(file)
                        newfile.close()

                        header = 'HTTP/1.1 200 OK\r\n\r\n'
                    except Exception as e:
                        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
                        response= '<html><body>Error 404: File not Found</body></html>'.encode()
                    print(header)
                    client_connection.sendall(header.encode())

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
                    #response= '<html><body>Error 404: File not Found</body></html>'.encode()
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