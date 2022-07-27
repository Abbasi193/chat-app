import threading
import socket
from crypto import Crypto
from getmac import get_mac_address


class Message (threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.crypto = Crypto()
        self.computer_name_flag = False
        self.mac_flag = False
        self.encryption = False
        self.counter = 0
        self.start()
        self.send_message()

    def run(self):
        self.recieve_message()

    def recieve_message(self):
        while True:
            message = str(self.socket.recv(1024), "utf8")

            if self.encryption:
                message = self.crypto.decrypt(message)
                print('.....', message)
                self.counter += 1
                if self.counter % 5 == 0:
                    self.crypto.update_key(self.counter)
                
            else:
                print('.....', message)

            if self.computer_name_flag:
                self.crypto.set_key(message)
                self.computer_name_flag = False

            elif self.mac_flag:
                self.crypto.set_mac(message)
                self.encryption = True
                print('Encryption enabled')
                self.mac_flag = False

            if message.upper() == "What is your computer Name?".upper():
                computer_name = socket.gethostname()
                self.socket.send(bytes(computer_name, "utf8"))
                self.crypto.set_key(computer_name)
                print(computer_name)
                

            elif message.upper() == "What is your MAC address?".upper():
                mac = get_mac_address().replace(":", "")
                self.socket.send(bytes(mac, "utf8"))
                self.crypto.set_mac(mac)
                self.encryption = True
                print(mac)
                print('Encryption enabled')

    def send_message(self):
        while True:
            message = input("")

            if message.upper() == "What is your computer Name?".upper():
                self.computer_name_flag = True

            elif message.upper() == "What is your MAC address?".upper():
                self.mac_flag = True

            if self.encryption:
                message = self.crypto.encrypt(message)
                self.counter += 1
                if self.counter % 5 == 0:
                    self.crypto.update_key(self.counter)

            self.socket.send(bytes(message, "utf8"))
