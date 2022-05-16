import chunk
import re
import socket
import constants

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    print('***********************************')
    print('Client is running...')
    host_to_connect = input()

    #Connect to host
    client_socket.connect((host_to_connect, constants.PORT_HTTP))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    command_to_send = input()




    while command_to_send != constants.QUIT:
        print('1. GET')
        print('2. HEAD')
        print('3. POST')

        if command_to_send == '1': #GET
            print('Please input a valid command...')
            command_to_send = input()                       
        elif (command_to_send == '2'): #HEAD
            data_to_send = input('Input data to send: ') 
            command_and_data_to_send = command_to_send + ' ' + data_to_send
            client_socket.send(bytes(command_and_data_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()               
        elif (command_to_send == '3'): #POST    
            client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()
        else:
            print('Please input a valid command...')
            command_to_send = input()




    #Send request
    request = b"GET /images/branding/googlelogo/1x/googlelogo_color_150x54dp.png HTTP/1.1\nHost:www.google.com\r\nConnection: close\r\n\r\n"
    client_socket.sendall(request)

    #Receive response
    response = b""
    while True:
        chunk = client_socket.recv(4096)
        if len(chunk) == 0:
            break
        response = response + chunk

    #Print response

    #print(str(response).encode("utf-8").decode())    #UTF-8-enconding string
    print(response)

    #close connection with host
    client_socket.close()

if __name__ == '__main__':
    main()