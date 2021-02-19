import os
import sys
import glob
import argparse
import configparser
import subprocess

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))


class ScriptScribe(object):

    def __init__(self):

        dbFile = 'scripts.db'
        db = os.path.join(dirCalled, dbFile)
        if os.path.exists(db):
            self.database = configparser.ConfigParser()
            self.database.read(db, encoding='utf-8')
        else:
            print('{} is not found.'.format(dbFile))
            sys.exit()        
        
        self.parse_args()

    def parse_args(self):

        self.parser = argparse.ArgumentParser(
            description = 'Extract a script from "scripts.db" to run it.',
            add_help=False
        )
        self.parser.add_argument(
            'script',
            nargs = '?'
        )
        self.parser.add_argument(
            '-B',
            dest = 'burst_bool',
            action = 'store_true',
            default = False,
            help = 'Take out all scripts.'
        )
        self.parser.add_argument(
            '-C',
            dest = 'clear_bool',
            action = 'store_true',
            default = False,
            help = 'Delete the script file after a run.'
        )

        self.args, self.script_arguments = self.parser.parse_known_args()
        self.run = True  


    def confirm_to_overwrite(self, afile):

        if not self.run:
            return True

        if afile is None:
            print('Ensure the script database file is set properly.')
            return False
        else:
            if os.path.exists(afile):
                answer = input('"{}" already exists. Are you sure to overwrite it? [y/N] '.format(afile))
                if answer.lower() == 'y':
                    os.remove(afile)
                    return True
                else:
                    return False
            else:
                return True


    def write_from_database(self, source, filename):        

        if self.confirm_to_overwrite(filename):
            try:
                content = self.database.get(self.args.script, source)                
            except:
                print('Ensure the script database file is set properly.')
                return False 
            
            if os.path.splitext(filename)[1] != '.cmd':
                content = content.replace('`', '')
            with open(filename, mode='w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False   

        
    def pick_script(self):

        if self.run:
            if not self.database.has_section(self.args.script):
                print('"{}" does not exist.'.format(self.args.script))
                return

        options=self.database.options(self.args.script)
        for option in options:
            if 'output' in option:
                filename = self.database.get(self.args.script, option)
                source = option.split('_')[0]
                if not self.write_from_database(source, filename):
                    return

        if self.run:
            ext = os.path.splitext(filename)[1]
            if ext == '.ps1':
                self.script_arguments.insert(0,'powershell.exe ./{}'.format(filename))
            else:
                self.script_arguments.insert(0, filename)
            cmd = ' '.join(self.script_arguments)
            print(cmd)
            os.system(cmd)

            if self.args.clear_bool:
                os.remove(filename)


    def burst_scripts(self):

        self.run = False
        scripts = sorted(self.database.sections(), key=str.casefold)

        for i in scripts:
            self.script = i
            self.pick_script()


    def enumerate_scripts(self):

        scripts = sorted(self.database.sections(), key=str.casefold)

        print()
        for i in scripts:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            print('{:12} {}'.format(i,description))
 

if __name__ == '__main__':
    SS = ScriptScribe()
    if SS.args.burst_bool:
        SS.burst_scripts()
    elif SS.args.script:
        SS.pick_script()
    else:
        SS.parser.print_help()
        SS.enumerate_scripts()
