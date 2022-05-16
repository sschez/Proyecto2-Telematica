import chunk
import re
import socket
import constants

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Receive response
response = b""
while True:
    chunk = sock.recv(4096)
    if len(chunk) == 0:
        break
    response = response + chunk

#Print response

#HEAD
    while command_to_send != constants.QUIT:
        if command_to_send == '':
            print('Please input a valid command...')
            command_to_send = input()                        
        elif (command_to_send == constants.DATA):
            data_to_send = input('Input data to send: ') 
            command_and_data_to_send = command_to_send + ' ' + data_to_send
            client_socket.send(bytes(command_and_data_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()            
        else:        
            client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()
    
    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)        
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()    

#print(str(response).encode("utf-8").decode())    #UTF-8-enconding string
print(response)
#>>>>>>> 9237e3e3fb13fd5f5f410f892bbb283e349934e6

sock.close()