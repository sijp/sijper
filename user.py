import json


#Basic User class
#Contains a User ID (uid) and a list of references to other User objects
#which correspond to the users this user if following
class User(object):

	#constructor - recieves a uid corresponding to this user
	def __init__(self,(uid,uname)):
		self.uid=uid
		self.uname=uname
	
	
	#get the id of the user
	def getId(self):
		return self.uid
	
	
	#get the name of the user
	def getName(self):
		return self.uname
	
	
	#get a JSON string representation of this User
	def getJSON(self):
		d={"uid":self.uid,"uname":self.uname}
		return json.dumps(d)


#decorator for methods that returns (uid,uname) tuples
#usually from the database.
#returns None if no tuples are returned by func
#	a User object if a single tuple is returned by fun
#	a list of User objects if more than 1 tuple is returned

def userformatter(func):
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
