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
        example = '''examples:
        unit.py 10 mi 20
            10 to 20 miles are converted to kilometers
        unit.py -c 0000FF
            This RGB value is converted to CMYK
        unit.py -c 240,120,99
            This RGB value is converted to CMYK
        unit.py -c 0.1,0.33,0.01
            This CMYK value is converted to RGB
        '''
        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description='Convert a unit of measurement to another.'
        )
        parser.add_argument(
            'numeral',
            nargs='*',
            help='Enter a numeric value with the full word or the first some letters of a unit type.'                
        )
        parser.add_argument(
            '-c',
            dest = 'color_bool',
            action = 'store_true',
            default = False,
            help = 'With this option, specify one or more RGB or CMYK values to convert between them.'
        )
        args = parser.parse_args()
        if args.color_bool:
            ColorModel(args.numeral)
        else:
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

class ColorModel(object):

    def __init__(self, color=None):
        self.color = color
        for i in self.color:    
            self.identify_color_model(i)     

    def error_message(self):
        print('The value is formatted wrong.')        

    def identify_color_model(self, color: str):   
        color = color.replace(' ', '')
        if color.count(',') >= 3:
            C, M, Y, K = self.parse_CMYK(color)
            if C is False:
                self.error_message()
            else:
                # check if between 0 and 1
                if not all(map(lambda x: x >= 0. and x <= 1., [C, M, Y, K])):
                    self.error_message()
                else:
                    self.CMYK_to_RGB(color, C, M, Y, K)
        else:
            R, G, B = self.parse_RGB(color)
            if R is False:
                self.error_message()
            else:
                # check if between 0 and 255
                if not all(map(lambda x: x in range(256), [R, G, B])):
                    self.error_message()
                else:
                    self.RGB_to_CMYK(color, R, G, B)

    def parse_CMYK(self, color: str):        
        color = color.split(',')
        if len(color) == 4:            
            try:
                C = float(color[0])
                M = float(color[1])
                Y = float(color[2])
                K = float(color[3])                
            except:
                C, M, Y, K = False, False, False, False
        else:
            C, M, Y, K = False, False, False, False

        return C, M, Y, K


    def parse_RGB(self, color: str):
        if color.count(',') == 0:        
            if len(color) == 6:
                try:
                    R = int(color[0:2], 16)
                    G = int(color[2:4], 16)
                    B = int(color[4:6], 16)
                except:
                    R, G, B = False, False, False

        if color.count(',') == 2: 
            color = color.split(',')
            try:
                R = int(color[0])
                G = int(color[1])
                B = int(color[2])
            except:
                R, G, B = False, False, False
            
        return R, G, B

    def RGB_to_CMYK(self, color, R, G, B):       
        R = R/255
        G = G/255
        B = B/255
        K = 1 - max(R, G, B)
        C = (1 - R - K) / (1 - K)
        M = (1 - G - K) / (1 - K)
        Y = (1 - B - K) / (1 - K)
        color = color.replace(',', ', ')
        CMYK = '{} = {:1.2f}, {:1.2f}, {:1.2f}, {:1.2f}'.format(color, C, M, Y, K)
        print(CMYK)

    def CMYK_to_RGB(self, color, C, M, Y, K):
        R = 255 * (1 - C) * (1 - K) 
        G = 255 * (1 - M) * (1 - K)
        B = 255 * (1 - Y) * (1 - K)
        color = color.replace(',', ', ')
        RGB = '{} = {:3.0f}, {:3.0f}, {:3.0f}'.format(color, R, G, B)
        print(RGB)

if __name__ == '__main__':
    unit = ConvertUnit()
    unit.parse_args()
