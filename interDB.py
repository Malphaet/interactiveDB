#!/usr/bin/env python

# GPLv3

# Modules
import argparse,sys
from pyparsing import *
import string, re

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
#Parse a query
#ParseQuery = argparse.ArgumentParser(description='Parse the query within a command')

def bettersplit(text):
    RawSimpleWord = Word(re.sub('[()" ]', '', string.printable))
    RawWord=Word(re.sub('"', '', string.printable))
    Token = Forward()
    Token << ( RawSimpleWord | OneOrMore(RawWord) | Group('(' + OneOrMore(RawSimpleWord) + ')') )
    Phrase = ZeroOrMore(Token)

    print Phrase.parseString(text, parseAll=True)


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
            except:
                pass
