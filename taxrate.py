import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family="HCR Dotum")

parser = argparse.ArgumentParser(
    description = 'Calculate income tax.'
)
parser.add_argument(
    'salary',
    nargs = '?',
    type = int,
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

# 1200만 원 초과 ~ 4600만 원 이하: 15%
rate_sections = {1200:6, 4600:15, 8800:24, 15000:35, 30000:38, 50000:40, 0:42}
accumulated_sections = {} 

def initialize():
    accumulated = 0
    preceding = 0
    for limit in rate_sections:
        if preceding == 0:
            accumulated_sections[limit] = 0
        else:        
            accumulated_sections[limit] = int(accumulated)
        rate = rate_sections[limit]
        accumulated = accumulated + ((limit - preceding) * rate/100)
        preceding = limit
    # print(accumulated_sections)

def rate_section_show():
    if args.show is True:
        rate_section_itemize()
    if args.plot is True:
        rate_section_draw()

def rate_section_itemize():
    for limit in rate_sections:
        if limit == 0:
            salary = '{:,}'.format(preceding)
            print(" Over %6s: %2d %%" %(salary, rate_sections[limit]))
        else:
            salary = '{:,}'.format(limit)
            print("Up to %6s: %d %%" %(salary, rate_sections[limit]))
            preceding = limit    

def rate_section_draw():
    sections, rates = [], []
    for limit in rate_sections:
        if limit == 0:
            salary = '>'+'{:,}'.format(preceding)
            sections.append(salary)
        else:
            salary = '≤'+'{:,}'.format(limit)
            sections.append(salary)
            preceding = limit
        rates.append(rate_sections[limit])
    x = np.arange(len(rate_sections))
    plt.bar(x,rates)
    plt.xticks(x, sections)    
    plt.xlabel('연봉(만 원)')
    plt.ylabel('세율(%)')
    plt.title('소득세')
    plt.show()

def calculate_tax(salary):
    corresponding = 0
    for limit in rate_sections:
        if salary > limit:
            if limit == 0:
                preceding = corresponding
            corresponding = limit
        else:
            preceding = corresponding
            corresponding = limit
            break
    accumulated = accumulated_sections[corresponding]
    rate = rate_sections[corresponding]
    # print(accumulated_sections)
    # print(accumulated, preceding, corresponding)
    tax = accumulated + ((salary - preceding) * rate/100)
    return tax

def display_pay(salary):
    tax = calculate_tax(salary)
    actual_rate = tax * 100 / salary
    monthly_pay = salary/12
    monthly_tax = monthly_pay * actual_rate/100
    post_tax_pay = monthly_pay - monthly_tax    
    output = """
    salary: %d
    Actual tax rate: %.2f%%
    Tax: %d
    Monthly pay: %.1f
    Monthly tax: %.1f
    Post-tax pay: %.1f
    """ %(salary, actual_rate, tax, monthly_pay, monthly_tax, post_tax_pay)
    print(output)
    rate_section_show()

if __name__=="__main__":
    args = parser.parse_args()
    initialize()    
    if args.salary is None:
        if args.show or args.plot:
            rate_section_show()
        else:
            parser.print_help()
    else:
        display_pay(args.salary)
else:
    initialize()