from Crypto.Cipher import Blowfish
import binascii


class MyBlowFish:
    """
    Blow fish encryption and decryption
    """
    def __init__(self, key):
        self.key = key

    @staticmethod
    def padding_pcks5(clear_text):
        byte_num = len(clear_text)
        packing_len = 8 - byte_num % 8
        appendage = chr(packing_len) * packing_len
        return clear_text + appendage

    def encrypt(self, clear_text):
        c1 = Blowfish.new(self.key, Blowfish.MODE_ECB)
        packed_string = MyBlowFish.padding_pcks5(clear_text)
        return c1.encrypt(packed_string)

    def decrypt(self, enc_string):
        c2 = Blowfish.new(self.key, Blowfish.MODE_ECB)
        return MyBlowFish.remove_padding(c2.decrypt(enc_string))

    @staticmethod
    def remove_padding(string):
        maxlen = len(string)
        loop = string[maxlen - 1]
        if 1 <= loop <= 8:
            maxlen = maxlen - loop
            return string[:maxlen]
        return string

    @staticmethod
    def print_hex(data):
        return binascii.hexlify(data)
