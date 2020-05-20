import math
import argparse

class ConvertUnit(object):

    def __init__(self, numeral=0, unit_type=None, until=None):
        self.numeral = numeral
        self.unit_type = unit_type
        self.until = until
        self.units = {
            'acre': ['acres', 'square meters', 4046.86],
            'degree': ['°', '%', 'self.gradient'],
            'fahrenheit': ['Fahrenheit', 'Celsius', 'self.temperature'],
            'foot': ['feet', 'meters', 0.3048],
            'inch': ['inches', 'centimeters', 2.54],
            'mile': ['miles', 'kilometers', 1.609344],
            'point': ['points', 'millimeters', 0.352778],
            'pound': ['pounds', 'kilograms', 0.453592],
            'pyeong': ['pyeongs', 'square meters', 3.305785],
            'yard': ['yards', 'meters', 0.9144],
            'knot': ['knots', 'km/h', 1.852]

        }
        self.unit_types = []
        for i in self.units.keys():
            self.unit_types.append(i)
        self.unit_types = sorted(self.unit_types)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description='Convert a unit of measurement to another.'
        )
        parser.add_argument(
            'numeral',
            nargs='*',
            help='Enter a numeric value with the full word or the first some letters of a unit type. \
                "unit.py 10 mi 20" performs converting calculations from 10 to 20 miles in kilometer.'
        )
        args = parser.parse_args()
        if len(args.numeral) < 2:
            print('Specify a unit type:')
            self.show_unit_list()
        else:
            self.numeral = float(args.numeral[0])
            self.unit_type = args.numeral[1]
            try:
                self.until = float(args.numeral[2])
            except:
                self.until = None
            unit.convert()

    def show_unit_list(self):
        print(', '.join(self.unit_types))

    def verify_unit(self):
        if self.unit_type in self.unit_types:
            return True
        else:
            for i in self.unit_types:
                if self.unit_type in i:
                    self.unit_type = i
                    return True
            print('%s is an unknown unit' % (self.unit_type))
            return False

    def gradient(self, numeral=0):
        degree = math.degrees(math.atan(numeral/100))
        percent = math.tan(math.radians(numeral)) * 100
        return degree, percent

    def temperature(self, numeral=0):
        fahrenheit = numeral * 9 / 5 + 32
        celsius = (numeral - 32) * 5 / 9
        return fahrenheit, celsius

    def convert(self):
        if not self.verify_unit():
            return False
        self.nonmetric_unit = self.units[self.unit_type][0]
        self.metric_unit = self.units[self.unit_type][1]
        self.coefficient = self.units[self.unit_type][2]
        if type(self.coefficient) is float:
            self.coefficient_bool = True
        else:
            self.coefficient_bool = False
        if self.until is not None:
            self.convert_until(self.numeral, self.until)
        else:
            self.convert_calculate(self.numeral)

    def convert_until(self, lower, upper):
        if lower > upper:
            print('Specify a higher value for the upper limit.')
            return
        while lower <= upper:
            self.convert_calculate(lower)
            lower += 1

    def convert_calculate(self, numeral):
        if self.coefficient_bool is True:
            nonmetric_coefficient = 1 / self.coefficient
            nonmetric_value = numeral * nonmetric_coefficient
            metric_value = numeral * self.coefficient
        else:
            func = self.coefficient + '(' + str(numeral) + ')'
            nonmetric_value, metric_value = eval(func)
        print('%6.2f %s = %6.2f %s \t %6.2f %s = %6.2f %s' % (
            numeral, self.nonmetric_unit, metric_value, self.metric_unit, numeral, 
            self.metric_unit, nonmetric_value, self.nonmetric_unit))

if __name__ == '__main__':
    unit = ConvertUnit()
    unit.parse_args()
