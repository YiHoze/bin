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
from itertools import combinations
from nltk.corpus import wordnet
# from nltk.corpus import words 

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
from mytex import LatexTemplate

class Lotto(object):

    def __init__(self, 
    letters=None, combination=None, wordnet=False, number=False, frequency=5, pdf=False, weeks=8):
        self.letters = letters
        self.combination = combination
        self.number_bool = number
        self.wordnet_bool = wordnet
        self.frequency = frequency
        self.pdf_bool = pdf
        self.weeks = weeks

    def parse_args(self):

        example = '''examples:
    lotto.py -f 10 -p -w 20
        Lotto numbers are picked at random.
        With "-f 10", 10 set of lotto numbers are presented.
        With "-p", lotto numbers are printed in PDF. This requires TeX Live.            
        With "-w 20", lotto numbers are presented for coming 20 weeks.
        This is available only with "-p".
    lotto.py -c 3-4 -W -n 12ab가나
        These characters are permuted.
        With "-c 3-4", characters are selected within the specified range 
            and each set is permuted.
        With "-c 2", characters are selected from the specified number 
            up to the length of the given characters.
        With "-W", only meaningful words among the results are displayed.
    lotto.py -n [...]
        Each result is numbered.
    '''

        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Pick lotto numbers or permute letters.'
        )
        parser.add_argument(
            'letters',
            type = str,
            nargs = '?',
            help = 'Type characters without space for permutation or nothing for lotto.'
        )
        parser.add_argument(
            '-c',
            dest = 'combination',   
            default = None,
            help = 'Specify a range of combination.'
        )        
        parser.add_argument(
            '-n',
            dest = 'number',
            action = 'store_true',
            default = False,
            help = 'Show results with numbers.'
        )
        parser.add_argument(
            '-W',
            dest = 'wordnet',
            action = 'store_true',
            default = False,
            help = 'Show only meaningful words. Note that it takes a rather long time.'
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
            help = 'Print lotto numbers in PDF using XeLaTeX.'
        )
        parser.add_argument(
            '-w',
            dest = 'weeks',
            default = '8',
            help = 'Specify how many weeks to print for lotto. (default: 8)'
        )
        args = parser.parse_args()
        self.letters = args.letters
        self.combination = args.combination
        self.number_bool = args.number
        self.wordnet_bool = args.wordnet
        self.frequency = args.frequency
        self.pdf_bool = args.pdf
        self.weeks = args.weeks        

    def determine_task(self):
        if self.letters is None:
            self.run_lotto()
        # permutation or combination
        else:
            self.letters = self.letters.upper()
            # check combination range
            if self.combination is not None:     
                cnt = self.combination 
                cnt = self.combination.split('-')
                try:
                    if len(cnt) == 1:
                        start = int(cnt[0])                
                        end = len(self.letters)
                    elif len(cnt) == 2:
                        start = int(cnt[0])
                        end = int(cnt[1])
                except:
                    print('Wrong combination range')
                    return False           
                if start > end:
                    start = end
                if start < 2:
                    start = 2
                if end > len(self.letters):
                    end = len(self.letters)
                self.display_results(self.run_combinations(self.letters, start, end))                
            else:
                self.display_results(self.run_permutations(self.letters))

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
            cnt += 1
            result = ', '.join(balls)
            if self.number_bool:
                print('{:2d}: {}'.format(cnt, result))
            else:
                print(result)

    def run_combinations(self, letters, start, end):
        letters = list(letters)               
        perms = []
        while start <= end:
            combs = combinations(letters, start)
            for i in list(combs):
                perms.extend(self.run_permutations(''.join(i)))
            start += 1
        return perms

    def run_permutations(self, letters):
        # num is just passed from run_combinations() to display_results() 
        # to display the number of picked letters.
        letters = list(letters)
        return list(permutations(letters))        

    def display_results(self, results):
        # join letters to a word in each item
        for index, value in enumerate(results):
            results[index] = ''.join(value)
        # remove duplicates
        results = set(results)
        # check if items are meaningful words
        if self.wordnet_bool:
            picked = []
            for i in results:
                # if i in words.words():
                if wordnet.synsets(i):
                    picked.append(i)
            results = picked        
        # add numbers to display
        results = sorted(results)
        if self.number_bool:
            digits = len(results)
            digits = len(str(digits))
            if self.combination is not None:
                results = sorted(results, key=len)
                for index, value in enumerate(results):
                    print('{}.{:{d}}: {}'.format(len(value), index+1, value, d=digits))
            else:
                for index, value in enumerate(results):
                    print('{:{d}}: {}'.format(index+1, value, d=digits))
        else:
            if self.combination is not None:
                # sort by the length of elements
                results = sorted(results, key=len)
                letters = len(results[0])
                comb = []
                for i in results:
                    # gather words that have the same length
                    if letters == len(i):
                        comb.extend([i])
                    else:    
                        comb = sorted(comb)                    
                        print('{} letters: {}'.format(letters, ', '.join(comb)))
                        letters = len(i)
                        comb = [i] 
                print('{} letters: {}'.format(letters, ', '.join(comb)))
            else:                
                print(', '.join(results))

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
        lotto.determine_task()

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