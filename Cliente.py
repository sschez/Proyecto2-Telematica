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