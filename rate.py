import sys
# ExchangeReate()
import urllib.request
from bs4 import BeautifulSoup
import argparse
import re
import unicodedata
# TaxRate()
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family="Noto Sans CJK KR")

class ExchangeRate(object):

    def __init__(self, amount=1.0, currency='USD', list=False):

        self.amount = amount
        self.currency = currency
        self.list_bool = list
        
        URL = 'https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_USDKRW'
        page = urllib.request.urlopen(URL)
        self.soup = BeautifulSoup(page, 'html.parser')  

        # getting currencies from <select>
        lines = ''        
        for i in self.soup.find_all('option'):              
            lines = lines + str(i) + '\n'        
        p = re.compile('>(.+?)<')
        found = p.findall(lines)
        i = 0
        while i < len(found):
            found[i] = found[i].strip()
            i += 1
        found = set(found)
        self.currencies = {}
        for i in found:
            words = i.split()
            self.currencies[words[-1]] = i

    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'View exchage rates.'
        )
        parser.add_argument(
            'amount',
            nargs = '?',
            type = float,
            default = 1.0,
            help = 'Specify an amount.'
        )
        parser.add_argument(
            dest = 'currency',
            nargs = '?',
            default = 'USD',
            help = 'specify a currency. (default: USD) '
        )
        parser.add_argument(
            '-l',
            dest = 'list',
            action = 'store_true',
            default = False,
            help = 'Show the ist of currencies.'
        )        
        args = parser.parse_args()
        self.amount = args.amount
        self.currency = args.currency
        self.list_bool = args.list


    def align_string(self, string: str, width: int):

        nfc_string = unicodedata.normalize('NFC', string)        
        wide_chars = [unicodedata.east_asian_width(c) for c in nfc_string]
        num_wide_chars = sum(map(wide_chars.count, ['W', 'F']))        
        width = max(width - num_wide_chars, num_wide_chars)
        return '{:{w}}'.format(nfc_string, w=width)     


    def show_currencies(self, columns=2):

        currencies = sorted(self.currencies.keys()) 
        cur_countries = []
        for i in currencies:
            country = self.currencies[i]
            # Removing 'CNY' from '중국 위안 CNY'
            country = country.rsplit(' ', 1)[0]            
            country = self.align_string(country, 25) 
            cur_countries.append('{0}: {1}'.format(i, country))
        cnt = 0
        line = ''
        for i in cur_countries:
            line += i
            cnt += 1
            if cnt == columns:
                print(line)
                line = ''
                cnt = 0
        if line != '':
            print(line)


    def calcurate(self):

        self.currency = self.currency.upper()
        try:
            exchange_rate = self.soup.find('option', text=self.currencies[self.currency]).attrs['value']
        except:
            print('Make sure the currency abbreviation is correct.')
            return
        basis = self.soup.find('option', text=self.currencies[self.currency]).attrs['label']
        
        # foreign : KRW for the basis
        exchange_rate = float(exchange_rate)
        basis = float(basis)
        won = basis * exchange_rate
        won = '{:,.2f}'.format(won)
        basis = '{:,.2f}'.format(basis)
        print('%s %s = %s KRW' %(basis, self.currency, won))
        
        # foreign : KRW for the given
        won_amount = self.amount * exchange_rate
        foreign_amount = self.amount
        won_amount = '{:,.2f}'.format(won_amount)
        foreign_amount = '{:,.2f}'.format(foreign_amount)
        print('%s %s = %s KRW' %(foreign_amount, self.currency, won_amount))
        
        # KRW : foreign for the given
        won_amount = self.amount
        foreign_amount = self.amount / exchange_rate
        won_amount = '{:,.2f}'.format(won_amount)
        foreign_amount = '{:,.2f}'.format(foreign_amount)
        print('%s KRW = %s %s' %(won_amount, foreign_amount, self.currency))


class ElectricityRate(object):

    def __init__(self, power=0, summer=False):

        self.power = power
        self.summer_bool = summer

        # 부가세
        self.tax_rate = 0.1
        # 전력 기금
        self.endowment_rate = 0.037
        

    def determine_rate(self):

        self.accumulated_sections = {} 

        if self.summer_bool:
            self.range_interval = 150
            # 구간
            self.rate_ranges = [300, 450, 451]
            # 기본 요금
            self.base_sections = { 300:910, 450:1600, 451:7300 }
            # 전력량 요금
            self.rate_sections = { 300:93.3, 450:187.9, 451:280.6 }
        else:
            self.range_interval = 200
            self.rate_ranges = [200, 400, 401]
            self.base_sections = { 200:910, 400:1600, 401:7300 }
            self.rate_sections = { 200:93.3, 400:187.9, 401:280.6 }

        preceding = 0
        difference = 0
        accumulation = 0
        for i in range( len(self.rate_ranges)-1 ):
            limit = self.rate_ranges[i]            
            difference = limit - preceding
            preceding = limit
            accumulation += difference * self.rate_sections[limit]             
            self.accumulated_sections[limit] = accumulation


    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'Electricity charge calculator'
        )

        parser.add_argument(
            'power',
            nargs = '+',
            type = int,
            help = 'Specify an amount of electrical power.'
        )
        parser.add_argument(
            '-s',
            dest = 'summer',
            action = 'store_true',
            default = False,
            help = 'Apply the summer rate.'
        )

        args = parser.parse_args()
        self.power = args.power
        self.summer_bool = args.summer
        self.determine_rate()


    def calculate(self):
        
        section = 0
        remainder = 0
        bottom = self.rate_ranges[0]
        top = self.rate_ranges[-1]

        for power in self.power:            
            if power <= bottom:
                result = power * self.rate_sections[bottom]
                result += self.base_sections[bottom]
            else:
                section = power//self.range_interval * self.range_interval
                if section >= top:
                    section = self.rate_ranges[-2]
                remainder = power - section
                result = self.accumulated_sections[section]
                
                section += self.range_interval
                if section >= top:
                    section = self.rate_ranges[-2]
                result += remainder * self.rate_sections[section] 
                result += self.base_sections[section]

            result = int(result) + round(result * self.tax_rate) + int(result * self.endowment_rate / 10)*10
            result = int(result/10) * 10
            print('{} kWh: ₩{:,}'.format(power, result))


