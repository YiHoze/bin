import sys, pkg_resources, importlib.util

if len(sys.argv) > 1:
    package_name = sys.argv[1]
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print('{} is not installed.'.format(package_name))
    else:
        package = __import__(package_name)
        if hasattr(package, '__version__'):
        	print('{}=={}'.format(package_name, package.__version__))
        else:
            print("{}'s version is not specified".format(package_name))
else:
    print('Specify a python package.')
