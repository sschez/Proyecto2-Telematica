import chunk
import re
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to host
sock.connect(("www.google.com", 80))

#Send request
request = b"GET /images/branding/googlelogo/1x/googlelogo_color_150x54dp.png HTTP/1.1\nHost:www.google.com\r\nConnection: close\r\n\r\n"
sock.sendall(request)

#Receive response
response = b""
while True:
    chunk = sock.recv(4096)
    if len(chunk) == 0:
        break
    response = response + chunk

#Print response

#print(str(response).encode("utf-8").decode())    #UTF-8-enconding string
print(response)

sock.close()