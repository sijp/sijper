import abstractaction
import user
import post
import json

'''
PostMessage Action - used to post messages to the system
'''
class PostMessage(abstractaction.AbstractAction):
	'''
	recieves a user.User object and a msgtext for the post
	'''
	def __init__(self,userid,msgtext):
		self.userid=userid
		self.msg=msgtext
	
	@abstractaction.SqlExecutor
	def execute(self):
		return ("INSERT INTO posts(uid,ptext) VALUES(%s,%s)",(self.userid,self.msg))

class GetFeed(abstractaction.AbstractAction):
	def __init__(self,userid=None):
		self.userid=userid

	@post.postformatter
	@abstractaction.SqlExecutor
	def execute(self):
		if self.userid<>None:
			return ("SELECT posts.pid,posts.uid,users.uname,posts.ptext FROM posts,users,follows "
				"WHERE follows.follower=%s AND users.uid=follows.followee AND posts.uid=follows.followee",(self.userid,))
		return ("SELECT posts.pid,users.uname,posts.uid,posts.ptext FROM posts INNER JOIN users "
			"ON users.uid=posts.uid" ,)

	def getDict(self):
		result=self.execute()
		if type(result) is post.Post:
			return {"count":1,
			   "posts":[result.getJSON()]}
		elif type(result) is list:
			return {"count":len(result),
				"posts":[r.getDict() for r in result]}
		else:
			return self.emptyJSONResult 


