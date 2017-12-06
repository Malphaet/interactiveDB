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

def action_selecter(parsed_input,stateobj):
    #res=parser.parseInput(arg)
    stateobj.lastCommand=parsed_input
    actions={
        "create":None,
        "purge":None,
        "insert":None,
        "update":None,
        "search":None,
        "remove":None,
        "show":None
    }

    # Backing up command used
    try:
        stateobj.listVars[parsed_input["varname"]]=parsed_input.asList()[1:]
        print stateobj.listVars
    except:
        VarName=None

    try:
        parsed_input["command"]
    except:
        # ParseBaseException shouldn't happen
        pass

    try:
        dbname=parsed_input["database"][1]
        if len(parsed_input["database"])>2:
            dbtype=parsed_input["database"][2]
            state.dbs[dbname]=dbtype
        state.database=dbname
        state.database_type=parsed_input["database"]
    except KeyError:
        #Load database from memory or Abort
        pass

    try:
        state.table=parsed_input["table"][1]
    except:
        #Load table from memory or Abort
        pass

    try:
        parsed_input["query"]
        parsed_input["values"]
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
        state=config.InternalState("interDB > ")
        while 1:
            try:
                text=raw_input(state.getPrompt())
                args=parser.parseInput(text)
                action_selecter(args,state)
            except KeyboardInterrupt:
                print ""
                break
            except ParseBaseException as errmsg:
                print "Syntax error: ",errmsg
            except:
                pass
