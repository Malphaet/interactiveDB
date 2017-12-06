#!/usr/bin/env python

# GPLv3

# Modules
import argparse,sys,traceback
from modules import config,functions,parser
import blessings
from pyparsing import ParseBaseException

# Autocomplete
import os,atexit,rlcompleter, readline
class Completer:
    def __init__(self, words):
        self.words = words
        self.prefix = None
    def complete(self, prefix, index):
        if prefix != self.prefix:
            self.matching_words = [w for w in self.words if w.startswith(prefix)]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None


readline.parse_and_bind('tab: complete')
readline.set_completer(Completer(parser.keywords_array).complete)
histfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "commandhistory")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

def action_selecter(parsed_input):
    #res=parser.parseInput(arg)
    actions={
        "create":None,
        "purge":None,
        "insert":None,
        "update":None,
        "search":None,
        "remove":None,
        "show":None
    }
    try:
        parsed_input["command"]

        parsed_input["varname"]
        parsed_input["query"]
        parsed_input["table"]
        parsed_input["values"]
        parsed_input["database"]
    except:
        print "Whoops"
    print res

# Command
class Execute(object):
    pass

if __name__ == '__main__':
    if len(sys.argv)>1:
        main(sys.argv[1:])
    else:
        while 1:
            try:
                args=parser.parseInput(raw_input("interDB > "))
                action_selecter(args)
            except KeyboardInterrupt:
                print ""
                break
            except ParseBaseException as errmsg:
                print "Syntax error: ",errmsg
            except:
                pass
