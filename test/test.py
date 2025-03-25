import argparse
import importlib


p = argparse.ArgumentParser()
subp = p.add_subparsers(dest='cmd')

# name_flags = ['-a','--nnnnn','--name']
# constrain = {'type':str}

greet_parser = subp.add_parser(name='greet')
greet_parser.add_argument('name')
greet_parser.add_argument('age')
args = p.parse_args()
print(args)
