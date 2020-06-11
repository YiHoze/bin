# loop.py "command foo_* goo_*"
# which processes command for each one seleted

import os
import sys
import glob
import argparse
import re

parser = argparse.ArgumentParser(
    description = 'A given command will be repeated with each one matching a wildcard expresson.'
)
parser.add_argument(
    'cmd',
    nargs = 1,
    help = 'Type a command with arguments.'
)
parser.add_argument(
    '-c',
    dest = 'check_bool',
    action = 'store_false',
    default = True,
    help = 'Do not check if files matching the wildcard expression exist.'
)
args = parser.parse_args()

# find the argument that contains '*'
cmd = args.cmd[0].split(' ')
for i in cmd:
    if i.count('*') > 0:
        selection = i
        break

cmd = ' '.join(cmd)
if args.check_bool:
    for i in glob.glob(selection):
        num = re.findall('\d+', i)
        if len(num) > 0:
            real_cmd = cmd.replace('*', num[0])
            os.system(real_cmd)
        else:
            print('No numbered files are found.')
            break
else:    
    for i in glob.glob(selection):
        real_cmd = cmd.replace(selection, i)
        os.system(real_cmd)
