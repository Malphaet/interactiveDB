#!/usr/bin/env python

# GPLv3

# Modules
import argparse,sys,traceback
from modules import config,functions,parser
import blessings

# Autocomplete
import os,atexit,rlcompleter, readline
readline.parse_and_bind('tab: complete')
#readline.set_completer(completer)
histfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "commandhistory")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

# Autocomplete
class Completer(object):
    pass
status=1

def main(arg):
    res=parser.parseInput(arg)
    print res

def bettersplit(text):
    parser.parseInput(text)
    #return arg

# Command
class Execute(object):
    pass

if __name__ == '__main__':
    if len(sys.argv)>1:
        main(sys.argv[1:])
    else:
        while 1:
            try:
                args=bettersplit(raw_input("interDB > "))
                main(args)
            except KeyboardInterrupt:
                print ""
                break
            except ParseBaseException:
                traceback.print_exc()
            except:
                pass
