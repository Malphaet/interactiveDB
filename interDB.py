#!/usr/bin/env python

# GPLv3

# Modules
import argparse,sys,traceback
from modules import config,functions,parser
import blessings
from pyparsing import ParseBaseException

actions={
    "create":None,
    "purge":None,
    "insert":None,
    "update":None,
    "search":None,
    "remove":None,
    "show":None
}
action_help={
    "create":"Create a database of the selected type\ncreate -d database_name database_type",
    "purge":"Delete a database or a table\npurge -d database_name [-t table]",
    "insert":"Insert an entry in a database\ninsert [-d database_name] [-t table] -v field0:value0 field1:value number 2...",
    "update":"Update or or more entries in a database\nupdate [-d database_name] [-t table] -v field:updated value -q {queryhelp} ",
    "search":"Search the table of selected database for entries matching the given query\nsearch [-d database_name] [-t table] -q {queryhelp}",
    "remove":"Remove a table or an entry matching a query\nremove [-d database_name] [-t table] -q {queryhelp}",
    "show":"Show table from the database or entries in a table matching the given query (all if none provided)\nshow [-d database] [-t table] -q {queryhelp}"
}
queryhelp="field=specific name & value>42\nFollowing operators are available: >,<,=,!=,c (contains),!c"
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


    # Backing up command used
    try:
        stateobj.listVars[parsed_input["varname"][0]]=parsed_input.asList()[2:]
        print(stateobj.listVars)
    except:
        VarName=None

    try:
        #Print help and exit
        parsed_input["help"]
        print("  "+action_help[parsed_input["command"]].format(queryhelp=queryhelp).replace("\n","\n  "))
        return True
    except KeyError:
        #Help wasn't asked
        pass
    except:
        print ("Help for this command is ill formated")
        return False

    try:
        dbname=parsed_input["database"][1]
        state.database=dbname
        if len(parsed_input["database"])>2: # Won't do much outside of create
            dbtype=parsed_input["database"][2]
            state.dbs[dbname]=dbtype
            state.database_type=dbtype
        else:
            state.database_type=state.dbs[dbname]
    except KeyError:
        #Load database from memory or Abort
        if state.database==None:
            print("Error: Can't load database, you must specify a database first") #Should have a error dict or custom errors, but speed is more important
            return False

    try:
        state.table=parsed_input["table"][1]
    except:
        #Load table from memory or Abort
        if state.table==None:
            print("  Error: Can't load table, you must specify a table first")


    try:
        query=parsed_input["query"]
        print query
    except:
        query=None

    try:
        values={}
        for i in parsed_input["values"][1:]:
            values[i[0]]=i[1]
        print values
    except:
        values=None
    try:
        res=(actions[parsed_input["command"]])
    except:
        print ("An error occured during the execution of {}".format(parsed_input["command"]))

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
                print "An exception occured"
                traceback.print_exc()
                pass
