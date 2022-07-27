from socket import socket
from message import Message

socket = socket()
port = 3000

socket.connect(('127.0.0.1', port))
print("Connected")
print("Client")

Message(socket)
