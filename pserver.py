import ssl
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
import threading
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
    resp=get_file(method,data,client_socket,raw)
    if(resp!=""):
        client_socket.sendall(resp)
    client_socket.close()
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
    method,resp_header,temp=split_headers(resp.decode())
    try:
        while((int(resp_header['Content-Length']))>=len_recieved):
            resp=resp+server_socket.recv(2048)
            len_recieved=len_recieved+2048
    except:
        pass
    server_socket.close()
    return resp
def http_proxy():
    http_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    http_server.bind(('127.0.0.1',8888))
    http_server.listen(10)
    try:
        while TRUE:
            client_socket,addr=http_server.accept()
            client_thread=threading.Thread(target=client_Connection,args=[client_socket])
            client_thread.start()
    except Exception as e:
        print(e)
        pass

def https_proxy():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/home/kaizukooni/Desktop/cert/CA/CA.pem', keyfile='/home/kaizukooni/Desktop/cert/CA/localhost/localhost.key',password='killjoy56')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        sock.bind(('127.0.0.1', 8889))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            req=conn.recv(1024)
            print(req.decode())

def main():
    http_pthread=threading.Thread(target=http_proxy)
    http_pthread.start()
    https_pthread=threading.Thread(target=https_proxy)
    https_pthread.start()
    https_pthread.join()
    http_pthread.join()

if __name__=="__main__":
    init_prog()
    print('\n\n')
    main()