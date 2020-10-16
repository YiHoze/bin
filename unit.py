import math
import argparse

class ConvertUnit(object):

    def __init__(self, numeral=0, unit_type=None, until=None):
        self.numeral = numeral
        self.unit_type = unit_type
        self.until = until
        self.units = {
            'acre': ['acres', 'm²', 4046.86],
            'degree': ['°', '%', 'self.gradient'],
            'fahrenheit': ['F°', 'C°', 'self.temperature'],
            'foot': ['feet', 'm', 0.3048],
            'inch': ['inches', 'cm', 2.54],
            'mile': ['miles', 'km', 1.609344],
            'point': ['points', 'mm', 0.352778],
            'pound': ['pounds', 'kg', 0.453592],
            'pyeong': ['pyeongs', 'm²', 3.305785],
            'yard': ['yards', 'm', 0.9144],
            'knot': ['knots', 'km/h', 1.852],
            'pascal': ['kg/cm²', 'Pa', 98066.5]
        }
        self.unit_types = []
        for i in self.units.keys():
            self.unit_types.append(i)
        self.unit_types = sorted(self.unit_types)

    def parse_args(self):
    
        example = '''examples:
    unit.py 
        Supported units are displayed.
    unit.py 10 mi 20
        10 to 20 miles are converted to kilometers.
    unit.py 99 fah
        A temperature in Fahrenheit is converted to Celsius.
    unit.py -c 0000FF
        This type of RGB value is converted to CMYK.
    unit.py -c 240,120,99
        This type of RGB value is converted to CMYK.
    unit.py -c 0.1,0.33,0.01
        This type of CMYK value is converted to RGB.
        
    To use a comma as thousand separator in Powershell, 
    wrap the number with quotes or use the escape character.
        unit "100,000" pa
        unit 100`,000 pa
    '''
        parser = argparse.ArgumentParser(
            epilog = example,  
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description = 'Convert non-metric units to the metric system.'
        )
        parser.add_argument(
            'numeral',
            nargs='*',
            help='Enter a numeric value with the full word or the first some letters of a non-metric unit.'
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
                self.numeral = float(args.numeral[0].replace(',', ''))
                self.unit_type = args.numeral[1]
                try:
                    self.until = float(args.numeral[2].replace(',', ''))
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
        result = '{:,.2f} {} = {:,.2f} {} \t {:,.2f} {} = {:,.2f} {}'.format(
            numeral, self.nonmetric_unit, metric_value, self.metric_unit, 
            numeral, self.metric_unit, nonmetric_value, self.nonmetric_unit
            )
        print(result)

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
                    self.CMYK_to_RGB(C, M, Y, K)
        else:
            R, G, B = self.parse_RGB(color)
            if R is False:
                self.error_message()
            else:
                # check if between 0 and 255
                if not all(map(lambda x: x in range(256), [R, G, B])):
                    self.error_message()
                else:
                    self.RGB_to_CMYK(R, G, B)

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

    def RGB_hex(self, R, G, B):
        RGB = [R, G, B]
        for i in range(len(RGB)):
            j = '{:3.0f}'.format(RGB[i])
            j = hex(int(j))
            j = j[2:]
            j = j.upper()
            j = j.zfill(2)
            RGB[i] = j
        RGB = ''.join(RGB)
        return RGB

    def RGB_to_CMYK(self, R, G, B):        
        Rp = R/255
        Gp = G/255
        Bp = B/255
        K = 1 - max(Rp, Gp, Bp)
        C = (1 - Rp - K) / (1 - K)
        M = (1 - Gp - K) / (1 - K)
        Y = (1 - Bp - K) / (1 - K)

        # 255,255,255
        RGBd = '{:3d}, {:3d}, {:3d}'.format(R, G, B)
        # 1.0,1.0,1.0
        RGBp = '{:1.2f}, {:1.2f}, {:1.2f}'.format(Rp, Gp, Bp)
        # FFFFFF
        RGBh = self.RGB_hex(R, G, B)
        
        result = '{} ({} / {}) = {:1.2f}, {:1.2f}, {:1.2f}, {:1.2f}'.format(RGBd, RGBp, RGBh, C, M, Y, K)
        print(result)

    def CMYK_to_RGB(self, C, M, Y, K):
        R = 255 * (1 - C) * (1 - K) 
        G = 255 * (1 - M) * (1 - K)
        B = 255 * (1 - Y) * (1 - K)
        Rp = R/255
        Gp = G/255
        Bp = B/255
        
        CMYK = map(lambda x: '{:3.2f}'.format(x), [C, M, Y, K])
        CMYK = ', '.join(CMYK)
        # 1.0,1.0,1.0
        RGBp = '{:1.2f}, {:1.2f}, {:1.2f}'.format(Rp, Gp, Bp)
        # FFFFFF
        RGBh = self.RGB_hex(R, G, B)

        result = '{} = {:3.0f}, {:3.0f}, {:3.0f} ({} / {})'.format(CMYK, R, G, B, RGBp, RGBh)
        print(result)

if __name__ == '__main__':
    unit = ConvertUnit()
    unit.parse_args()
