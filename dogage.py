import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    description = "Calculate a dog's age as human."
)
parser.add_argument(
    'age',
    nargs = '*',
    help = 'Enter one or more numbers.'
)
parser.add_argument(
    '-p',
    dest = 'plot',
    action = 'store_true',
    default = False,
    help = "Draw a curve plot displaying dog's age rate"
)
args = parser.parse_args()

def age_print(age):
    dog, human = age_calculate(age)
    print('%.1f ≈ %.1f' %(dog, human))

def age_calculate(dog):
    dog = float(dog)
    human = 16 * np.log(dog) + 31
    return(dog, human)

def age_draw(age):
    age = float(age)
    dogs, humans = [], []
    i = 0
    if age < 1:
        incr = 0.1
    else:
        incr = 1
    while i <= age:
        i = i + incr
        dog, human = age_calculate(i)
        dogs.append(dog)
        humans.append(human)
    plt.xlabel('Dog age')
    plt.ylabel('Human age')
    plt.title("Dog's age as human")
    plt.plot(dogs, humans)
    plt.show()

if args.plot:
    age_draw(args.age[0])
else:
    print('dog year(s) ≈ human year(s)')
    for age in args.age:
        age_print(age)
        