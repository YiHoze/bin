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

        parser = argparse.ArgumentParser(
            description = 'Extract a script from "scripts.db" to run it.'
        )
        parser.add_argument(
            'script',
            nargs = '?'
        )
        parser.add_argument(
            '-B',
            dest = 'burst',
            action = 'store_true',
            default = False,
            help = 'Take out all scripts.'
        )
        parser.add_argument(
            '-H',
            dest = 'script_help',
            action = 'store_true',
            default = False,
            help = 'Display the help of the specified python script.'
        )

        self.args, self.unknown_arguments = parser.parse_known_args()
        self.script = self.args.script
        self.burst_bool = self.args.burst
        self.script_help_bool = self.args.script_help
        self.run = True  
        self.script_arguments = self.unknown_arguments.copy()     

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
                content = self.database.get(self.script, source)                
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
            if not self.database.has_section(self.script):
                print('"{}" does not exist.'.format(self.script))
                return

        options=self.database.options(self.script)
        for i, option in enumerate(options):
            if 'output' in option:
                filename = self.database.get(self.script, option)
                source = option.split('_')[0]
                if not self.write_from_database(source, filename):
                    return

        if self.run:
            ext = os.path.splitext(filename)[1]
            if ext == '.ps1':
                self.script_arguments.insert(0,'powershell.exe ./{}'.format(filename))
            else:
                self.script_arguments.insert(0, filename)
            if ext == '.py' and self.script_help_bool:
                self.script_arguments.insert(1, '-h')
            cmd = ' '.join(self.script_arguments)
            print(cmd)
            os.system(cmd)


    def burst_scripts(self):

        self.run = False
        scripts = sorted(self.database.sections(), key=str.casefold)

        for i in scripts:
            self.script = i
            self.pick_script()


    def enumerate_scripts(self):

        scripts = sorted(self.database.sections(), key=str.casefold)

        for i in scripts:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            print('{:20} {}'.format(i,description))
 

if __name__ == '__main__':
    SS = ScriptScribe()
    if SS.burst_bool:
        SS.burst_scripts()
    elif SS.script:
        SS.pick_script()
    else:     
        SS.enumerate_scripts()
