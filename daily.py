# [Chrome]
# app = C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
# target =     
#     http://dic.daum.net/index.do?dic=eng 
#     http://www.ktug.org

import os
import sys
import argparse
import configparser
import subprocess 

class DailyBusiness(object):
    def __init__(self, list='daily.ini'):
        self.list = list
        dirCalled = os.path.dirname(__file__)
        self.list = os.path.join(dirCalled, self.list)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = 'Open apps and their targets specified in daily.ini.'
        )
        parser.add_argument(
            'list',
            nargs = '?',
            help = 'Specify another daily to-do list.'
        )
        args = parser.parse_args()
        if args.list is not None:
            self.list = args.list

    def enumerate_tasks(self):
        if os.path.exists(self.list):
            config = configparser.ConfigParser()
            config.read([self.list], encoding='utf-8')
            for section in config.sections():
                app = config.get(section, 'app')
                try: 
                    target = config.get(section, 'target')
                except:
                    target = ''
                cmd = '\"%s\" %s' %(app, target.replace('\n', ' '))
                subprocess.Popen(cmd)        
        else:
            print('%s is not found.' %(self.list))

if __name__ == '__main__':
    daily = DailyBusiness()
    daily.parse_args()
    daily.enumerate_tasks()