from asyncio.windows_events import NULL
from functools import cache
from genericpath import isdir, isfile
from importlib.resources import path
from mimetypes import init
from multiprocessing.connection import Connection
import os
import re
from email import header
from http.client import HTTPConnection
import shutil
from pickle import TRUE
import socket
cache_Q=[]
blacklist=[]
def init_prog():
    f=open('blacklist.txt','r')
    text=f.read()
    text=text.split('\n')
    for lines in text:
        blacklist.append(lines.strip())
    if(os.path.isdir(".Cache")):
        shutil.rmtree(".Cache")
    os.mkdir(".Cache")

def split_headers(raw_msg):
    req_headers={}
    method=''
    lines=raw_msg.split('\n')
    for lines in lines:
        if(re.search('HTTP',lines)==None):
            lines=lines.split(':')
            if(len(lines)>1):
                    req_headers[lines[0]]=lines[1]
        else:
            if(method==''):
                method=lines
    return method,req_headers,raw_msg   
def client_Connection(client_socket):
    data=client_socket.recv(1024).decode()
    method,data,raw=split_headers(data)
    temp=method.split(' ')
    if(re.search('^(http)://',temp[1])):
        resp=get_file(method,data,client_socket,raw)
        if(resp!=""):
            client_socket.sendall(resp)
        client_socket.close()
    else:
        https_Connection(method,data,client_socket,raw)

def https_Connection(method,data,client_socket,raw):
    print(raw)
    ip=socket.gethostbyname(data['Host'].strip())
    
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.connect((ip,443))
    server_socket.sendall(raw.encode())
    x=0
    while x<10:
        print(data['Host'])
        resp=server_socket.recv(2048)
        len_recieved=2048
        print(resp.decode())
        x=x+1
    method,resp_header,temp=split_headers(resp.decode())
    server_socket.close()
    print(resp)

def get_file(method,data,client_socket,raw):
    hash_val=hash(method)
    try:
        index=blacklist.index(data['Host'].strip())
        resp=""
        return resp
    except:
        pass
    try:
        index=cache_Q.index(hash_val)
        cache_Q.pop(index)
        f=open(f'.Cache/{hash_val}','rb')
        resp=f.read()
        f.close()
        cache_Q.append(hash_val)
        return resp
    except:
        pass
    cache_Q.append(hash_val)
    resp=http_Conn(method,data,client_socket,raw)
    f=open(f'.Cache/{hash_val}','wb')
    f.write(resp)
    f.close()
    return resp

def http_Conn(top_header,data,conn,raw):
    ip=socket.gethostbyname(data['Host'].strip())
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.connect((ip,80))
    server_socket.sendall(raw.encode())
    resp=server_socket.recv(2048)
    len_recieved=2048
    print(resp.decode())
    method,resp_header,temp=split_headers(resp.decode())
    while((int(resp_header['Content-Length']))>=len_recieved):
        resp=resp+server_socket.recv(2048)
        len_recieved=len_recieved+2048
    server_socket.close()
    return resp

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('192.168.10.9',8888))
    server.listen(1)
    try:
        while TRUE:
            client_socket,addr=server.accept()
            client_Connection(client_socket)
            print(cache_Q)
    except Exception as e:
        print(e)
        pass
    
if __name__=="__main__":
    init_prog()
    print('\n\n')
    main()