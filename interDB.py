#!/usr/bin/env python

# GPLv3

# Modules
import argparse,sys,traceback
from pyparsing import *
import string, re
from modules import config,functions

# Autocomplete
import os,atexit,rlcompleter, readline
readline.parse_and_bind('tab: complete')
#readline.set_completer()
histfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "commandhistory")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

 #import blessings

# Autocomplete
class Completer(object):
    pass
status=1

# ArgParse
#Parse a full text command
# * connect -d database [options]
#create [-h] [-t table(take current if none given)] [data format]
#purge [-h] [-t table]
#insert [-h] [-t table] [values if confident or data:value]
#update [-h] [-q query] [-d database] data:"new value"
#search [-h] [-q query]
#remove [-h] [-d database] [-q query]
#show [-h] [-d database] [-q query]

ParseCommand = argparse.ArgumentParser(prog="iterDB",description='Parse a full text command')
ParseCommand.add_argument('command', nargs=1,choices=["create","purge","insert","update","search","remove","show"],help="Command to execute")
ParseCommand.add_argument('-t', metavar='table',help="Table from witch to select")
ParseCommand.add_argument('-q', metavar='query', nargs='+', help='Query to select entries')
ParseCommand.add_argument('-v', metavar='query', nargs='+',help='Data to store')

def main(arg):
    res=ParseCommand.parse_args(arg)
    print res

#Parse a query will soon replace argparse entirely

RawSimpleWord = Word(re.sub('[()" ]', '', string.printable))
RawWord=Word(re.sub('"', '', string.printable))
Token = Forward()
Token << ( RawSimpleWord | QuotedString('"') | Group("("+OneOrMore(Token)+")") )
Phrase = ZeroOrMore(Token)

def bettersplit(text):
    arg= Phrase.parseString(text, parseAll=True)
    print arg
    return arg

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
