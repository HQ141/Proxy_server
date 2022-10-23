from functools import cache
from genericpath import isdir, isfile
from importlib.resources import path
from mimetypes import init
from multiprocessing.connection import Connection
import os
import re
from email import header
from http.client import HTTPConnection
import imp
from pickle import TRUE
import socket
import requests
cache_Q=[]
def init_prog():
    if(os.path.isdir("Cache")):
        os.rmdir("Cache")
    os.mkdir("Cache")
def http_Conn(header,conn):
    print("a")
    r=requests.request(header[0],header[1])
    r='HTTP/1.0 200 OK\n\n'+r
    print('a')
    print(r.text)
    conn.sendall(r.text.encode())
    conn.close()
def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',8888))
    server.listen(1)
    try:
        while TRUE:
            client_conn,addr=server.accept()
            data=client_conn.recv(1024).decode()
            print(data)
            data=data.split("\n")
            top_header=data[0].split(" ")
            print(top_header)
            
            #if(re.search('^(http)://',top_header[1])):
            http_Conn(top_header,client_conn)
    except:
        pass
if __name__=="__main__":
    init_prog()
    main()