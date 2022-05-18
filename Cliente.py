import chunk
import re
import socket
import constants

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    print('***********************************')
    print('Client is running...')
    print('***********************************')
    print('Enter host to connect:')
    host_to_connect = input()

    #Connect to host
    client_socket.connect((host_to_connect, constants.PORT_HTTP))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    print('1. GET')
    print('2. HEAD')
    print('3. POST')
    print('4. PUT')
    print('5. DELETE')
    command_to_send = input()


    while command_to_send != constants.QUIT:
        #GET
        if command_to_send == constants.GET:
            print('Input data to get')
            #Get data to get from user
            data_to_get = input()
            #Create request to send
            request = command_to_send + ' ' + data_to_get + ' ' + 'HTTP/1.1\r\nHost: ' + host_to_connect + '\r\n\r\n'
            #Send request
            client_socket.sendall(request.encode())
            #Receive response
            response = receiveResponse(client_socket)
            print('***********************************')
            print(response[0])
            print('***********************************')
            print(response[1])
            #Status code 
            status_code = getStatusCode(response)
            headers = getHeaders(response[0])
            #print(headers)
            #print(headers[b'Content-Type'])
            if (status_code == '200'):
                received_file = response[1]
        elif (command_to_send == constants.POST):
            print('POST')
        elif (command_to_send == constants.DELETE):   
            print('DELETE')
        elif (command_to_send == constants.HEAD):
            print('HEAD')
        elif (command_to_send == constants.PUT):
            print('PUT')
        else:
            print('Please input a valid command...')
            command_to_send = input()
        print(command_to_send)
        print('***********************************')
        print('Enter a new command:')
        command_to_send = input()

    #Quit program - Close connection
    print('Closing connection...')
    client_socket.close()  

#Receive response
def receiveResponse(client_socket):
    content_length = 0
    response = b""
    while True:
        chunk = client_socket.recv(4096)
        if len(chunk) == 0:
            break
        response = response + chunk
        for item in response.split(b"\r\n"):
            if (item.split(b":")[0] == "Content-Length"):
                content_length = int(item.split(b":")[1].lstrip())
                print(item.split(b":")[0], item.split(b":")[1])
        if content_length <= len(response):
            print("BREAK")
            break
    #print(response)
    response = response.split(b"\r\n\r\n")
    return response    


def getHeaders(response):
    response = response.split(b"\r\n")
    headers = {}
    for header in response[1:len(response)-1]:
        tmp = header.split(b":")
        key = tmp[0]
        value = tmp[1].lstrip()
        headers[key] = value
    return headers

#Function to get response's status code
def getStatusCode(response):
    return response[0].decode().split(' ')[1]

#Print response
#print(str(response).encode("utf-8").decode())    #UTF-8-enconding string
#print(response)

if __name__ == '__main__':
    main()
