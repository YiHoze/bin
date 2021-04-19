import os
import sys
import glob
import argparse
import configparser


dirCalled = os.path.dirname(__file__)

class ExamManager(object):

    def __init__(self, argv=None):

        self.dbFile = os.path.join(dirCalled, 'exam.db')
        if os.path.exists(self.dbFile)
            self.database = configparser.ConfigParser()
            self.database.read(self.dbFile, encoding='utf-8')
        else:
            print('{} is not found.'.format(self.dbFile))
            sys.exit()

        self.parse_args(argv)

        if self.insert_bool:
            self.insert_new()


    def parse_args(self, argv=None):

        parser = argparse.ArgumentParser(
            description = 'Manage the examination database.'
        )
        parser.add_argument(
            'sections'
            nargs = '+',
            help = 'Specify one or more sections or files.'
        )
        parser.add_argument(
            '-l',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate sections.'
        )
        parser.add_argument(
            '-i',
            dest = 'insert_bool',
            action = 'store_true',
            default = False,
            help = "Insert new TeX files into the database file. Stems of filenames are used as section labels in the database."
        )
        parser.add_argument(
            '-u',
            dest = 'update_bool',
            action = 'store_true',
            default = False,
            help = 'Update the dabase with the files whose names are the same as specified.'
        )
        parser.add_argument(
            '-r',
            dest = 'remove_bool',
            action = 'store_true',
            default = False,
            help = 'Remove the section from the database.'
        )
        parser.add_argument(
            '-a',
            dest = 'assemble_bool',
            action = 'store_true',
            default = False,
            help = 'Assemble sections to build a document.'
        )

        self.args = parser.parse_args(argv)


    # def run_recursive(self, func):



    def if_exits(self, filename):

        if os.path.exists(filename):
            return True
        else:
            print('"{}" does not exist in the current directory.'.format(filename))
            return False


    def escape_content(self, filename, content):

    def insert_new(self):

        for i in self.args.sections:
            for filepath in glob.glob(i):
                section = os.path.splitext(os.path.basename(filepath))[0]
                if section in self.database.sections():
                    print('"{}" is already included in the database.'.format(section))
                else:
                    with open(filename, )
                    self.database.add_section(section)
                    self.database.set








if __name__ == '__main__':
    ExamManager()
