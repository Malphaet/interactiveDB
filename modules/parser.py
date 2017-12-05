from pyparsing import *
import string, re
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

#ParseCommand = argparse.ArgumentParser(prog="iterDB",description='Parse a full text command')
#ParseCommand.add_argument('command', nargs=1,choices=["create","purge","insert","update","search","remove","show"],help="Command to execute")
#ParseCommand.add_argument('-t', metavar='table',help="Table from witch to select")
#ParseCommand.add_argument('-q', metavar='query', nargs='+', help='Query to select entries')
#ParseCommand.add_argument('-v', metavar='values', nargs='+',help='Data to store')

SimpleWord = Word(re.sub('[()" ]', '', string.printable)) # Everything not elimitated by "() "
AlWord= Word(alphas)
AlNuWord=Word(alphanums)
PuWord=Word(printables)
QueryVal = Forward()
QueryVal << ( SimpleWord | QuotedString('"')  | Group("("+OneOrMore(QueryVal)+")") ) #| QuotedString("'")

keywords_array=["create","purge","insert","update","search","remove","show"]
Keywords = Or(Keyword(i) for i in keywords_array)

VarName=AlWord + "="
Table = "-t" + AlWord
Query = "-q" + QueryVal

label = AlWord + FollowedBy(":")
attribute = Group(label + Suppress(":")+OneOrMore(PuWord,stopOn=label).setParseAction(' '.join))
ValueList = "-v" + OneOrMore(attribute) #Supress

Command = Forward()
Command <<  Optional(VarName) + Keywords + Optional(Table) + Optional(Query) + Optional(ValueList)


def parseInput(text):
    return QueryVal.parseString(text, parseAll=True)


if __name__ == '__main__':
    import blessings
    from minitest import minitest
    term=blessings.Terminal()

    mainTests=minitest.testGroup("Main Tests",term,verbose=True,align=40)
    def nestedCompare(t1,t2):
        for i in range(len(t1)):
            e,f=t1[i],t2[i]
            if type(e)!=str and type(e)!=int:
                if not nestedCompare(e,f):
                    return False
            else:
                if (e!=f):
                    return False
        return True

    class parserTest(minitest.simpleTestUnit):
        def __init__(self):
            super(parserTest, self).__init__("Parser")

        def _testBase(self):
            self.currentTest("Nested comparator")
            try:
                t=['a','b',2,["a",["RR"],22],33]
                assert(nestedCompare(t,t[:]))
                self.addSuccess()
            except:
                self.addFailure("Nested comparaison ill implemented")

            self.currentTest("Simple word")
            SimpleWord = Word(re.sub('[()" ]', '', string.printable)) # Everything not elimitated by "() "
            if nestedCompare([SimpleWord.parseString("flicker"),
                    SimpleWord.parseString("[flicker]"),
                    SimpleWord.parseString("fl(icker"),
                    SimpleWord.parseString('fli"cker')],
                    [['flicker'],['[flicker]'],['fl'],['fli']]):
                self.addSuccess()
            else:
                self.addFailure("SimpleWord ill implemented")

            self.currentTest("Query detection")
            try:
                assert(QueryVal.parseString('"should come as one" shouldnt be parsed')[0]=="should come as one")
                assert(nestedCompare(QueryVal.parseString('(Should come as four (should still be inside "should be one and ( should work"))'),[['(', 'Should', 'come', 'as', 'four', ['(', 'should', 'still', 'be', 'inside', 'should be one and ( should work', ')'], ')']]))
                self.addSuccess()
            except:
                self.addFailure("QueryVal.parseString failed")

            self.currentTest("Keywords recognition")
            for i in keywords_array:
                if not Keywords.matches(i):
                    self.addFailure("Cant match keyword {}".format(i))
            if Keywords.matches("Unmatcheble"):
                self.addFailure("Matching wrong strings")
            self.addSuccess()

            #VarName=Word(alphas) + "="
            self.currentTest("Varnames")
            if VarName.matches("voila=")&VarName.matches('still = ')&VarName.matches("works ="):
                self.addSuccess()
            else:
                self.addFailure("Can't process VarName")

            #Table = "-t" + Word(alphas)
            self.currentTest("Table selection")
            if Table.matches("-t table")&Table.matches(" -t TT")& (not Table.matches(" - Tav")):
                self.addSuccess()
            else:
                self.addFailure("Table selection incorrect")

            #Query = "-q" + QueryVal
            self.currentTest("Query")

            #ValueList = "-v" + OneOrMore(alphas+":"+(QuotedString('"')|alphas))
            self.currentTest("List of values")
            print ValueList.parseString("-v sam:Samuel val: a luva : 44  7")

            #Command <<  Optional(VarName) + Keywords + Optional(Table) + Optional(Query) + Optional(ValueList)
            self.currentTest("Command parsing")

    mainTests.addTest(parserTest())
    mainTests.test()
