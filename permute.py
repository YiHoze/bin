# How to download nltk packages:
# >>> import nltk
# >>> nltk.download()
# Then the NLTKDownloader window appears.
# Click the All Packages tab, scroll down to the wordnet item, and then click the Download button
# Scroll down to the words item, and click the Download button

import os
import sys
import argparse
from nltk.corpus import wordnet
# from nltk.corpus import words 
from itertools import permutations

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from mytex import LatexTemplate

class PermuteLetters(object):

    def __init__(self, letters=None, wordnet=False, number=False, pdf=False):
        self.letters = letters
        self.number_bool = number
        self.wordnet_bool = wordnet
        self.pdf_bool = pdf

    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'Permute letters.'
        )
        parser.add_argument(
            'letters',
            type = str,
            nargs = 1,
            help = 'Type letters without space.'
        )
        parser.add_argument(
            '-n',
            dest = 'number',
            action = 'store_true',
            default = False,
            help = 'Show results with number.'
        )
        parser.add_argument(
            '-w',
            dest = 'wordnet',
            action = 'store_true',
            default = False,
            help = 'Show only ones close to word. Note that it takes a rather long time.'
        )
        parser.add_argument(
            '-p',
            dest = 'pdf',
            action = 'store_true',
            default = False,
            help = 'Print in PDF using XeLaTeX.'
        )
        args = parser.parse_args()
        self.letters = args.letters
        self.number_bool = args.number
        self.wordnet_bool = args.wordnet
        self.pdf_bool = args.pdf
        # letters = list(args.letters[0])

    def permute(self):
        letters = list(self.letters[0])
        perms = list(permutations(letters))
        for index, value in enumerate(perms):
            perms[index] = ''.join(value)
        perms = set(sorted(perms))
        if self.wordnet_bool:
            picked = []
            for i in perms:
                # if i in words.words():
                if wordnet.synsets(i):
                    picked.append(i)
            perms = picked
        self.display(perms)

    def display(self, perms):        
        if self.number_bool:
            digits = len(perms)
            digits = len(str(digits))
            for index, value in enumerate(perms):
                print('{0:{d}}: {1}'.format(index+1, value, d=digits))
        else:
            print(', '.join(perms))

    def generate_pdf(self):
        mytex = LatexTemplate(template='permute', substitutes=self.letters)
        if mytex.ini_bool:
            mytex.make()
    

if __name__ == '__main__':
    pl = PermuteLetters()
    pl.parse_args()
    if pl.pdf_bool:
        pl.generate_pdf()
    else:
        pl.permute()

    