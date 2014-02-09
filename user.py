import json

class User(object):
    ''' Basic User class
        Contains a User ID (uid) and a list of references to other User objects
        which correspond to the users this user if following
    '''

    def __init__(self,(uid,uname)):
        ''' constructor - recieves a uid corresponding to this user
        '''
        
        self.uid=uid
        self.uname=uname
    
    def getId(self):
        ''' get the id of the user
        '''
        
        return self.uid
    
    def getName(self):
        ''' get the name of the user
        '''
        
        return self.uname
    
    def getDict(self):
        ''' get a JSON string representation of this User
        '''
        return {"uid":self.uid,"uname":self.uname}

def userformatter(func):
    ''' decorator for methods that returns (uid,uname) tuples
        usually from the database.
        returns None if no tuples are returned by func
            a User object if a single tuple is returned by fun
            a list of User objects if more than 1 tuple is returned
    '''
    
    def userWrapper(*args,**kwargs):
        rs=func(*args,**kwargs)
        if len(rs)==0:
            return None
        if len(rs)==1:
            return User(rs[0])
        ret=[]
        for r in rs:
            ret.append(User(r))
        return ret
    return userWrapper
