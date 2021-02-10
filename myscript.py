import os
import sys
import glob
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
        
        self.script_arguments = ''
        if len(sys.argv) == 1:
            self.script = None
        else:            
            self.script = sys.argv[1]
            if len(sys.argv) > 2:            
                del sys.argv[0]
                del sys.argv[0]
                self.script_arguments = ' '.join(sys.argv)
       

    def confirm_to_overwrite(self, afile):

        if os.path.exists(afile):
            answer = input('"{}" already exists. Are you sure to overwrite it? [y/N] '.format(afile))
            if answer.lower() == 'y':
                os.remove(afile)
                return True
            else:
                return False
        else:
            return True


    def write_from_database(self):

        filename = self.database.get(self.script, 'output', fallback=None)
        if filename is None:
            print('Ensure the script database file is set properly.')
            return 

        if self.confirm_to_overwrite(filename):
            try:
                content = self.database.get(self.script, 'content')
                if os.path.splitext(filename)[1] != '.cmd':
                    content = content.replace('`', '')
                with open(filename, mode='w', encoding='utf-8') as f:
                    f.write(content)
            except:
                print('Ensure the script database file is set properly.')
                return

        cmd = '{} {}'.format(filename, self.script_arguments)
        if os.path.splitext(filename)[1] == '.ps1':
            cmd = 'powershell.exe ./' + cmd        
        # print(cmd)
        os.system(cmd)        


    def enumerate_scripts(self):

        scripts = sorted(self.database.sections(), key=str.casefold)

        for i in scripts:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            print('{:20} {}'.format(i,description))
 

if __name__ == '__main__':
    SS = ScriptScribe()
    if SS.script is None:
        SS.enumerate_scripts()
    else:
        SS.write_from_database()


        



