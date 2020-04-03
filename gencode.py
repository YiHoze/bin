# pip python-barcode
# pip install qrcode[pil]

import os, argparse
import barcode, qrcode, qrcode.image.svg, codecs, re, webbrowser
from pyzbar.pyzbar import decode
from PIL import Image
from barcode.writer import ImageWriter
from barcode import generate

class GenerateCode(object):
    def __init__(self, code=None, qrcode=False, filename='barcode', svg=False, decode=False):
        self.code = code
        self.qrcode_bool = qrcode
        self.output = filename
        self.svg_bool = svg
        self.decode_bool = decode

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = '''Generate barcodes or QR codes in PNG. 
            The last check digit of barcode will be automatically corrected if it is wrong.'''
        )
        parser.add_argument(
            'code',
            nargs = '+',
            help = 'Specify a 13-digit number or more for barcodes or a text or more for QR codes.'
        )
        parser.add_argument(
            '-q',
            dest = 'qrcode',
            action = 'store_true',
            default = False,
            help = 'Create QR codes.'
        )
        parser.add_argument(
            '-o',
            dest = 'output',
            default = 'barcode',
            help = '''Specify a filename for output. 
            The default is "barcode" or "qrcode", and it will be sequentially numbered with two digits.'''
        )
        parser.add_argument(
            '-s',
            dest = 'svg',
            action = 'store_true',
            default = False,
            help = 'Additionaly generate barcodes or QR codes in SVG.'
        )
        parser.add_argument(
            '-d',
            dest = 'decode',
            action = 'store_true',
            default = False,
            help = 'Decode a QR code of PNG or JPG image.'
        )
        args = parser.parse_args()
        self.code = args.code
        self.qrcode_bool = args.qrcode
        self.output = args.output
        self.svg_bool = args.svg
        self.decode_bool = args.decode

    def name_file(self, counter):
        basename = os.path.splitext(self.output)[0]
        if len(self.code) > 1:
            filename = "%s_%02d" %(basename, counter)
        else:
            filename = basename
        return filename

    def encode_barcode(self):
        EAN = barcode.get_barcode_class('ean13')
        counter = 1
        for code in self.code:
            filename = self.name_file(counter)
            ean = EAN(code, writer=ImageWriter())
            ean.save(filename)
            if self.svg_bool:
                generate('EAN13', code, output=filename)
            counter += 1

    def encode_qrcode(self):   
        if self.output == 'barcode':
            self.output = 'qrcode'
        counter = 1 
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        for code in self.code:
            filename = self.name_file(counter)       
            qr.add_data(code)
            qr.make(fit=True)
            img = qr.make_image()
            png = filename + '.png'
            img.save(png)        
            qr.clear()
            if self.svg_bool:
                factory = qrcode.image.svg.SvgPathImage
                img = qrcode.make(code, image_factory=factory)
                svg = filename + '.svg'
                img.save(svg)
            counter +=1 

    def decode_qrcode(self):
        for img in self.code:
            if not os.path.exists(img):
                print('%s does not exist.' %(img))
                return
            data = decode(Image.open(img))[0][0]    
            data = data.decode('utf-8')        
            link = data.replace('\\:', ':')
            link = link.replace(';', '')
            result = re.search('http.*', link)
            if result is not None:
                uri = result.group()
                print(uri)
                webbrowser.open_new_tab(uri)    
            else:
                print(data)

if __name__ == '__main__':
    gencode = GenerateCode()
    gencode.parse_args()
    if gencode.decode_bool:
        gencode.decode_qrcode()
    else:
        if gencode.qrcode_bool:
            gencode.encode_qrcode()
        else:
            gencode.encode_barcode()