from email import header
from http.client import HTTPConnection
import imp
import socket
import http.client
import http.server

hconn=http.client.HTTPConnection("google.com")
hconn.request("GET","/")
resp=hconn.getresponse()
print(resp)