import abstractaction
import json
import user

#create a new user in the system whose name will be uname (id auto generated)
class CreateUser(abstractaction.AbstractAction):

	def __init__(self,uname):
		self.uname=uname
	
	@abstractaction.SqlExecutor
	def execute(self):
		return ("INSERT INTO users(uname) VALUES(%s)",(self.uname,))
	

#get a user.User object from the system whose name is uname 
#if uname is not given, than retrieves a list of all users
class GetUser(abstractaction.AbstractAction):
	def __init__(self,uname=None):
		self.uname=uname

	@user.userformatter
	@abstractaction.SqlExecutor
	def execute(self):
		if self.uname==None:
			return ("SELECT uid,uname FROM users",)
		return ("SELECT uid,uname FROM users WHERE uname=%s",(self.uname,))

	#return a dict representation of the query result

	def getDict(self):
		result=self.execute()
		if type(result) is user.User:
			return {"count":1,
			   		"users":[result.getDict()]}
		elif type(result) is list:
			return {"count":len(result),
					"users":[r.getDict() for r in result]}
		else:
			return self.emptyJSONResult 

# Sets user whose uid is follower follow user whose uid is followee
class Follow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee
	
	@abstractaction.SqlExecutor
	def execute(self):
		return ("INSERT INTO follows(follower,followee) VALUES(%s,%s)",(self.follower,self.followee))
	

#Sets user whose uid is follower unfollow user whose uid is followee
class Unfollow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee

	@abstractaction.SqlExecutor
	def execute(self):
		return ("DELETE FROM follows WHERE follower=%s AND followee=%s",(self.follower,self.followee))

#returns a list of users (or a single user) that are being followed by 
#the user whose uid is follower
class GetFollowing(GetUser):
	def __init__(self,follower):
		if type(follower) is user.User:
			self.uid=follower.getId()
		elif type(follower) is int:
			self.uid=follower
		elif type(follower) is str and follower.isdigit():
			self.uid=int(follower)

	@user.userformatter
	@abstractaction.SqlExecutor
	def execute(self):
		return ("SELECT users.uid,users.uname FROM users INNER JOIN follows"
			" ON follows.followee=users.uid WHERE follows.follower=%s ",(self.uid,))
		
	
