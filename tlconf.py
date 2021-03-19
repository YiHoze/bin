
import os
import sys
import configparser
import argparse
import glob
import subprocess


class TeXLiveConfigure(object):

    def __init__(self):

        self.initialize()
        self.check_TeXLive()        
        self.parse_args()
        self.configure()


    def initialize(self):

        self.inipath = os.path.dirname(__file__)
        ini = os.path.join(self.inipath, 'docenv.ini')
        if os.path.exists(ini):
            self.config = configparser.ConfigParser()
            self.config.read(ini)
        else:
            print('docenv.ini is not found.')
            sys.exit()


    def check_TeXLive(self):

        try:
            subprocess.check_call('mktexlsr.exe --version')
        except OSError:
            print("Make sure TeX Live is included in PATH.")
            sys.exit()


    def parse_args(self):

        parser = argparse.ArgumentParser(
            description ='Configure your documentation environment for LaTeX.'
        )
        # parser.add_argument(
        #     '-s',
        #     dest = 'store_to_local',
        #     action = 'store_true',
        #     default = False,
        #     help = 'Copy the provided latex class and style files into the local TEXMF directory.'
        # )
        parser.add_argument(
            '-H',
            dest = 'texmfhome',
            action = 'store_true',
            default = False,
            help = 'Set TEXMFHOME as an environment variable.'
        )
        parser.add_argument(
            '-C',
            dest = 'texmf_cnf',
            action = 'store_true',
            default = False,
            help = "Add user's local font directory to texmf.cnf."
        )
        parser.add_argument(
            '-L',
            dest = 'local_conf',
            action = 'store_true',
            default = False,
            help = "Create local.conf for which to include user's local font directory."
        )
        parser.add_argument(
            '-e',
            dest = 'texedit',
            action = 'store_true',
            default = False,
            help = 'Set TEXEDIT as an environment variable.'
        )
        parser.add_argument(
            '-p',
            dest = 'sumatrapdf',
            action = 'store_true',
            default = False,
            help = 'Set SumatraPDF to enable inverse search. (jumping back to the corresponding point in the source tex file)'
        )
        parser.add_argument(
            '-r',
            dest = 'set_repository',
            action = 'store_true',
            default = False,
            help = 'Set the main TeX Live repository.'
        )
        parser.add_argument(
            '-u',
            dest = 'update_texlive',
            action = 'store_true',
            default = False,
            help = 'Update TeX Live.'
        )
        parser.add_argument(
            '-c',
            dest = 'cache_font',
            action = 'store_true',
            default = False,
            help = 'Cache fonts for XeLaTeX.'
        )
        parser.add_argument(
            '-l',
            dest = 'luaotfload',
            action = 'store_true',
            default = False,
            help = 'Update the font database for LuaLaTeX.'
        )
        parser.add_argument(
            '-b',
            dest = 'batch',
            action = 'store_true',
            default = False,
            help = 'Get every option done at once.'
        )
        parser.add_argument(
            '-q',
            dest = 'confirmation_bool',
            action = 'store_false',
            default = True,
            help = 'Proceed without asking for confirmation.'
        )

        self.args = parser.parse_args()


    def confirm(self, msg):

        if self.args.confirmation_bool:
            answer = input(msg)
            return answer
        else:
            return 'y'


    def store_to_local(self):

        print('\n[Copying latex style files]')
        try:
            latex_style = self.config.get('Sphinx Style', 'latex')
            texmf_local = self.config.get('TeX Live', 'texmflocal')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'These files are going to be copied into <{}>\n{}\nEnter [Y] to proceed, [n] to abandon, or another directory: '.format(texmf_local, latex_style.replace(', ', '\n'))
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        if not (answer.lower() == 'y' or answer == ''):
            texmf_local = answer
        files = latex_style.split(', ')
        for afile in files:
            src = os.path.join(self.inipath, afile)
            if os.path.exists(src):
                cmd = 'copy {} {}'.format(src, texmf_local)
                os.system(cmd)
        cmd = 'dir {}'.format(texmf_local)
        os.system(cmd)
        os.system('mktexlsr.exe')


    def set_texmfhome(self):

        print('\n[Setting TEXMFHOME]')
        try:
            texmfhome = self.config.get('TeX Live', 'TEXMFHOME')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'Are you sure to set the TEXMFHOME environment variable to  <{}>?\nEnter [Y] to proceed, [n] to abandon, or another path: '.format(texmfhome)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        if not (answer.lower() == 'y' or answer == ''):
            texmfhome = answer
        cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXMFHOME -value '{}'\"".format(texmfhome)
        os.system(cmd)
        cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXMFHOME'\""
        os.system(cmd)


    def set_texedit(self):

        print('\n[Setting TEXEDIT]')
        try:
            texedit = self.config.get('TeX Live', 'TEXEDIT')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'Are you sure to set the TEXEDIT environment variable to  <{}>?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: '.format(texedit)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        if not (answer.lower() == 'y' or answer == ''):
            texedit = answer
        cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXEDIT -value '{}'\"".format(texedit)
        os.system(cmd)
        cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXEDIT'\""
        os.system(cmd)


    def set_sumatrapdf(self):

        print('\n[Setting SumatraPDF')
        try:
            sumatra = self.config.get('SumatraPDF', 'path')
            editor = self.config.get('SumatraPDF', 'inverse-search')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'Are you sure to use <{}> to enable the inverse search feature of SumatraPDF?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: '.format(editor)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        if not (answer.lower() == 'y' or answer == ''):
            editor = answer
        cmd = []
        cmd.append(sumatra)
        cmd.append('-inverse-search')
        cmd.append(editor)
        subprocess.Popen(cmd)


    def modify_texmf_cnf(self):

        print('\n[texmf.cnf]')
        try:
            texmf_cnf = self.config.get('TEXMF.CNF', 'path')
            target = self.config.get('TEXMF.CNF', 'target')
            substitute = self.config.get('TEXMF.CNF', 'substitute')
        except:
            print('Make sure to have docenv.ini set properly')
            return
        query = "'{}' will be replaced with '{}' in <{}>\nEnter [Y] to proceed, [n] to abandon.".format(target, substitute, texmf_cnf)
        answer = self.confirm(query)
        if (answer.lower() == 'n'):
            return
        else:
            with open(texmf_cnf, mode='r') as f:
                content = f.read()
                content = content.replace(target, substitute)
            with open(texmf_cnf, mode='w') as f:
                f.write(content)


    def create_local_conf(self):

        print('\n[local.conf]')
        try:
            local_conf = self.config.get('LOCAL.CONF', 'path')
            content = self.config.get('LOCAL.CONF', 'content')
        except:
            print('Make sure to have docenv.ini set properly')
            return
        query = "<{}> will be created to include {}\nEnter [Y] to proceed, [n] to abandon.".format(local_conf, content)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        else:
            with open(local_conf, mode='w') as f:
                f.write(content)


    def update_texlive(self):

        print('\n[Updating the TeX Live]')
        query = 'Are you sure to update the TeX Live?\nEnter [Y] to proceed or [n] to abandon: '
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        else:
            os.system('tlmgr.bat update --self --all')


    def set_repository(self):

        repository = self.get_repository('main')
        if repository:
            os.system('tlmgr.bat option repository {}'.format(repository))
        repository = self.get_repository('private')
        if repository:
            os.system('tlmgr.bat repository add {} private'.format(repository))
            os.system('tlmgr.bat pinning add private')
        os.system('tlmgr.bat repository list')


    def get_repository(self, kind):

        print('\n[Setting the {} repository]'.format(kind))
        option = 'repository_{}'.format(kind)
        url = self.config.get('TeX Live', option, fallback=False)
        if url:
            query = 'Are you sure to set <{}> as the {} repository?\nEnter [Y] to proceed, [n] to abandon, or another repository: '.format(url, kind)
            answer = self.confirm(query)
            if (answer.lower() == 'y' or answer == ''):
                return url
            elif answer.lower() == 'n':
                return False
            else:
                return answer
        else:
            return False
        

    def cache_font(self):

        print('\n[Caching fonts]')
        query = 'Are you sure to cache fonts for XeLaTeX?\nEnter [Y] to proceed or [n] to abandon: '
        answer = self.confirm(query)
        if (answer.lower() == 'y' or answer == ''):
            cmd = 'fc-cache.exe -v -r'
            os.system(cmd)


    def luaotfload(self):

        query = 'Are you sure to update the font database for LuLaTeX?\nEnter [Y] to proceed or [n] to abandon: '
        answer = self.confirm(query)
        if (answer.lower() == 'y' or answer == ''):
            cmd = 'luaotfload-tool --update --force --verbose=3'
            os.system(cmd)


    def ToContinue(self, func):

        if self.args.confirmation_bool:
            query = '\nDo you want to continue this batch configuration? [Y/n] '
            answer = self.confirm(query)
        else:
            answer = 'y'
        if answer.lower() == 'n':
            return False
        else:
            func()
            return True


    def configure(self):

        if self.args.batch:
            # if not self.ToContinue(self.store_to_local):
            #     return None
            if not self.ToContinue(self.set_texmfhome):
                return None
            if not self.ToContinue(self.modify_texmf_cnf):
                return None
            if not self.ToContinue(self.create_local_conf):
                return None
            if not self.ToContinue(self.set_texedit):
                return None
            if not self.ToContinue(self.set_sumatrapdf):
                return None
            if not self.ToContinue(self.set_repository):
                return None
            if not self.ToContinue(self.update_texlive):
                return None
            if not self.ToContinue(self.cache_font):
                return None
            self.ToContinue(self.luaotfload)
        else:
            # if self.args.store_to_local:
            #     self.store_to_local()
            if self.args.texmfhome:
                self.set_texmfhome()
            if self.args.texmf_cnf:
                self.modify_texmf_cnf()
            if self.args.local_conf:
                self.create_local_conf()
            if self.args.texedit:
                self.set_texedit()
            if self.args.sumatrapdf:
                self.set_sumatrapdf()
            if self.args.set_repository:
                self.set_repository()
            if self.args.update_texlive:
                self.update_texlive()
            if self.args.cache_font:
                self.cache_font()
            if self.args.luaotfload:
                self.luaotfload()

if __name__ == '__main__':
    TeXLiveConfigure()    