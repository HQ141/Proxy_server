from email import header
from http.client import HTTPConnection
import imp
import socket
import http.client
import http.server

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',8889))
server.listen(1)
while True:
    conn,addr=server.accept()
    data=conn.recv(1024).decode()
    print(data)
    data=data.split('\n')
    temp=data[0].split(' ')
    method=temp[0]
    req=temp[1]
    test=socket.gethostbyname(req)
