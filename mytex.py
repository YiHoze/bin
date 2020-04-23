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
            dest = 'defy',
            action = 'store_true',
            default = False,
            help = 'Do not compile even if some compile options are prescribed.'
        )
        parser.add_argument(
            '-f',
            dest = 'force',
            action = 'store_true',
            default = False,
            help = 'Compile even if no compile option is prescribed .'
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
        self.defy_bool = args.defy
        self.force_bool = args.force

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
            self.filename = self.templates.get(self.template, 'output', fallback='mydoc')
        else:
            filename = self.output
            self.filename = os.path.splitext(filename)[0]        
        self.tex = self.filename + '.tex'        

    def make_image_list(self):
        image_list_file = self.templates.get('album', 'image_list', fallback='im@ges.txt')
        if os.path.exists(image_list_file):
            os.remove(image_list_file)
        pdf = self.filename + '.pdf'
        if os.path.exists(pdf):
            os.remove(pdf)
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
            content = content.replace('\\PDF', self.filename + '.pdf')
            cmd = self.filename + '.cmd'         
            if self.confirm_to_remove(cmd):
                with open(cmd, mode='w', encoding='utf-8') as f:
                    f.write(content)
        # writing style
        content = self.templates.get(self.template, 'style', fallback=None)
        if content is not None:
            content = content.replace('`', '')            
            sty = self.filename + '.sty'
            if self.confirm_to_remove(sty):
                with open(sty, mode='w', encoding='utf-8') as f:
                    f.write(content)            
        # writing bib
        content = self.templates.get(self.template, 'bib', fallback=None)
        if content is not None:
            content = content.replace('`', '')            
            bib = self.filename + '.bib'
            if self.confirm_to_remove(bib):
                with open(bib, mode='w', encoding='utf-8') as f:
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
        if self.defy_bool:
            return

        compiler = self.templates.get(self.template, 'compiler', fallback=None)
                
        if compiler is None:
            if self.force_bool:
                texer = LatexCompiler(self.tex)
                texer.parse_args(['-v'])
                texer.compile()   
        else:       
            compiler = compiler.split(', ')
            compiler.append('-v')                
            texer = LatexCompiler(self.tex)
            texer.parse_args(compiler)        
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
            self.compile()                

    def show_templates(self, columns=4):      
        """Print the list of template names."""  
        templates = sorted(self.templates.sections())
        width = 0
        for i in templates:
            width = max(width, len(i))
        width += 4
        i = 0
        while i < len(templates):
            line = ''
            for j in range(columns):
                k = i + j
                if k < len(templates):
                    line += '{:{w}}'.format(templates[k], w=width)
                else:
                    break
            i += columns
            print(line)

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