import os
import sys
import glob
import argparse
import configparser
import subprocess

class ImageUtility(object):
    def __init__(self, images=None,
        Magick=None, Inkscape=None, info=False, 
        target='pdf', resize=False, density=100, maxwidth=0, scale=100, gray=False,
        recursive=False):
        self.images = images
        self.Magick = Magick
        self.Inkscape = Inkscape
        self.info_bool = info
        self.trgfmt = target
        self.resize_bool = resize
        self.density = density
        self.maxwidth = maxwidth
        self.scale = scale
        self.gray_bool = gray
        self.recursive = recursive
        self.vectors = ('.eps', '.pdf', '.svg')
        self.bitmaps = ('.bmp', '.cr2', '.gif', '.jpg', '.pbm', '.png', '.ppm', '.tga', '.webp')
        self.cnt = 0
        self.initialize()

    def initialize(self):
        inipath = os.path.dirname(__file__)
        ini = os.path.join(inipath, 'docenv.ini')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            try:
                self.Inkscape = config.get('Inkscape', 'path')                
            except:
                print('Make sure to have docenv.ini set properly with Inkscape.')
                self.Inkscape = 'inkscape.com'
            try:
                self.Magick = config.get('ImageMagick', 'path')
            except:
                print('Make sure to have docenv.ini set properly with ImageMagick.')  
                self.Magick = 'magick.exe'
        else:
            print('Docenv.ini is not found in %s.' %(inipath))
            self.Inkscape = 'inkscape.com'
            self.Magick = 'magick.exe'

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = "This script requires TeX Live, Inkscape, and ImageMagick. With this script you can: 1) view bitmap images' information; 2) resize bitmap images by changing their resolution or scale; 3) convert bitmap images to another format; 4) convert vector images to another vector or bitmap format. Be aware that SVG cannot be the target format."
        )
        parser.add_argument(
            'images',
            nargs = '+',
            help = 'Specify one or more images.'
        )
        parser.add_argument(
            '-i',
            dest = 'info',
            action = 'store_true',
            default = False,
            help = "Display bitmap images' information."
        )
        parser.add_argument(
            '-t',
            dest = 'trgfmt',
            default = 'pdf',
            help = 'Specify a target format. (default: pdf)'
        )
        parser.add_argument(
            '-r',
            dest = 'resize',
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
            '-g',
            dest = 'gray',
            action = 'store_true',
            default = False,
            help = 'Covert bitmap images to grayscale.'
        )
        parser.add_argument(
            '-R',
            dest = 'recursive',
            action = 'store_true',
            default = False,
            help = 'Process ones in all subdirectories'
        )
        args = parser.parse_args()
        self.images = args.images
        self.info_bool = args.info
        self.trgfmt = args.trgfmt
        self.resize_bool = args.resize
        self.density = args.density
        self.maxwidth = args.maxwidth
        self.scale = args.scale
        self.recursive = args.recursive
        self.gray_bool = args.gray 

    def check_TeXLive(self):
        try:
            subprocess.check_call('epstopdf.exe --version')
            return True
        except OSError:
            print("Make sure TeX Live is included in PATH.")
            return False

    def check_Inkscape(self):
        try:
            subprocess.check_call(self.Inkscape + ' --version')
            return True
        except OSError:
            print("Check the path to Inkscape.")
            return False

    def check_ImageMagick(self):
        try:
            subprocess.check_call(self.Magick + ' --version')
            return True
        except OSError:
            print("Check the path to ImageMagick.")
            return False

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
            print('%s is not covered.' %(ext))
            return False

    def get_subdirs(self):
        return [x[0] for x in os.walk('.')]

    def run_recursive(self, func):
        if self.recursive:
            subdirs = self.get_subdirs()
            for subdir in subdirs:
                for fnpattern in self.images:            
                    fnpattern = os.path.join(subdir, fnpattern)
                    for img in glob.glob(fnpattern):                        
                        func(img)
        else:
            for fnpattern in self.images:
                for img in glob.glob(fnpattern):
                    func(img)

    def get_info(self, img):
        if self.check_format(img) == 'bitmap':
            cmd = '\"%s\" identify -verbose %s' %(self.Magick, img)
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)   
            result = result.decode(encoding='utf-8')            
            result = result.split('\r\n')
            print('\n %s' %(img))
            line = 4
            while line < 8:
                print(result[line])
                line += 1  

    def resize_bitmap(self, img):
        if self.check_format(img) == 'bitmap':
            if self.maxwidth > 0:
                cmd = '"%s" "%s"  -resize %dx%d^> "%s"' % (self.Magick, img, self.maxwidth, self.maxwidth, img)
                subprocess.run(cmd)
            cmd = '"%s" "%s" -auto-orient -units PixelsPerCentimeter -density %d -resize %d%%  "%s"' % (self.Magick, img, self.density, self.scale, img)            
            subprocess.run(cmd)
            self.cnt += 1

    def name_target(self, img):
        filename, ext = os.path.splitext(img)
        ext = ext.lower()
        if ext == '.gif':
            trg = filename + "%03d" + self.trgfmt
        else:
            trg = filename + self.trgfmt
        return trg
    
    def bitmap_to_bitmap(self, img):
        trg = self.name_target(img)
        cmd = '"%s" "%s" -units PixelsPerCentimeter -density %d' %(self.Magick, img, self.density)
        if self.gray_bool:
            cmd = cmd + ' -colorspace gray'
        cmd = cmd + ' "%s"' %(trg)   
        subprocess.run(cmd)
        self.cnt += 1 

    def count_pdf_pages(self, img):
        ext = os.path.splitext(img)[1]
        if ext.lower() == '.pdf':
            cmd = 'pdfinfo.exe ' + img
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            result = str(result).split('\\r\\n')
            for i in result:
                if 'Pages:' in i:
                    tmp = i.replace('Pages:', '')                    
                    return int(tmp)
        else:
            return 0

    def vector_to_bitmap(self, img):        
        trg = self.name_target(img)
        cmd = '"%s" -density 254 "%s" "%s"' %(self.Magick, img, trg)
        subprocess.run(cmd)
        page_count = self.count_pdf_pages(img)
        if page_count > 1:
            filename, ext = os.path.splitext(trg)
            trg = filename + '*' + ext
        for i in glob.glob(trg):
            cmd = '"%s" "%s" -units PixelsPerCentimeter -density 100 "%s"' % (self.Magick, i, i)
            subprocess.run(cmd)
        self.cnt += 1

    def eps_to_pdf(self, img):
        cmd = 'epstopdf.exe "%s"' %(img)
        subprocess.run(cmd)
        self.cnt += 1

    def pdf_to_eps(self, img):
        cmd = 'pdftops -eps "%s"' %(img)
        subprocess.run(cmd)
        self.cnt += 1

    def svg_to_pdf(self, img):
        trg = self.name_target(img)
        cmd = '"%s" --export-pdf "%s" "%s"' %(self.Inkscape, trg, img)
        subprocess.run(cmd)
        cmd = 'pdfcrop.exe "%s" "%s"' %(trg, trg)
        subprocess.run(cmd)
        self.cnt += 1

    def svg_to_eps(self, img):
        trg = self.name_target(img)
        cmd = '"%s" --export-eps "%s" "%s"' %(self.Inkscape, trg, img)
        subprocess.run(cmd)  
        self.cnt += 1

    def convert(self):
        recipe = {}
        self.trgfmt = self.trgfmt.lower()
        if not self.trgfmt.startswith('.'):
            self.trgfmt = '.' + self.trgfmt        
        recipe['target format'] = self.trgfmt
        recipe['target type'] = self.check_format(self.trgfmt)
        for fnpattern in self.images:
            srcfmt = os.path.splitext(fnpattern)[1]
            srctype = self.check_format(srcfmt)
            recipe['source format'] = srcfmt 
            recipe['source type'] = srctype
            self.converter_diverge(recipe)
    
    def converter_diverge(self, recipe):
        if recipe['source type'] == 'bitmap':
            if recipe['target type'] == 'bitmap':
                if self.check_ImageMagick():
                    self.run_recursive(self.bitmap_to_bitmap)
            elif recipe['target format'] == '.eps' or recipe['target format'] == '.pdf':
                if self.check_ImageMagick():
                    self.run_recursive(self.bitmap_to_bitmap)

        elif recipe['source type'] == 'vector':
            if recipe['target type'] == 'bitmap':
                if recipe['source format'] == '.pdf':
                    if self.check_TeXLive() and self.check_ImageMagick():
                        self.run_recursive(self.vector_to_bitmap)
                else:
                    if self.check_ImageMagick():
                        self.run_recursive(self.vector_to_bitmap)
            elif recipe['target type'] == 'vector':
                if recipe['source format'] == '.eps' and recipe['target format'] == '.pdf':
                    if self.check_TeXLive():
                        self.run_recursive(self.eps_to_pdf)
                elif recipe['source format'] == '.pdf' and recipe['target format'] == '.eps':
                    if self.check_TeXLive():
                        self.run_recursive(self.pdf_to_eps)
                elif recipe['source format'] == '.svg':
                    if self.check_Inkscape():
                        if recipe['target format'] == '.eps':
                            self.run_recursive(self.svg_to_eps)
                        elif recipe['target format'] == '.pdf':
                            if self.check_TeXLive():
                                self.run_recursive(self.svg_to_pdf)    

    def count(self):
        if self.resize_bool:
            print('%d file(s) have been resized.' %(self.cnt))
        elif not self.info_bool:
            print('%d file(s) have been converted.' %(self.cnt))

    def diverge(self):
        if self.info_bool:
            if self.check_ImageMagick():
                self.run_recursive(self.get_info)
        elif self.resize_bool:
            if self.check_ImageMagick(): 
                self.run_recursive(self.resize_bitmap)
        else:
            self.convert()
        self.count()

if __name__ == '__main__':
    iu = ImageUtility()
    iu.parse_args()
    iu.diverge()