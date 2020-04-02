# How to download nltk packages:
# >>> import nltk
# >>> nltk.download()
# Then the NLTKDownloader window appears.
# Click the All Packages tab, scroll down to the wordnet item, and then click the Download button
# Scroll down to the words item, and click the Download button

import os
import sys
import argparse
from random import randint
from itertools import permutations
# from itertools import combinations
from nltk.corpus import wordnet
# from nltk.corpus import words 

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from mytex import LatexTemplate

class Lotto(object):

    def __init__(self, 
    letters=None, wordnet=False, number=False, frequency=5, pdf=False, weeks=8):
        self.letters = letters
        self.number_bool = number
        self.wordnet_bool = wordnet
        self.frequency = frequency
        self.pdf_bool = pdf
        self.weeks = weeks

    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'Pick lotto numbers or permute letters.'
        )
        parser.add_argument(
            'letters',
            type = str,
            nargs = '?',
            help = 'Type letters without space for permutation or nothing for lotto.'
        )
        parser.add_argument(
            '-n',
            dest = 'number',
            action = 'store_true',
            default = False,
            help = 'Show results with number.'
        )
        parser.add_argument(
            '-W',
            dest = 'wordnet',
            action = 'store_true',
            default = False,
            help = 'Show only ones close to word. Note that it takes a rather long time.'
        )
        parser.add_argument(
            '-f',
            dest = 'frequency',
            type = int,
            default = 5,
            help = 'Specify how many times to pick numbers for lotto. (default: 5)'
        )
        parser.add_argument(
            '-p',
            dest = 'pdf',
            action = 'store_true',
            default = False,
            help = 'Print in PDF using XeLaTeX.'
        )
        parser.add_argument(
            '-w',
            dest = 'weeks',
            default = '8',
            help = 'Specify how many weeks to print for lotto. (default: 8)'
        )
        args = parser.parse_args()
        self.letters = args.letters
        self.number_bool = args.number
        self.wordnet_bool = args.wordnet
        self.frequency = args.frequency
        self.pdf_bool = args.pdf
        self.weeks = args.weeks
        

    def run(self):
        if self.letters is None:
            self.run_lotto()
        else:
            self.run_permutations()

    def run_lotto(self):
        m, n = 6, 45
        balls = []
        cnt = 0
        while cnt < self.frequency:
            balls.clear()
            for i in range(n-m+1, n+1):
                drawn = randint(1, i) 
                if drawn in balls:
                    balls.append(i)
                else:
                    balls.append(drawn)
            balls.sort()            
            for index, value in enumerate(balls):
                balls[index] = '{:>2}'.format(str(value))
            print(', '.join(balls))            
            cnt += 1

    def run_permutations(self):
        letters = list(self.letters)
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
        self.permutations_display(perms)

    def permutations_display(self, perms):        
        if self.number_bool:
            digits = len(perms)
            digits = len(str(digits))
            for index, value in enumerate(perms):
                print('{0:{d}}: {1}'.format(index+1, value, d=digits))
        else:
            print(', '.join(perms))

    def generate_pdf(self):
        if self.letters is None:
            mytex = LatexTemplate(template='lotto', substitutes=[self.weeks, str(self.frequency)])
        else:
            mytex = LatexTemplate(template='permute', substitutes=[self.letters])
        if mytex.ini_bool:
            mytex.make()    

if __name__ == '__main__':
    lotto = Lotto()
    lotto.parse_args()
    if lotto.pdf_bool:
        lotto.generate_pdf()
    else:
        lotto.run()

# def permute(a, k=0):    
#     global num
#     global row
#     if k == len(a):
#         show(a)        
#     else:        
#         for i in range(k, len(a)):            
#             a[k], a[i] = a[i] ,a[k]
#             permute(a, k+1)
#             a[k], a[i] = a[i], a[k]

# def heap(a):
#     n = len(a)
#     idx = []
#     for i in range(n):
#         idx.append(0)
#     show(a)
#     i = 0
#     while i < n:
#         if idx[i] < i:
#             if (i % 2) == 0:
#                 a[0], a[i] = a[i], a[0]
#             else:
#                 a[idx[i]], a[i] = a[i], a[idx[i]]
#             show(a)
#             idx[i] = idx[i] + 1
#             i = 0
#         else:
#             idx[i] = 0
#             i = i + 1