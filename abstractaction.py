import dbhandler
import json

class AbstractAction(object):
    ''' Abstractions for supported actions
        every supported HTTP action should be subclassed from this.
        Then, in config.py those classes should be mapped in a dictionary.
    '''
    
    #most basic json string that should be returned to clients' requests
    emptyJSONResult={"count":0}

    def execute(self):
        '''execute the action
        
        '''
        pass
    
    def getJSON(self):
        '''execute the action and return a json representation of the response
        
        '''
        
        return json.dumps(self.getDict())

    def getDict(self):
        self.execute()
        return self.emptyJSONResult 

def SqlExecutor(getSQLQuery):
    '''returns the result tuples of the query
       
       decorator for methods that return an sql string
       
    '''
    
    def sqlitewrapper(*args, **kwargs):
        cmd=getSQLQuery(*args,**kwargs)
        rs=dbhandler.execute(cmd)
        return rs
    return sqlitewrapper

