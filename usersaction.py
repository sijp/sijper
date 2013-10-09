import abstractaction
import json
import user

class CreateUser(abstractaction.AbstractAction):

	def __init__(self,uname):
		self.uname=uname
	
	@abstractaction.SqlExecutor
	def execute(self):
		return ("INSERT INTO users(uname) VALUES(%s)",(self.uname,))
	

	
class GetUser(abstractaction.AbstractAction):
	def __init__(self,uname=None):
		self.uname=uname

	@user.userformatter
	@abstractaction.SqlExecutor
	def execute(self):
		if self.uname==None:
			return ("SELECT uid,uname FROM users",)
		return ("SELECT uid,uname FROM users WHERE uname=%s",(self.uname,))



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

'''	def getJSON(self):
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
'''
class Follow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee
	
	@abstractaction.SqlExecutor
	def execute(self):
		return ("INSERT INTO follows(follower,followee) VALUES(%s,%s)",(self.follower,self.followee))
	


class Unfollow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee

	@abstractaction.SqlExecutor
	def execute(self):
		return ("DELETE FROM follows WHERE follower=%s AND followee=%s",(self.follower,self.followee))
	
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
		
	
