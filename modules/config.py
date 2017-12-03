# Pref Loader
class PrefLoader(object):
    pass

# DB Selecter
class DbSelecter(object):
    def __init__(self):
        self._status=None # True for sucess False for an error in the request
        self._returnMessage="" # Custom return message for debug & such
        self.result="" #Result of the query
        self._init=False
        self._initialise()

    def _status(self,state,message):
        self._status=state
        self._returnMessage=message

    def checkStatus(self):
        "Check the status of the last query should log/print/except any error"
        if self._status==None:
            return True
        return self._status==True

    def checkInitialised(self):
        "Return True if the database is correctly initialysed, dataval is loaded and such, should print/log/except anything if not"
        return self._init

    def _initialyse(self):
        "Initialyse the database or any process taking place beforehand"
        self._init=True
        return True

    def insert(self,*args,**kwargs):
        "Execute the insert query with the selected args, kwarg (You might want to enforce data validation here)"
        self.result=""
        self._status(True,"")
        return True

    def update(self,id,updatedict):
        "Update the fields with the value in the updatedict"
        self.result=""
        self._status(True,"")
        return True

    def search(self,**kwargs):
        "Search for arguments matching the query and return a list of id matched"
        self.result=[]
        self._status(True,"")
        return True

    def remove(self,id):
        "Remove the ids given"
        self.result=''
        self._status(True,"")
        return True




# Internal State
# Store info on witch query was made last and allow acess to last results (especially important to avoid having the user entering over and over again numbers)



def makeDb(dbtype,args,kwargs):
    return DbSelecter(args,kwargs)

def makeInternal(dbtype,args,kwargs):
    return InternalState(args,kwargs)
