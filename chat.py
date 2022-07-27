import socket
from getmac import get_mac_address


class Chat():
    def __init__(self, socket):
        self.socket = socket
        self.computer_name_flag = False
        self.mac_flag = False
        self.encryption = False
        self.counter = 0

    def recieve_message(self):
        
        message = str(self.socket.recv(1024), "utf8")

        if self.encryption:
            message = self.decrypt(message)
            print(message)
            self.counter += 1
            if self.counter % 5 == 0:
                self.update_key(self.counter)
            
        else:
            print(message)

        if self.computer_name_flag:
            self.set_key(message)
            self.computer_name_flag = False

        elif self.mac_flag:
            self.set_mac(message)
            self.encryption = True
            self.mac_flag = False

        if message.upper() == "What is your computer Name?".upper():
            computer_name = socket.gethostname()
            self.socket.send(bytes(computer_name, "utf8"))
            self.set_key(computer_name)
            print(computer_name)
            return True
            

        elif message.upper() == "What is your MAC address?".upper():
            mac = get_mac_address().replace(":", "")
            self.socket.send(bytes(mac, "utf8"))
            self.set_mac(mac)
            self.encryption = True
            print(mac)
            return True

        return False

    def send_message(self):
        
        message = input("Type..")

        if message.upper() == "What is your computer Name?".upper():
            self.computer_name_flag = True

        elif message.upper() == "What is your MAC address?".upper():
            self.mac_flag = True

        if self.encryption:
            message = self.encrypt(message)
            self.counter += 1
            if self.counter % 5 == 0:
                self.update_key(self.counter)

        self.socket.send(bytes(message, "utf8"))


    def set_key(self, pc_name):
        sum = 0
        for x in pc_name:
            sum += ord(x)
        average = round(sum / len(pc_name))
        key = average % 26
        self.key = key

    def set_mac(self, mac_address):
        mac_address.replace(":", "")
        self.mac_address = mac_address

    def update_key(self, no_messages):
        location = (int(no_messages / 5) - 1) % 12
        half_octet = self.mac_address[location]
        increment = int(half_octet, 16)
        self.key = (self.key + increment) % 26
        print('Key updated')

    def encrypt(self, plain_text):
        cipher_text = ''
        for x in plain_text:

            if ord(x) >= ord('a') and ord(x) <= ord('z'):
                shift = ord(x) - ord('a') + self.key
                cipher_text += chr(shift % 26 + ord('a'))

            elif ord(x) >= ord('A') and ord(x) <= ord('Z'):
                shift = ord(x) - ord('A') + self.key
                cipher_text += chr(shift % 26 + ord('A'))

            else:
                cipher_text += x

        return cipher_text

    def decrypt(self, cipher_text):
        plain_text = ''
        for x in cipher_text:

            if ord(x) >= ord('a') and ord(x) <= ord('z'):
                shift = ord(x) - ord('a') - self.key
                if shift < 0:
                    shift = 26 + shift
                plain_text += chr(shift + ord('a'))

            elif ord(x) >= ord('A') and ord(x) <= ord('Z'):
                shift = ord(x) - ord('A') - self.key
                if shift < 0:
                    shift = 26 + shift
                plain_text += chr(shift + ord('A'))

            else:
                plain_text += x

        return plain_text
