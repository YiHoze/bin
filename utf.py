import argparse
import re

class UTFanalyzer(object):

    def __init__(self, chars=None, upper=False):
        self.chars = chars
        self.upper_bool = upper

    def parser_args(self):
        parser = argparse.ArgumentParser(
            description='This scripts shows Unicode code points and UTF-8 Hbytes of given characters.'
        )

        parser.add_argument(
            'chars',
            type=str,
            help='Type one or more characters.'
        )
        parser.add_argument(
            '-u',
            dest='upper',
            action='store_true',
            default=False,
            help='Use uppercase for hexadecimal.'
        )

        args = parser.parse_args()
        self.chars = args.chars
        self.upper_bool = args.upper

    def highlight_Bcode(self, dec, byte):
        # 31:red, 32:green, 33:yellow, 34:blue, 35:magenta, 36:cyan, 37: white
        head = '\x1b[34m'
        tail = '\x1b[37m'
        normal = '\x1b[0m'

        if dec < int('0x80', 16):        
            byte = byte.zfill(8)
            return head + byte[:1] + tail + byte[1:] + normal
        elif dec < int('0x800', 16):
            byte = byte.zfill(12)
            return head + byte[0:6] + tail + byte[6:] + normal
        elif dec < int('0x10000', 16):
            byte = byte.zfill(16)
            return head + byte[0:4] + tail + byte[4:10] + head + byte[10:16] + normal
        else:
            byte = byte.zfill(24)
            return head + byte[0:6] + tail + byte[6:12] + head + byte[12:18] + tail + byte[18:24] + normal            

    def highlight_Bbyte(self, byte_number, byte_index, byte):
        head = '\x1b[32m'
        tail = '\x1b[33m'
        normal = '\x1b[0m'
        if byte_index > 0: 
            return head + byte[:2] + tail + byte[2:] + normal
        else:
            if byte_number == 2:
                return head + byte[:3] + tail + byte[3:] + normal
            elif byte_number == 3:
                return head + byte[:4] + tail + byte[4:] + normal
            elif byte_number == 4:
                return head + byte[:5] + tail + byte[5:] + normal

    def show(self):
        for char in self.chars:
            # decimal code points
            Dcode = ord(char)
            # hexadecimal code points
            Hcode = hex(Dcode).replace('0x', '')
            if self.upper_bool:
                Hcode = Hcode.upper()
            # binary code points
            Bcode = bin(Dcode).replace('0b', '')
            # Bcode = Bcode.zfill(8)
            Bcode = self.highlight_Bcode(Dcode, Bcode)
            # hexadecimal UTF-8 bytes
            if Dcode > 127:
                Hbyte = str(char.encode('utf-8'))
                Hbyte = Hbyte.replace("b'\\x", "")
                Hbyte = Hbyte.replace("'", "")
                Hbyte = Hbyte.split('\\x')
                # binary UTF-8 bytes
                Bbyte = []
                for i, val in enumerate(Hbyte):
                    if self.upper_bool:
                        Hbyte[i] = val.upper()
                    bbyte = bin(int(val, 16)).replace('0b', '')
                    bbyte = self.highlight_Bbyte(len(Hbyte), i, bbyte)
                    Bbyte.append(bbyte)
                Hbyte = ' '.join(Hbyte)
                Bbyte = ' '.join(Bbyte)
                print(char, Hcode, Bcode, Hbyte, Bbyte)
            else:
                print(char, Hcode, Bcode)

if __name__ == '__main__':
    utf = UTFanalyzer()
    utf.parser_args()
    utf.show()