# pip pytnon-barcode
# pip install qrcode[pil]
# #>qr 'https:hoze.tistory.com' > hoze.svg
import argparse, barcode, qrcode, qrcode.image.svg, re, webbrowser
from pyzbar.pyzbar import decode
from PIL import Image
from barcode.writer import ImageWriter
from barcode import generate

parser = argparse.ArgumentParser(
    description = '''Generate barcodes or QR codes in SVG. 
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
    help = 'Create a QR code.'
)
parser.add_argument(
    '-n',
    dest = 'filename',
    default = 'barcode',
    help = '''Specify a filename. 
    The default is "barcode" or "qrcode", and it will be sequentially numbered with two or more numbers.'''
)
parser.add_argument(
    '-p',
    dest = 'png',
    action = 'store_true',
    default = False,
    help = 'Additionaly generate the barcode in PNG.'
)
parser.add_argument(
    '-d',
    dest = 'decode',
    action = 'store_true',
    default = False,
    help = 'Decode a QR code of PNG or JPG image.'
)
args = parser.parse_args()

def encode_barcode():
    EAN = barcode.get_barcode_class('ean13')
    counter = 1
    for code in args.code:
        if len(args.code) > 1:
            filename = "%s_%02d" %(args.filename, counter)
        else:
            filename = args.filename
        generate('EAN13', code, output=filename)
        if args.png:
            ean = EAN(code, writer=ImageWriter())
            ean.save(filename)
        counter += 1

def encode_qrcode():   
    if args.filename is 'barcode':
        args.filename = 'qrcode'
    counter = 1 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    for code in args.code:
        if len(args.code) > 1:
            filename = "%s_%02d" %(args.filename, counter) 
        else:
            filename = args.filename 
        factory = qrcode.image.svg.SvgPathImage
        img = qrcode.make(code, image_factory=factory)
        svg = filename + '.svg'
        img.save(svg)
        if args.png:
            qr.add_data(code)
            qr.make(fit=True)
            img = qr.make_image()
            png = filename + '.png'
            img.save(png)        
            qr.clear()
        counter +=1 

def decode_qrcode():
    for img in args.code:
        code = str(decode(Image.open(img)))
        # print(code)
        p = re.compile("http.+?(?=\')")
        result = p.search(code)        
        url = result.group()
        print(url)
        webbrowser.open_new_tab(url)

if args.decode:
    decode_qrcode()
else:
    if args.qrcode:
        encode_qrcode()
    else:
        encode_barcode()