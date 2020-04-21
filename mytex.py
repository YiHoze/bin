#>mytex.py template -s foo1 foo2 foo3 

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

    def __init__(self, template='hzguide', substitutes=None, output=None, compile=True):
        self.template = template
        self.substitutes = substitutes
        self.output = output
        self.compile_bool = compile
        self.list_bool = False
        self.ini_bool = self.initialize()    

    def initialize(self):
        tpl = os.path.join(dirCalled, 'latex.tpl')
        if os.path.exists(tpl):
            self.templates = configparser.ConfigParser()
            self.templates.read(tpl, encoding='utf-8')
            return True
        else:
            print('latex.tpl is not found.')
            return False

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Create a LaTeX file from several templates.'
        )
        parser.add_argument(
            'template',
            type = str,
            nargs = '?',
            default = 'article',
            help = 'Choose a template.'
        )
        parser.add_argument(
            '-s',
            dest = 'substitutes',
            nargs = '*',
            help = 'Specify strings which to replace the tex file with.'
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
        parser.add_argument(
            '-d',
            dest = 'detail',
            action = 'store_true',
            default = False,
            help = 'Show the details about the specified template.'            
        )
        args = parser.parse_args()
        self.template = args.template
        self.substitutes = args.substitutes
        self.output = args.output
        self.list_bool = args.list
        self.detail_bool = args.detail
        self.compile_bool = args.compile

    def confirm_to_remove(self, afile):
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
            filename = self.templates.get(self.template, 'output', fallback='mydoc')
        else:
            filename = self.output
            filename = os.path.splitext(filename)[0]
        self.tex = filename + '.tex'
        self.pdf = filename + '.pdf'
        self.sty = filename + '.sty'
        self.cmd = filename + '.cmd'         

    def make_image_list(self):
        image_list_file = self.templates.get('album', 'image_list', fallback='im@ges.txt')
        if os.path.exists(image_list_file):
            os.remove(image_list_file)
        if os.path.exists(self.pdf):
            os.remove(self.pdf)
        # Make a file the contains a list of image files
        images = []
        image_type = ['pdf', 'jpg', 'jpeg', 'png']
        for img in image_type:
            for afile in glob.glob('*.' + img):
                images.append(afile)
        if len(images) == 0:
            print('No image files are found.')
            return False
        images.sort()
        images = '\n'.join(images)        
        with open(image_list_file, mode='w') as f:
            f.write(images)
        return True

    def fill_placeholders(self, content):        
        content = content.replace('`', '')
        try:
            placeholders = int(self.templates.get(self.template, 'placeholders'))
            defaults = self.templates.get(self.template, 'defaults')
            defaults = defaults.split(', ')
        except:
            return content
        if self.substitutes is not None:
            for index, value in enumerate(self.substitutes):
                if index < placeholders:
                    defaults[index] = value
                else:
                    break
        cnt = 1
        for i in defaults:
            content = content.replace('\\' + str(cnt), i)
            cnt += 1
        return content

    def write_from_template(self):
        # writing commmand
        content = self.templates.get(self.template, 'command', fallback=None)
        if content is not None:
            content = content.replace('\\TEX', self.tex)
            content = content.replace('\\PDF', self.pdf)
            if self.confirm_to_remove(self.cmd):
                with open(self.cmd, mode='w', encoding='utf-8') as f:
                    f.write(content)
        # writing style
        content = self.templates.get(self.template, 'style', fallback=None)
        if content is not None:
            content = content.replace('`', '')            
            if self.confirm_to_remove(self.sty):
                with open(self.sty, mode='w', encoding='utf-8') as f:
                    f.write(content)            
        # writing latex
        if not self.confirm_to_remove(self.tex):
            return False
        try:
            content = self.templates.get(self.template, 'tex')
            content = self.fill_placeholders(content)
        except:
            print('Make sure to have latex.tpl set properly.')
            return False
        with open(self.tex, mode='w', encoding='utf-8') as f:
            f.write(content)

        opener = FileOpener()
        opener.OpenTxt(self.tex)
        return True

    def compile(self):
        compile_option = self.templates.get(self.template, 'compile_option', fallback=None)
        if compile_option is not None:
            compile_option = compile_option.split(', ')
            texer = LatexCompiler(self.tex)
            compile_option.append('-v')
            texer.parse_args(compile_option)
            texer.compile()   

    def make(self):
        if not self.templates.has_section(self.template):
            print('"{}" is not defined.'.format(self.template))
            return False
        self.determine_filename()
        if self.template == 'album':            
            if self.make_image_list() is False:
                return 
        if self.write_from_template():            
            if self.compile_bool:
                self.compile()                

    def show_templates(self):      
        """Print the list of template names."""  
        templates = ', '.join(sorted(self.templates.sections()))
        print(templates)

    def show_details(self):
        if not self.templates.has_section(self.template):
            print('"{}" is not defined.'.format(self.template))
            return 
        usage = self.templates.get(self.template, 'description', fallback=None)
        if usage == None:
            print('"{}" has no decription'.format(self.template))
        else: 
            print('\n{}\n'.format(usage))
 
if __name__ == '__main__':
    mytex = LatexTemplate()
    if mytex.ini_bool:
        mytex.parse_args()
        if mytex.list_bool:
            mytex.show_templates()
        elif mytex.detail_bool:
            mytex.show_details()
        else:
            mytex.make()