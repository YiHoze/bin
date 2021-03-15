#>mytex.py template -s foo1 foo2 foo3 

import os
import sys
import glob
import argparse
import configparser
import re

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from open import FileOpener
from ltx import LatexCompiler


class LatexTemplate(object):

    def __init__(self, argv=None):    

        self.generated_files = []

        self.dbFile = 'latex.db'
        self.dbFile = os.path.join(dirCalled, self.dbFile)
        if os.path.exists(self.dbFile):
            self.database = configparser.ConfigParser()
            self.database.read(self.dbFile, encoding='utf-8')
        else:
            print('{} is not found.'.format(self.dbFile))
            sys.exit()

        self.parse_args(argv)

        if self.args.List_bool:
            self.enumerate_with_description()
        elif self.args.list_bool:
            self.enumerate_without_description()        
        elif self.args.detail_bool:
            self.show_details()
        elif self.args.update_bool:
            self.update_database()
        elif self.args.insert_bool:
            self.insert_new()
        elif self.args.burst_bool:
            self.burst_templates()
        else:
            self.make()


    def parse_args(self, argv=None):

        example = '''examples:
    mytex.py
        makes mydoc.tex out of the default template, article.
    mytex.py -l
        enumerates templates
    mytex.py metapost -d
        gives a brief description of the metapost template.
    mytex.py memoir -o foo 
        makes "foo.tex" out of the memoir template.
    mytex.py lotto -s 20 10 
        makes and compiles lotto.tex, of which two placeholders are replaced with "20" and "10".
    mytex.py lotto -n
        makes lotto.tex but doesn't compile though this template has some compilation options.
    mytex.py glyph -f
        makes and compiles myfont.tex though this template has no comilation options.
        '''
        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Create a LaTeX file from the template databse and compile it using ltx.py.'
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
            '-n',
            dest = 'defy_bool',
            action = 'store_true',
            default = False,
            help = 'Do not compile even if some compilation options are prescribed.'
        )
        parser.add_argument(
            '-f',
            dest = 'force_bool',
            action = 'store_true',
            default = False,
            help = 'Compile without opening the tex file even if no compilation option is prescribed .'
        )
        parser.add_argument(
            '-r',
            dest = 'remove_bool',
            action = 'store_true',
            default = False,
            help = 'Remove the tex and its subsidiary files after compilation.'
        )
        parser.add_argument(
            '-l',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate templates'
        )
        parser.add_argument(
            '-L',
            dest = 'List_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate tempaltes with description.'
        )
        parser.add_argument(
            '-d',
            dest = 'detail_bool',
            action = 'store_true',
            default = False,
            help = 'Show the details about the specified template.'            
        )
        parser.add_argument(
            '-i',
            dest = 'insert_bool',
            action = 'store_true',
            default = False,
            help = 'Insert a new TeX file into the database file.'
        )
        parser.add_argument(
            '-u',
            dest = 'update_bool',
            action = 'store_true',
            default = False,
            help = 'Update the database file with the files being in the current directory.'
        )
        parser.add_argument(
            '-b',
            dest = 'burst_bool',
            action = 'store_true',
            default = False,
            help = 'Take out all templates.'
        )

        self.args = parser.parse_args(argv)

    def check_section(self):

        if self.database.has_section(self.args.template):
            return True
        else:
            print('"{}" is not included in the database.'.format(self.args.template))
            return False


    def confirm_to_overwrite(self, afile):

        if os.path.exists(afile):
            answer = input('{} already exists. Are you sure to overwrite it? [y/N] '.format(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True


    def make_image_list(self, filename='images.lst', exclude='album.pdf'):

        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(exclude):
            os.remove(exclude)

        images = []
        image_type = ['pdf', 'jpg', 'jpeg', 'png']
        for img in image_type:
            for afile in glob.glob('*.' + img):
                images.append(afile)

        if len(images) == 0:
            print('No image files are found.')
            return False

        images.sort(key=str.lower)
        images = '\n'.join(images)        
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write(images)

        if self.args.remove_bool:
            self.generated_files.append(filename)

        return True


    def fill_placeholders(self, content):
        
        try:
            placeholders = int(self.database.get(self.args.template, 'placeholders'))
            defaults = self.database.get(self.args.template, 'defaults')
            defaults = defaults.split(', ')
        except:
            return content
        if self.args.substitutes is not None:
            for index, value in enumerate(self.args.substitutes):
                if index < placeholders:
                    defaults[index] = value
                else:
                    break
        cnt = 1
        for i in defaults:
            content = content.replace('\\' + str(cnt), i)
            cnt += 1
        return content


    def write_from_database(self, filename, source):

        if self.confirm_to_overwrite(filename):
            try:
                content = self.database.get(self.args.template, source)
            except:
                print('Ensure options under {} are set properly.'.format(self.args.template))
                return False
            content = content.replace('`', '')
            if os.path.splitext(filename)[1] == '.tex':
                content = self.fill_placeholders(content)
            with open(filename, mode='w', encoding='utf-8') as f:
                f.write(content)
            if self.args.remove_bool:
                self.generated_files.append(filename)
            return True
        else:
            return False


    def pick_template(self):        

        options = self.database.options(self.args.template)

        for option in options:
            if 'output' in option:
                filename = self.database.get(self.args.template, option, fallback=False)
                if filename:
                    source = option.split('_')[0]
                    if option == 'tex_output':                
                        if self.args.burst_bool and filename == 'mydoc.tex':
                            filename = self.args.template + '.tex'
                        else:
                            self.tex = filename
                    if not self.write_from_database(filename, source):
                        return False
                else:
                    print('"{}" is not specified under {}.'.format(option, self.args.template))
                    return False
        return True

    def compile(self):

        cmd = self.database.get(self.args.template, 'cmd_output', fallback=False)

        if cmd:
            answer = input('Do you want to run {}? [Y/n] '.format(cmd))
            if answer.lower() != 'n':
                os.system(cmd)
        else:
            compiler = self.database.get(self.args.template, 'compiler', fallback=False)
            if compiler:
                compiler = compiler.split(', ')
                compiler.append('-v')
                LatexCompiler(self.tex, compiler)
            else:
                if self.args.force_bool:
                    LatexCompiler(self.tex, ['-v'])

        if self.args.remove_bool:
            for i in self.generated_files:
                os.remove(i)


    def make(self):

        if not self.check_section():
            return True

        if self.args.template == 'album':            
            if not self.make_image_list():
                return 
        
        if not self.pick_template():
            return

        if not self.args.remove_bool:
            opener = FileOpener()
            opener.open_txt(self.tex)

        if not self.args.defy_bool:    
            self.compile()                


    def enumerate_with_description(self):

        templates = sorted(self.database.sections(), key=str.casefold)
        for i in templates:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            else:
                description = description.split('\n')[0]
            print('{:16} {}'.format(i, description))


    def enumerate_without_description(self, columns=4):  

        """Print the list of template names."""  
        templates = sorted(self.database.sections(), key=str.casefold)
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

        if not self.check_section():
            return True

        usage = self.database.get(self.args.template, 'description', fallback=None)
        if usage == None:
            print('"{}" has no decription'.format(self.args.template))
        else: 
            print('\n{}\n'.format(usage))


    def update_database(self):

        if not self.check_section():
            return True

        options = self.database.options(self.args.template)
        for option in options:
            if 'output' in option:
                filename = self.database.get(self.args.template, option)
                source = option.split('_')[0]
                self.comply_ini_syntax(filename, source)

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully updated.')


    def if_exits(self, filename):

        if os.path.exists(filename):
            return True
        else:
            print('"{}" does not exist in the current directory.'.format(filename))
            return False


    def insert_new(self):

        filename = os.path.basename(self.args.template)
        if not self.if_exits(filename):
            return
        
        name = os.path.splitext(filename)[0]
        if name in self.database.sections():
            print('"{}" is already included in the database.'.format(name))
            return

        self.args.template = name
        self.database.add_section(name)
        self.database.set(name, 'description', '')
        self.database.set(name, 'tex_output', filename)
        self.comply_ini_syntax(filename, 'tex')

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully inserted.')


    def comply_ini_syntax(self, filename, source):

        if not self.if_exits(filename):
            return

        with open(filename, mode='r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub('%', '%%', content)
        if os.path.splitext(filename)[1] != '.cmd':
            content = re.sub('\n', '\n`', content)
        self.database.set(self.args.template, source, content)


    def burst_templates(self):

        templates = self.database.sections()
        for i in templates:
            self.args.template = i
            self.pick_template()


if __name__ == '__main__':
    LatexTemplate()
