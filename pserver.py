from email import header
from http.client import HTTPConnection
import imp
from pickle import TRUE
import socket
import requests
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',8889))
server.listen(1)
conn,addr=server.accept()
while TRUE:
    data=conn.recv(1024)
    data=data.split("\n")
    top_header=data[0].split(" ")
    r=requests.request(top_header[0],top_header[1])
    print(r)