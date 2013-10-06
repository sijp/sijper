from dbinterface import DBInterface

# Basic User class
# Contains a User ID (uid) and a list of references to other User objects
# which correspond to the users this user if following

class User:

	#Users this user object is following
	#initialised to empty list
	following=[]
	
	#constructor - recieves a uid corresponding to this user
	def __init__(self,(uid,uname)):
		self.uid=uid
		self.uname=uname
		self.following=self.dbm.getFollowingList(uid)
	'''
	#follow a user u
	#u - a reference to another User object
	
	def follow(self,u):
		self.following.append(u)
		dbm.follow(self.uid,u.uid)
		
	
	#unfollow a user u
	#u - a reference to another User object
	#returns True if this user followed `u` before,
	#	 otherwise False
	def unfollow(self,u):
		try:
			self.following.remove(u)
			dbm.unfollow(self.uid,u.uid)
			return True
		except ValueError:
			return False
	'''

	#returns a list of the users this user if following
	def getFollowingList(self):
		return self.following

	def getName(self):
		return self.uname
