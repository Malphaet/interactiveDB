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

# Base grammar
SimpleWord = Word(re.sub('[()" ]', '', string.printable)) # Everything not elimitated by "() "
AlWord= Word(alphas)
AlNuWord=Word(alphanums)
PuWord=Word(printables)

#Keywords
keywords_array=["create","purge","insert","update","search","remove","show"]
Keywords = Or(Keyword(i) for i in keywords_array)

# Query
operand_array=[ "=","!=",       #key must be equal or different to value
                ">", "<",       #key must be bigger or smaller than value, with strings result will be int() dependant
                "c","!c"        #val contains or doesn't contains the key
              ]
interquery= ["&"    # Both queries must be true
             #,"|"  # One query must be true (Require nested parenthesis handling)
            ]
Operand=Or(Literal(i) for i in operand_array)
Interquery = Keyword(interquery[0])
label_query = AlNuWord + Operand
stopquery=Or(Keyword(i) for i in ["&","-t","-d","-v","-h"])
QueryVal = Forward()
QueryVal << Group(label_query+OneOrMore(PuWord,stopOn=stopquery).setParseAction(" ".join)) + Optional(Interquery + QueryVal)

# Varname assignement, Tables, Query
VarName=AlWord + "="
Table = "-t" + AlWord
Query = "-q" + QueryVal

# Value List
label = AlWord + FollowedBy(":")
attribute = Group(label + Suppress(":")+OneOrMore(PuWord,stopOn=label).setParseAction(' '.join))
ValueList = "-v" + OneOrMore(attribute) #Supress

# Command Line
Command = Optional(VarName) + Keywords + OneOrMore(Keyword("-h") | Table | Query | ValueList)

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
                assert(nestedCompare(QueryVal.parseString("name c Oja & date<32 & label c 33 "),
                    [['name', 'c', 'Oja'], '&', ['date', '<', '32'], '&', ['label', 'c', '33']]))
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

            # Query = "-q" + QueryVal
            self.currentTest("Query test")
            if (Query.matches("-q name = 33 & val c foo bar")):
                self.addSuccess()
            else:
                self.addFailure()


            # ValueList = "-v" + OneOrMore(attribute) #Supress
            self.currentTest("Value assignement")
            if (nestedCompare(['-v', ['sam', 'Samuel'], ['val', 'a'], ['luva', '44 7']],
                ValueList.parseString("-v sam:Samuel val: a luva : 44  7"))):
                self.addSuccess()
            else:
                self.addFailure("Can't parse value assignement")


            #Command <<  Optional(VarName) + Keywords + Optional(Table) + Optional(Query) + Optional(ValueList)
            self.currentTest("Command parsing")
            try:
                assert(nestedCompare(Command.parseString("val= update -q name = Oja gon un & date < 22/33 -t Characters -v Salary:22 Job:God Killer"),
                    ['val', '=', 'update', '-q', ['name', '=', 'Oja gon un'], '&', ['date', '<', '22/33'], '-t', 'Characters', '-v', ['Salary', '22'], ['Job', 'God Killer']]))
                self.addSuccess()
            except:
                self.addFailure("Can't parse regular command")

    mainTests.addTest(parserTest())
    mainTests.test()
