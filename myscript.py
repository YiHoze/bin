import os
import sys
import glob
import argparse
import configparser
import subprocess
import re

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))


class ScriptScribe(object):

    def __init__(self):

        self.dbFile = 'scripts.db'
        self.dbFile = os.path.join(dirCalled, self.dbFile)
        if os.path.exists(self.dbFile):
            self.database = configparser.ConfigParser()
            self.database.read(self.dbFile, encoding='utf-8')
        else:
            print('{} is not found.'.format(self.dbFile))
            sys.exit()

        self.parse_args()

        if self.args.script:
            if self.args.update_bool:
                self.update()
            elif self.args.insert_bool:
                self.insert_new()
            elif self.args.remove_bool:
                self.remove()
            else:
                self.pick_script()
        else:
            if self.args.burst_bool:
                self.burst_database()
            else:
                self.parser.print_help()
                self.enumerate_scripts()



    def parse_args(self):

        self.parser = argparse.ArgumentParser(
            add_help=False,
            description = 'Extract a script from "scripts.db" to run it.'
        )
        self.parser.add_argument(
            'script',
            nargs = '?'
        )
        self.parser.add_argument(
            '-I',
            dest = 'insert_bool',
            action = 'store_true',
            default = False,
            help = 'Insert a new script file into the database file.'
        )
        self.parser.add_argument(
            '-U',
            dest = 'update_bool',
            action = 'store_true',
            default = False,
            help = 'Update the database with the file being in the current directory.'
        )
        self.parser.add_argument(
            '-R',
            dest = 'remove_bool',
            action = 'store_true',
            default = False,
            help = 'Remove the specified script from the database.'
        )
        self.parser.add_argument(
            '-B',
            dest = 'burst_bool',
            action = 'store_true',
            default = False,
            help = 'Take out every script.'
        )
        self.parser.add_argument(
            '-N',
            dest = 'run_bool',
            action = 'store_false',
            default = True,
            help = 'Extract but do not run the specified script.'
        )
        self.parser.add_argument(
            '-C',
            dest = 'clear_bool',
            action = 'store_true',
            default = False,
            help = 'Delete the extracted script file after a run.'
        )


        self.args, self.script_arguments = self.parser.parse_known_args()


    def check_section(self):

        if self.database.has_section(self.args.script):
            return True
        else:
            print('"{}" is not included in the database.'.format(self.args.script))
            return False


    def confirm_to_overwrite(self, afile):

        if not self.args.run_bool:
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


    def write_from_database(self, filename, source):

        if self.confirm_to_overwrite(filename):
            try:
                content = self.database.get(self.args.script, source)
            except:
                print('Ensure the script database is set properly.')
                return False
            if os.path.splitext(filename)[1] != '.cmd':
                content = content.replace('`', '')
            with open(filename, mode='w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False


    def pick_script(self):

        if self.args.run_bool:
            if not self.check_section():
                return

        options=self.database.options(self.args.script)
        for option in options:
            if 'output' in option:
                filename = self.database.get(self.args.script, option)
                if option == 'code_output':
                    codefile = filename
                source = option.split('_')[0]
                if not self.write_from_database(filename, source):
                    return

        if self.args.run_bool:
            ext = os.path.splitext(codefile)[1]
            if ext == '.ps1':
                self.script_arguments.insert(0,'powershell.exe ./{}'.format(codefile))
            else:
                self.script_arguments.insert(0, codefile)

            cmd = ' '.join(self.script_arguments)
            if len(self.script_arguments) < 2:
                sargs = self.database.get(self.args.script, 'default_arguments', fallback=None)
                if sargs:
                    cmd = '{} {}'.format(cmd, sargs)

            print(cmd)
            os.system(cmd)

            if self.args.clear_bool:
                os.remove(codefile)


    def if_exits(self, filename):

        if os.path.exists(filename):
            return True
        else:
            print('"{}" does not exist in the current directory.'.format(filename))
            return False


    def read_script_file(self, filename):

        ext = os.path.splitext(filename)[1]

        if ext == '.py':
            script_type = '[Python]'
        elif ext == '.ps1':
            script_type = '[PowerShell]'
        elif ext == '.cmd':
            script_type = '[cmd]'
        else:
            script_type = '[Unknown]'

        with open(filename, mode='r', encoding='utf-8') as f:
            code = f.read()
        code = re.sub('%', '%%', code)
        if os.path.splitext(filename)[1] != '.cmd':
            code = re.sub('^', '`', code, flags=re.MULTILINE)

        found = re.search('(?<= description = ).*$', code, flags=re.MULTILINE)
        if found:
            description = found.group(0)
            description = re.sub("^'", "", description)
            description = re.sub("'\n", "", description)
            description = '{} {}'.format(script_type, description)
        else:
            description = script_type

        return description, code

    def insert_new(self):

        filename = os.path.basename(self.args.script)
        if not self.if_exits(filename):
            return

        name = os.path.splitext(filename)[0]
        if name in self.database.sections():
            print('"{}" is already included in the database.'.format(name))
            return

        description, code = self.read_script_file(filename)

        self.database.add_section(name)
        self.database.set(name, 'description', description)
        self.database.set(name, 'code_output', filename)
        self.database.set(name, 'code', code)

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully inserted.')


    def update(self):

        if not self.check_section():
            return

        filename = self.database.get(self.args.script, 'code_output')
        if not self.if_exits(filename):
            return

        description, code = self.read_script_file(filename)

        self.database.set(self.args.script, 'description', description)
        self.database.set(self.args.script, 'code', code)

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully updated.')


    def remove(self):

        if not self.check_section():
            return

        answer = input('Are you sure to remove "{}" from the database? [y/N]'.format(self.args.script))
        if answer.lower() == 'y':
            self.database.remove_section(self.args.script)
            with open(self.dbFile, mode='w', encoding='utf-8') as f:
                self.database.write(f)
                print('Successfully removed.')


    def enumerate_scripts(self):

        scripts = sorted(self.database.sections(), key=str.casefold)

        print()
        for i in scripts:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            print('{:12} {}'.format(i,description))


    def burst_database(self):

        self.args.run_bool = False
        scripts = sorted(self.database.sections(), key=str.casefold)

        for i in scripts:
            self.script = i
            self.pick_script()

if __name__ == '__main__':
    ScriptScribe()