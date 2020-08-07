import os
import sys
import configparser
import argparse
import glob
import subprocess

class TeXLiveConf(object):
    def __init__(self, confirmation=True, answer='y'):
        self.ini = self.initialize()
        self.confirmation_bool = confirmation
        self.answer = answer
        if self.ini:
            self.ini= self.check_TeXLive()

    def initialize(self):
        self.inipath = os.path.dirname(__file__) 
        ini = os.path.join(self.inipath, 'docenv.ini')
        if os.path.exists(ini):
            self.config = configparser.ConfigParser()
            self.config.read(ini)
            return True
        else:
            print('docenv.ini is not found.')
            return False

    def check_TeXLive(self):
        try:
            subprocess.check_call('mktexlsr.exe --version')
            return True
        except OSError:
            print("Make sure TeX Live is included in PATH.")
            return False

    def create_parser(self):
        parser = argparse.ArgumentParser(
            description ='Configure your documentation environment for LaTeX.'
        )
        parser.add_argument(
            '-s',
            dest = 'store_to_local',
            action = 'store_true',
            default = False,
            help = 'Copy the provided latex class and style files into the local TEXMF directory.'
        )
        # parser.add_argument(
        #     '-H',
        #     dest = 'texmfhome',
        #     action = 'store_true',
        #     default = False,
        #     help = 'Set TEXMFHOME as an environment variable.'
        # )
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
            '-B',
            dest = 'batch',
            action = 'store_true',
            default = False,
            help = 'Get every option done at once.'
        )
        parser.add_argument(
            '-P',
            dest = 'confirmation',
            action = 'store_true',
            default = False,
            help = 'Proceed without asking for confirmation.'
        )
        return parser

    def confirm(self, msg):
        if self.confirmation_bool:
            answer = input(msg)
            return answer
        else:
            return self.answer

    def store_to_local(self):
        print('\n[Copying latex style files]')   
        try:
            latex_style = self.config.get('Sphinx Style', 'latex')
            texmf_local = self.config.get('TeX Live', 'texmflocal')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'These files are going to be copied into <%s>\n%s\nEnter [Y] to proceed, [n] to abandon, or another directory: ' %(texmf_local, latex_style.replace(', ', '\n'))
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        if not (answer.lower() == 'y' or answer == ''):
            texmf_local = answer
        files = latex_style.split(', ')
        for afile in files:        
            src = os.path.join(self.inipath, afile)
            if os.path.exists(src):
                cmd = 'copy %s %s' %(src, texmf_local) 
                os.system(cmd)
        cmd = 'dir %s' %(texmf_local)
        os.system(cmd)
        os.system('mktexlsr.exe')

    # def set_texmfhome(self):
    #     print('\n[Setting TEXMFHOME]')    
    #     try:
    #         texmfhome = self.config.get('TeX Live', 'TEXMFHOME')
    #     except:
    #         print('Make sure to have docenv.ini set properly.')
    #         return
    #     query = 'Are you sure to set the TEXMFHOME environment variable to  <%s>?\nEnter [Y] to proceed, [n] to abandon, or another path: ' %(texmfhome)
    #     answer = self.confirm(query)
    #     if answer.lower() == 'n':
    #         return
    #     if not (answer.lower() == 'y' or answer == ''):
    #         texmfhome = answer
    #     cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXMFHOME -value '%s'\"" % (texmfhome)
    #     os.system(cmd)
    #     cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXMFHOME'\""
    #     os.system(cmd)

    def set_texedit(self):
        print('\n[Setting TEXEDIT]')    
        try:    
            texedit = self.config.get('TeX Live', 'TEXEDIT')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'Are you sure to set the TEXEDIT environment variable to  <%s>?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(texedit)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        if not (answer.lower() == 'y' or answer == ''):
            texedit = answer
        cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXEDIT -value '%s'\"" % (texedit)
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
        query = 'Are you sure to use <%s> to enable the inverse search feature of SumatraPDF?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ' %(editor)
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
        query = "'%s' will be replaced with '%s' in <%s>\nEnter [Y] to proceed, [n] to abandon." %(target, substitute, texmf_cnf)
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
        query = "<%s> will be created to include %s\nEnter [Y] to proceed, [n] to abandon." %(local_conf, content)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        else:
            with open(local_conf, mode='w') as f:
                f.write(content)

    def update_texlive(self):
        print('\n[Updating TeX Live]')    
        try:
            repository = self.config.get('TeX Live', 'repository')
        except:
            print('Make sure to have docenv.ini set properly.')
            return
        query = 'Are you sure to use the <%s> repository to update the TeX Live?\nEnter [Y] to proceed, [n] to abandon, or another repository: ' %(repository)
        answer = self.confirm(query)
        if answer.lower() == 'n':
            return
        else:
            if not (answer.lower() == 'y' or answer == ''):
                repository = answer
            os.system('tlmgr.bat option repository %s' %(repository))
            os.system('tlmgr.bat update --self --all')

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
        if self.confirmation_bool:
            query = '\nDo you want to continue this batch configuration? [Y/n] '
            answer = self.confirm(query)
        else:
            answer = self.answer
        if answer.lower() == 'n':
            return False
        else:
            func()
            return True        

    def configure(self):
        if self.ini:
            if self.args.batch:
                if not self.ToContinue(self.store_to_local):
                    return None
                # if not self.ToContinue(self.set_texmfhome):
                #     return None
                if not self.ToContinue(self.modify_texmf_cnf):
                    return None
                if not self.ToContinue(self.create_local_conf):
                    return None
                if not self.ToContinue(self.set_texedit):
                    return None
                if not self.ToContinue(self.set_sumatrapdf):
                    return None
                if not self.ToContinue(self.update_texlive):
                    return None
                if not self.ToContinue(self.cache_font):
                    return None
                self.ToContinue(self.luaotfload)                
            else:    
                if self.args.store_to_local:
                    self.store_to_local()
                # if self.args.texmfhome:
                #     self.set_texmfhome()
                if self.args.texmf_cnf:
                    self.modify_texmf_cnf()
                if self.args.local_conf:
                    self.create_local_conf()
                if self.args.texedit:
                    self.set_texedit()
                if self.args.sumatrapdf:
                    self.set_sumatrapdf()
                if self.args.update_texlive:
                    self.update_texlive()
                if self.args.cache_font:
                    self.cache_font()
                if self.args.luaotfload:
                    self.luaotfload()

if __name__ == '__main__':
    texconf = TeXLiveConf()
    parser = texconf.create_parser()
    texconf.args = parser.parse_args()
    if texconf.args.confirmation:
        texconf.confirmation_bool = True
    texconf.configure()