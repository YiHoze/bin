import os
import sys
import glob
import argparse
import configparser

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener
from ltx import LatexCompiler

class LatexTemplate(object):

    def __init__(self, template='hzguide', output=None, compile=True):
        self.template = template
        self.output = output
        self.compile_bool = compile
        self.list_bool = False
        self.ini_bool = self.initialize()    

    def initialize(self):
        tpl = os.path.join(dirCalled, 'latex.tpl')
        if os.path.exists(tpl):
            self.templates = configparser.ConfigParser()
            self.templates.read(tpl)
            return True
        else:
            print('latex.tpl is not found.')
            return False

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Create a LaTeX file for one of the following purposes.'
        )
        parser.add_argument(
            'template',
            type = str,
            nargs = '?',
            default = 'article',
            help = 'Choose a template.'
        )
        parser.add_argument(
            '-o',
            dest = 'output',
            help = 'Specify a filename for output.'
        )
        parser.add_argument(
            '-n',
            dest = 'compile',
            action = 'store_false',
            default = True,
            help = 'Do not compile.'
        )
        parser.add_argument(
            '-l',
            dest = 'list',
            action = 'store_true',
            default = False,
            help = 'Show the list of templates.'
        )
        args = parser.parse_args()
        self.template = args.template
        self.output = args.output
        self.list_bool = args.list
        self.compile_bool = args.compile

    def check_to_remove(self, afile):
        if os.path.exists(afile):
            answer = input('%s alread exists. Are you sure to overwrite it? [y/N] ' %(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True

    def determine_filename(self):
        if self.output is None:
            try:                
                filename = self.templates.get(self.template, 'output')
            except:                
                filename = 'mytex'
        else:
            filename = self.output
            filename = os.path.splitext(filename)[0]
        self.tex = filename + '.tex'
        self.pdf = filename + '.pdf'

    def make_image_list(self):
        try:
            image_list_file = self.templates.get('album', 'image_list')
        except:
            print('Make sure to have latex.tpl set properly.')
            return False
        if self.check_to_remove(image_list_file) is False:
            return False
        # Make a file the contains a list of image files
        images = []
        image_type = ['pdf', 'jpg', 'jpeg', 'png']
        for img in image_type:
            for afile in glob.glob('*.' + img):
                images.append(afile)
        images.sort()
        images = '\n'.join(images)
        with open(image_list_file, mode='w') as f:
            f.write(images)
        return True

    def make_command_for_numbers(self):
        content = """
            xelatex %s
            pdfcrop %s @@@.pdf
            pdftk @@@.pdf burst
            """ %(self.tex, self.pdf)
        with open('circled_numbers.cmd', mode='w', encoding='utf-8') as f:
            f.write(content)

    def write_from_template(self):  
        try:
            content = self.templates.get(self.template, 'tex')
        except:
            print('Make sure to have latex.tpl set properly.')
            return False
        if not self.check_to_remove(self.tex):
            return False
        with open(self.tex, mode='w', encoding='utf-8') as f:
            f.write(content)
        opener = FileOpener()
        opener.OpenTxt(self.tex)
        return True

    def compile(self):
        try:
            compile_option = self.templates.get(self.template, 'compile_option')
            compile_option = compile_option.split(', ')
        except:
            compile_option = None
        if compile_option is not None:
            texer = LatexCompiler(self.tex)
            compile_option.append('-v')
            texer.parse_args(compile_option)
            texer.compile()   

    def make(self):
        self.determine_filename()
        if self.template == 'album':
            if self.check_to_remove(self.pdf) is False:
                return
            if self.make_image_list() is False:
                return 
        if self.write_from_template():
            if self.compile_bool:
                self.compile()
            if self.template == 'number':
                self.make_command_for_numbers()

    def show_templates(self):
        templates = ', '.join(self.templates.sections())
        print(templates)
 
if __name__ == '__main__':
    mytex = LatexTemplate()
    if mytex.ini_bool:
        mytex.parse_args()
        if mytex.list_bool:
            mytex.show_templates()
        else:
            mytex.make()
