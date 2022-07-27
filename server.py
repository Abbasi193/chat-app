from socket import socket
from message import Message

socket = socket()
port = 3000

socket.bind(('', port))
socket.listen(5)
print("Listening...")

connection, addr = socket.accept()
print("Connected")
print("Server")

Message(connection)
