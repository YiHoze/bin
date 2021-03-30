import os
import sys
import glob
import argparse
import configparser
import subprocess
from PyPDF2 import PdfFileReader

class ImageUtility(object):

    def __init__(self, argv=None):

        self.vectors = ('.eps', '.pdf', '.svg')
        self.bitmaps = ('.bmp', '.cr2', '.gif', '.jpg', '.jpeg', '.pbm', '.png', '.ppm', '.tga', '.tiff', '.webp')
       
        inipath = os.path.dirname(__file__)
        ini = os.path.join(inipath, 'docenv.ini')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            
            self.Inkscape = config.get('Inkscape', 'path', fallback=False)                
            if not self.Inkscape:
                print('Make sure to have docenv.ini set properly with Inkscape.')
                self.Inkscape = 'inkscape.com'
            
            self.Magick = config.get('ImageMagick', 'path', fallback=False)
            if not self.Magick:
                print('Make sure to have docenv.ini set properly with ImageMagick.')  
                self.Magick = 'magick.exe'
        else:
            print('Docenv.ini is not found in {}.'.format(inipath))
            self.Inkscape = 'inkscape.com'
            self.Magick = 'magick.exe'

        self.cnt = 0
        self.parse_args(argv)
        self.determine_task()


    def parse_args(self, argv=None):

        example = '''With this script you can: 
    1) view a bitmap image's information; 
    2) resize bitmap images by changing their resolution or scale; 
    3) convert bitmap images to another format; 
    4) convert vector images to another vector or bitmap format. 
    Be aware that SVG cannot be the target format.
examples:
    iu.py
        Supported image formats are enumerated.
    iu.py foo.eps
        foo.pdf is created from foo.eps.
    iu -t png -R *.eps
        Every EPS file, including those in all subdirectories, is converted to PNG.
    iu.py -t png *.jpg
        Every JPG file is converted to PNG.
    iu.py -i foo.jpg
        foo.jpg's details are displayed, including pixel size.
    iu.py -r foo.jpg
        foo.jpg is resized to 100 PPC by default.
    iu.py -r -d 150 foo.jpg
        foo.jpg is resized to 150 PPC.
    iu.py -r -s 75 foo.jpg
        foo.jpg is resized to 75%.
    iu.py -r -m 800 *.jpg
        JPG files wider than 800 pixels are resized.
    '''

        parser = argparse.ArgumentParser(
            epilog = example,
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = "Convert image files to other formats using TeX Live, Inkscape, and ImageMagick."
        )
        parser.add_argument(
            'images',
            nargs = '*',
            help = 'Specify one or more images.'
        )
        parser.add_argument(
            '-i',
            dest = 'info_bool',
            action = 'store_true',
            default = False,
            help = "Display bitmap images' information."
        )
        parser.add_argument(
            '-t',
            dest = 'target_format',
            default = 'pdf',
            help = 'Specify a target format. (default: pdf)'
        )
        parser.add_argument(
            '-r',
            dest = 'resize_bool',
            action = 'store_true',
            default = False,
            help = "Change bimap images' size."
        )
        parser.add_argument(
            '-d',
            dest = 'density',
            type = int,
            default = 100,
            help = "With '-r', specify a pixel density. (default: 100 pixels per centimeter)"
        )
        parser.add_argument(
            '-m',
            dest = 'maxwidth',
            type = int,
            default = 0,
            help = "With '-r', specify a max width to reduce bigger ones than it."
        )
        parser.add_argument(
            '-s',
            dest = 'scale',
            type = int,
            default = 100,
            help = "With '-r', specify a scale to be applied after checking with the max width. (default: 100 %%)"
        )
        parser.add_argument(
            '-R',
            dest = 'recursive_bool',
            action = 'store_true',
            default = False,
            help = 'Process ones in all subdirectories'
        )
        self.args = parser.parse_args(argv)


    # def check_TeXLive(self):

    #     try:
    #         subprocess.check_call('epstopdf.exe --version')
    #         return True
    #     except OSError:
    #         print("Make sure TeX Live is included in PATH.")
    #         return False


    # def check_Inkscape(self):

    #     try:
    #         subprocess.check_call(self.Inkscape + ' --version')
    #         return True
    #     except OSError:
    #         print("Check the path to Inkscape.")
    #         return False


    # def check_ImageMagick(self):

    #     try:
    #         subprocess.check_call(self.Magick + ' --version')
    #         return True
    #     except OSError:
    #         print("Check the path to ImageMagick.")
    #         return False


    def check_format(self, img):

        basename = os.path.basename(img)
        ext = os.path.splitext(basename)[1]
        if not ext:        
            ext = img
        ext = ext.lower()
        if ext in self.bitmaps:
            return 'bitmap'
        elif ext in self.vectors:
            return 'vector'
        else:
            print('{} is not covered.'.format(ext))
            return False


    def get_subdirs(self):

        return [x[0] for x in os.walk('.')]


    def run_recursive(self, func):

        if self.args.recursive_bool:
            subdirs = self.get_subdirs()
            for subdir in subdirs:
                for fnpattern in self.args.images:            
                    fnpattern = os.path.join(subdir, fnpattern)
                    for img in glob.glob(fnpattern):                        
                        func(img)
        else:
            for fnpattern in self.args.images:
                for img in glob.glob(fnpattern):
                    func(img)


    def run_cmd(self, cmd, cnt=1):

        try:
            subprocess.check_output(cmd, stderr=subprocess.PIPE)            
            self.cnt += cnt
            print(self.cnt, end='\r')
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def get_info(self, img):

        if self.check_format(img) == 'bitmap':
            cmd = '\"{}\" identify -verbose {}'.format(self.Magick, img)
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)   
            result = result.decode(encoding='utf-8')  
            result = result.split('\r\n')
            print('\n {}'.format(img))
            for n in range(4):
                print(result[n+4])


    def resize_bitmap(self, img):

        if self.check_format(img) == 'bitmap':
            if self.args.maxwidth > 0:
                cmd = '"{}"  -resize {}x{}^> "{}" "{}"'.format(self.Magick, self.args.maxwidth, self.args.maxwidth, img, img)
                self.run_cmd(cmd, 0)            
            cmd = '"{}" "{}" -auto-orient -units PixelsPerCentimeter -density {} -resize {}%  "{}"'.format(self.Magick, img, self.args.density, self.args.scale, img)            
            self.run_cmd(cmd)


    def name_target(self, img):

        filename, ext = os.path.splitext(img)
        ext = ext.lower()

        digits=1        
        if ext == '.gif':
            frames = self.count_gif_frames(img)
            digits = self.count_digits(frames)
        elif ext == '.pdf':
            pages = self.count_pdf_pages(img)
            digits = self.count_digits(pages)

        if digits > 1:
            trg = '{}_%0{}d{}'.format(filename, digits, self.args.target_format)
        else:
            trg = filename + self.args.target_format

        return trg
                


    def bitmap_to_bitmap(self, img):

        trg = self.name_target(img)
        cmd = '"{}" -units PixelsPerCentimeter -density {} "{}" "{}"'.format(self.Magick, self.args.density, img, trg)
        self.run_cmd(cmd)


    def count_digits(self, n):

        digits = 0
        while(n >= 1):
            digits += 1
            n = n /10
        return digits


    def count_gif_frames(self, img):

        cmd = '\"{}\" identify {}'.format(self.Magick, img)
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        result = result.decode(encoding='utf-8')            
        result = result.split('\n')
        return len(result)


    def count_pdf_pages(self, img):

        with open(img, 'rb') as f:
            pdf = PdfFileReader(f)
            pages = pdf.getNumPages()
        return pages


    def vector_to_bitmap(self, img):

        trg = self.name_target(img)
        cmd = '"{}" -colorspace rgb -density {}  "{}" "{}"'.format(self.Magick, self.args.density, img, trg) 
        self.run_cmd(cmd)

        if os.path.splitext(img)[1].lower() == '.pdf':        
            if self.count_pdf_pages(img) > 1:
                filename = os.path.splitext(img)[0]
                ext = os.path.splitext(trg)[1]
                trg = filename + '*' + ext
        for i in glob.glob(trg):
            cmd = '"{}" -units PixelsPerCentimeter -density 100 "{}" "{}"'.format(self.Magick, i, i)
            self.run_cmd(cmd, 0)


    def eps_to_pdf(self, img):

        cmd = 'epstopdf.exe "{}"'.format(img)
        self.run_cmd(cmd)


    def pdf_to_eps(self, img):

        cmd = 'pdftops -eps "{}"'.format(img)
        self.run_cmd(cmd)


    def svg_to_pdf(self, img):

        trg = self.name_target(img)
        cmd = '"{}" --export-pdf "{}" "{}"'.format(self.Inkscape, trg, img)
        self.run_cmd(cmd)
        cmd = 'pdfcrop.exe "{}" "{}"'.format(trg, trg)
        self.run_cmd(cmd, 0)


    def svg_to_eps(self, img):

        trg = self.name_target(img)
        cmd = '"{}" --export-eps "{}" "{}"'.format(self.Inkscape, trg, img)
        self.run_cmd(cmd)  


    def convert(self):

        recipe = {}
        self.args.target_format = self.args.target_format.lower()
        if not self.args.target_format.startswith('.'):
            self.args.target_format = '.' + self.args.target_format        
        recipe['target format'] = self.args.target_format
        recipe['target type'] = self.check_format(self.args.target_format)
        for fnpattern in self.args.images:
            srcfmt = os.path.splitext(fnpattern)[1]
            srctype = self.check_format(srcfmt)
            recipe['source format'] = srcfmt 
            recipe['source type'] = srctype
            self.converter_diverge(recipe)


    def converter_diverge(self, recipe):

        if recipe['source type'] == 'bitmap':
            if recipe['target type'] == 'bitmap':
                self.run_recursive(self.bitmap_to_bitmap)
            elif recipe['target format'] == '.eps' or recipe['target format'] == '.pdf':
                self.run_recursive(self.bitmap_to_bitmap)

        elif recipe['source type'] == 'vector':
            if recipe['target type'] == 'bitmap':
                if self.args.density == 100:
                    self.args.density = 254
                self.run_recursive(self.vector_to_bitmap)
            elif recipe['target type'] == 'vector':
                if recipe['source format'] == '.eps' and recipe['target format'] == '.pdf':
                    self.run_recursive(self.eps_to_pdf)
                elif recipe['source format'] == '.pdf' and recipe['target format'] == '.eps':
                    self.run_recursive(self.pdf_to_eps)
                elif recipe['source format'] == '.svg':
                    if recipe['target format'] == '.eps':
                        self.run_recursive(self.svg_to_eps)
                    elif recipe['target format'] == '.pdf':
                        self.run_recursive(self.svg_to_pdf)    


    def count(self):

        if self.args.resize_bool:
            print('{} file(s) have been resized.'.format(self.cnt))
        elif not self.args.info_bool:
            print('{} file(s) have been converted.'.format(self.cnt))


    def display_formats(self):

        bitmaps = ', '.join(self.bitmaps)
        vectors = ', '.join(self.vectors)
        print("Bitmap:", bitmaps)
        print("Vector:", vectors)


    def determine_task(self):

        if len(self.args.images) == 0:
            self.display_formats()
        else:          
            if self.args.info_bool:
                self.run_recursive(self.get_info)
            elif self.args.resize_bool:
                self.run_recursive(self.resize_bitmap)
            else:
                self.convert()
            self.count()


if __name__ == '__main__':
    ImageUtility()    