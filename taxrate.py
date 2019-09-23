import argparse

parser = argparse.ArgumentParser(
    description = 'calculate income tax.'
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
# args = parser.parse_args()

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

def rate_section_show():
    for limit in rate_sections:
        print("Up to %6d: %2d%%" %(limit, rate_sections[limit]))

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
    tax = int(accumulated + ((salary - preceding) * rate/100))
    return tax

def display_pay(salary):
    tax = calculate_tax(salary)
    actual_rate = int(tax * 100 /salary)
    monthly_pay = int(salary/12)
    monthly_tax = int(monthly_pay * actual_rate/100)
    post_tax_pay = monthly_pay - monthly_tax    
    output = """
    salary: %d
    Actual tax rate: %d%%
    Tax: %d
    Monthly pay: %d
    Monthly tax: %d
    Post-tax pay: %d
    """ %(salary, actual_rate, tax, monthly_pay, monthly_tax, post_tax_pay)
    print(output)

if __name__=="__main__":
    args = parser.parse_args()
    initialize()
    if args.show:
        rate_section_show()
    elif args.salary is None:
        parser.print_help()
    else:
        display_pay(args.salary)
else:
    initialize()