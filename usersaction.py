import abstractaction
import json
import user

class CreateUser(abstractaction.AbstractAction):

	def __init__(self,uname):
		self.uname=uname
	
	@abstractaction.SqliteExecutor
	def execute(self):
		print "creating user"
		return ("INSERT INTO users(uname) VALUES(%s)",(self.uname,))
	

	
class GetUser(abstractaction.AbstractAction):
	def __init__(self,uname=None):
		self.uname=uname

	@user.userformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		print "getting user"
		if self.uname==None:
			return ("SELECT uid,uname FROM users",)
		return ("SELECT uid,uname FROM users WHERE uname=%s",(self.uname,))

	def getJSON(self):
		result=self.execute()
		print "getuser:"
		print result
		print type(result) is user.User
		if type(result) is user.User:
			d={"count":1}
			d["users"]=[result.getJSON()]
			return json.dumps(d)
		elif type(result) is list:
			d={"count":len(result)}
			d["users"]=[]
			for r in result:
				d["users"].append(r.getJSON())
			return json.dumps(d)
		else:
			return self.emptyJSONResult 

class Follow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee
	
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("INSERT INTO follows(follower,followee) VALUES(%s,%s)",(self.follower,self.followee))
	


class Unfollow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee

	@abstractaction.SqliteExecutor
	def execute(self):
		return ("DELETE FROM follows WHERE follower=%s AND followee=%s",(follower,followee))
	
class GetFollowing(GetUser):
	def __init__(self,follower):
		print "getfollowing:%s"%type(follower)
		if type(follower) is user.User:
			self.uid=follower.getId()
		elif type(follower) is int:
			self.uid=follower
		elif type(follower) is str and follower.isdigit():
			self.uid=int(follower)

	@user.userformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("SELECT users.uid,users.uname FROM users INNER JOIN follows ON follows.followee=users.uid WHERE follows.follower=%s ",(self.uid,))
	
