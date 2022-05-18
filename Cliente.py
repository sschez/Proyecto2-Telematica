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
            response = old_receiveResponse(client_socket)
            status_code = getStatusCode(response)
            headers = getHeaders(response[0])
            #print(headers)
            print("Content type: ", headers[b'Content-Type'])
            if (status_code == '200'):
                received_file = response[1]
                print("Content type (0): ", headers[b'Content-Type'].split(b';')[0])
                if (headers[b'Content-Type'].split(b';')[0] == b'text/html'):
                    print("Get resources")
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
        print('***********************************')
        print('Enter a new command:')
        command_to_send = input()

    #Quit program - Close connection
    print('Closing connection...')
    client_socket.close()  

#Receive simple response with wide buffer
def receiveResponse(client_socket):
    response = b""
    response = client_socket.recv(1000000000)
    response = response.split(b"\r\n\r\n")
    return response

#Receive response
def old_receiveResponse(client_socket):
    count = 0
    content_length = 10000
    response = b""
    while True:
        chunk = client_socket.recv(4096)
        if len(chunk) == 0:
            break
        response = response + chunk
        if count == 0:
            for item in response.split(b"\r\n"):
                if (item.split(b":")[0] == "Content-Length"):
                    content_length = int(item.split(b":")[1].lstrip())
        #else: 
            #print("CHUNK: ", chunk.split(b"\r\n")[0])
        if count == 1 and (chunk.split(b"\r\n")[0] == b"0" or content_length <= len(response)):
            break
        count = 1
        #print("CHUNK: ", chunk)
    response = response.split(b"\r\n\r\n")
    return response    

#Function to get a dictionary with keys/value headers
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

if __name__ == '__main__':
    main()
