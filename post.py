import user
import json

class Post(object):
    ''' Basic Post object
    
    '''
    
    def __init__(self,(postid,uid,uname,ptext)):
        ''' constructor - recieves a uid corresponding to this user
        
        '''
        self.pid=postid
        self.user=user.User((uid,uname))
        self.ptext=ptext

    def getId(self):
        ''' returns the id of the post
        '''
        return self.pid
    
    def getUser(self):
        ''' returns the user associated with this post
        '''
        return self.user

    def getMessage(self):
        ''' get the message of this post
        '''
        return self.ptext
    
    def getDict(self):
        ''' get a JSON string representation of this Post
        '''
        
        return {"pid":self.pid,"user":self.user.getDict(),"msg":self.ptext}

def postformatter(func):
    ''' decorator for methods that returns (postid,uid,uname,ptext) tuples
        usually from the database.
        returns None if no tuples are returned by func
        a Post object if a single tuple is returned by fun
        a list of Post objects if more than 1 tuple is returned
            
    '''
    
    def postWrapper(*args,**kwargs):
        rs=func(*args,**kwargs)
        if len(rs)==0:
            return None
        if len(rs)==1:
            return Post(rs[0])
        return [Post(r) for r in rs]
    return postWrapper
