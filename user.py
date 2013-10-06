
# Basic User class
# Contains a User ID (uid) and a list of references to other User objects
# which correspond to the users this user if following

class User:

	#constructor - recieves a uid corresponding to this user
	def __init__(self,(uid,uname)):
		self.uid=uid
		self.uname=uname
	
	def getId(self):
		return self.uid
	
	def getName(self):
		return self.uname


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
