import chunk
import re
import socket
import constants
import os

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
            data_to_get = input()
            request = command_to_send + ' ' + data_to_get + ' ' + 'HTTP/1.1\r\n'
            request += 'Host: ' + host_to_connect + '\r\n'
            request += 'Connection: keep-alive\r\n\r\n'
            #Send request
            client_socket.sendall(request.encode())
            #Receive response
            response = receiveResponse(client_socket)
            status_code = getStatusCode(response)
            headers = getHeaders(response[0])
            if (status_code == '200'):
                received_file = response[1]
                if (headers[b'Content-Type'].split(b';')[0] == b'text/html'):
                    resources = re.findall("\s(=:src|href)(?:=\")([a-zA-Z0-9._/-]+?)\"", str(response[1]))
                    getResources(resources, host_to_connect)
                    
            elif (status_code == '404'):
                print('Resource not found.')
        elif (command_to_send == constants.POST or command_to_send == constants.PUT):
            content_type = 'multipart/form-data'
            print('Enter the relative path for the file to send:')
            file_path = input()
            file_name = os.path.basename(file_path)
            success = False
            try:
                print('Uploading file...')
                file = open(file_path, 'rb')
                file_data = file.read()
                print('Read! Data: ', file_data)
                file_len = len(file_data)
                print('Length: ', file_len)
                file.close()
                success = True
            except Exception:
                print(Exception)
            request = command_to_send +' ' + '/uploads/' + file_path + ' HTTP/1.1\r\n'
            request += 'Host: ' + host_to_connect + '\r\n'
            request += 'Content-Type: ' + content_type + '\r\n'
            request += 'Content-Length: ' + str(file_len) + '\r\n'
            request += 'Connection: keep-alive\r\n\r\n'
            request += str(file_data) + '\r\n'
            #print('REQUEST: ', request)
            #print('***********************************')
            #Send request
            client_socket.sendall(request.encode())
            #Receive response
            response = receiveResponse(client_socket)
            status_code = getStatusCode(response)
            print("Response: ", response)
        elif (command_to_send == constants.DELETE):
            print('Enter the relative path for the file to delete:')
            file_path = input()   
            request = command_to_send + ' ' + file_path + ' HTTP/1.1\r\n'
            request += 'Host: ' + host_to_connect + '\r\n'
            request += 'Connection: keep-alive\r\n\r\n'
            print('REQUEST:', request)
            print('***********************************')
            #Send request
            client_socket.sendall(request.encode())
            #Receive response
            response = receiveResponse(client_socket)
            status_code = getStatusCode(response)
            print("Response: ", response)
        elif (command_to_send == constants.HEAD):
            print('Input data to get')
            data_to_get = input()
            request = command_to_send + ' ' + data_to_get + ' ' + 'HTTP/1.1\r\n'
            request += 'Host: ' + host_to_connect + '\r\n\r\n'
            #Send request
            client_socket.sendall(request.encode())
            #Receive response
            response = b''
            response = client_socket.recv(8000)
            response = response.split(b"\r\n\r\n")
            print('Response: ', response)
            status_code = getStatusCode(response)
            headers = getHeaders(response[0])
        else:
            print('Please input a valid command...')
            command_to_send = input()
        print('***********************************')
        print('Enter a new command:')
        command_to_send = input()

    #Quit program - Close connection
    client_socket.sendall(b'QUIT')
    response = receiveResponse(client_socket)
    print(response)
    print('Closing connection...')
    client_socket.close()  

#Receive simple response with wide buffer
def receiveResponse(client_socket):
    response = b""
    response = client_socket.recv(1000000000)
    print(response)
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
        if count == 1 and (chunk.split(b"\r\n")[0] == b"0" or content_length <= len(response)):
            break
        count = 1
    response = response.split(b"\r\n\r\n")
    return response  

def getResources(resources, host): 
    for item in resources:
        request = 'GET' + ' ' + item + ' ' + 'HTTP/1.1\r\n'
        request += 'Host: ' + host + '\r\n'
        request += 'Connection: keep-alive\r\n\r\n'
        #Send request
        client_socket.sendall(request.encode())
        #Receive response
        response = receiveResponse(client_socket)
        status_code = getStatusCode(response)
        if (status_code == '200'):
                received_file = response[1]
                os.makedirs()

#Function to get a dictionary with keys/value headers
def getHeaders(response):
    response = response.split(b"\r\n")
    headers = {}
    for header in response[1:len(response)]:
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
