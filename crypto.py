
class Crypto:

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
        print('Key changed')

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
