# loop.py command foo_* goo_*
# which processes command for each one seleted

import os
import sys
import glob
import re

args = len(sys.argv)

# find the arguments that contains '*'
index = 1
while index < args:
    if sys.argv[index].count('*') > 0:        
        selection = sys.argv[index]
        break
    index += 1

# combine arguments to compose a command    
cmd = ''
index = 1
while index < args:
    cmd = cmd + ' ' + sys.argv[index]
    index += 1

# replace '*' with real numbers
for i in glob.glob(selection):
    num = re.findall('\d+', i)
    if len(num) > 0:
        real_cmd = cmd.replace('*', num[0])
        os.system(real_cmd)
    else:
        print('No numbered files are found.')
        break