class TaxRate(object):
    
    def __init__(self, salary=0, show=False, plot=False):

        self.salary = salary
        self.show_bool = show
        self.plot_bool = plot

        # 1200만 원 초과 ~ 4600만 원 이하: 15%
        # self.rate_sections = OrderedDict({1200:6, 4600:15, 8800:24, 15000:35, 30000:38, 50000:40, 50001:42})
        # to be compatible with WinPython
        self.rate_sections = {1200:6, 4600:15, 8800:24, 15000:35, 30000:38, 50000:40, 50001:42}
        self.rate_sections = OrderedDict(sorted(self.rate_sections.items()))
        self.accumulated_sections = {} 
        self.initialize()


    def initialize(self):

        accumulated = 0
        preceding = 0
        for limit in self.rate_sections:
            if preceding == 0:
                self.accumulated_sections[limit] = 0
            else:        
                self.accumulated_sections[limit] = int(accumulated)
            rate = self.rate_sections[limit]
            accumulated = accumulated + ((limit - preceding) * rate/100)
            preceding = limit


    def parse_args(self):

        parser = argparse.ArgumentParser(
            description = 'Calculate income tax.'
        )
        parser.add_argument(
            'salary',
            nargs = '?',
            type = int,
            default = 0,
            help = 'Specify an amount of salary in unit of 10,000.'
        )
        parser.add_argument(
            '-s',
            dest = 'show',
            action = 'store_true',
            default = False,
            help = 'Dispay rate sections by income.'
        )
        parser.add_argument(
            '-p',
            dest = 'plot',
            action = 'store_true',
            default = False,
            help = 'Draw a bar plot for rate sections.'
        )
        args = parser.parse_args()
        self.salary = args.salary
        self.show_bool = args.show
        self.plot_bool = args.plot


    def rate_section_show(self):

        if self.show_bool is True:
            self.rate_section_itemize()
        if self.plot_bool is True:
            self.rate_section_draw()


    def rate_section_itemize(self):

        for limit in self.rate_sections:
            if limit == 50001:
                salary = '{:,}'.format(preceding)
                print(" Over %6s: %2d %%" %(salary, self.rate_sections[limit]))
            else:
                salary = '{:,}'.format(limit)
                print("Up to %6s: %d %%" %(salary, self.rate_sections[limit]))
                preceding = limit    


    def rate_section_draw(self):

        sections, rates = [], []
        for limit in self.rate_sections:
            if limit == 50001:
                salary = '>'+'{:,}'.format(preceding)
                sections.append(salary)
            else:
                salary = '≤'+'{:,}'.format(limit)
                sections.append(salary)
                preceding = limit
            rates.append(self.rate_sections[limit])
        x = np.arange(len(self.rate_sections))
        plt.bar(x,rates)
        plt.xticks(x, sections)    
        plt.xlabel('연봉(만 원)')
        plt.ylabel('세율(%)')
        plt.title('소득세')
        plt.show()


    def calculate_tax(self, salary):

        corresponding = 0
        for limit in self.rate_sections:
            if salary > limit:
                if limit == 50001:
                    preceding = corresponding
                corresponding = limit
            else:
                preceding = corresponding
                corresponding = limit
                break
        accumulated = self.accumulated_sections[corresponding]
        rate = self.rate_sections[corresponding]
        tax = accumulated + ((salary - preceding) * rate/100)
        return tax


    def display_pay(self, salary):

        tax = self.calculate_tax(salary)
        actual_rate = tax * 100 / salary
        monthly_pay = salary/12
        monthly_tax = monthly_pay * actual_rate / 100
        post_tax_pay = monthly_pay - monthly_tax    
        
        output = '''Salary: {}
Tax: {}
Actual tax rate: {:.2f}%
Monthly pay: {:.1f}
Monthly tax: {:.1f}
Post-tax pay: {:.1f}
            '''.format(salary, tax, actual_rate, monthly_pay, monthly_tax, post_tax_pay)
        print(output)
        self.rate_section_show()


def call_exchange_rate():

    exrate = ExchangeRate()
    exrate.parse_args()
    if exrate.list_bool:
        exrate.show_currencies()
    else:
        exrate.calcurate()


def call_electricity_rate():

    eRate = ElectricityRate()
    eRate.parse_args()
    eRate.calculate()


def call_tax_rate():

    taxrate = TaxRate()
    taxrate.parse_args()
    if taxrate.salary == 0:
        if taxrate.show_bool or taxrate.plot_bool:
            taxrate.rate_section_show()
    else:
        taxrate.display_pay(taxrate.salary)


def help():
    output = '''Available functions are:
rate.py [exchange] 
rate.py elec 
rate.py tax 
'''
    print(output)


if __name__=="__main__":
    # print(sys.argv)
    if len(sys.argv) > 1:
        choice = sys.argv[1].lower()
        del sys.argv[1]
        if choice == 'exchange':
            call_exchange_rate()
        elif choice == 'tax':
            call_tax_rate()
        elif choice == 'elec':
            call_electricity_rate()
        else:
            help()
    else:    
        call_exchange_rate()