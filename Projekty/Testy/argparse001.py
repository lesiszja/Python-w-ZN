import sys
import argparse

print(sys.argv)

parser = argparse.ArgumentParser(description='Process some integers')
parser.add_argument('filename', help='filename to process')
parser.add_argument('--limit', '-l', type=int,default=0, help='limit the number of line to process')
parser.add_argument('--flag', '-f', action='store_true', help='just a flag')
parser.add_argument('--list', '-L', nargs='*',help='lits of strings')

args = parser.parse_args()

print(args)
print(args.filename)
print(args.limit)
print(args.flag)
print(args.list)
