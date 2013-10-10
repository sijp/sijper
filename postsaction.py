import abstractaction
import user
import post
import json

#PostMessage Action - used to post messages to the system
class PostMessage(abstractaction.AbstractAction):
	#recieves a user.User object and a msgtext for the post
	def __init__(self,userid,msgtext):
		self.userid=userid
		self.msg=msgtext
	
	@abstractaction.SqlExecutor
	def execute(self):
		return ("INSERT INTO posts(uid,ptext) VALUES(%s,%s)",(self.userid,self.msg))

#gets a message feed from the system
#if userid is given, retrieves only messages this user
#is following, otherwise retrieves all messages
#messages retrieves must have PID that is greater (newer) than fromid

class GetFeed(abstractaction.AbstractAction):
	def __init__(self,userid=None,fromid=-1):
		self.userid=userid
		self.fromid=fromid

	@post.postformatter
	@abstractaction.SqlExecutor
	def execute(self):
		if self.userid<>None:
			return ("SELECT posts.pid,posts.uid,users.uname,posts.ptext FROM posts,users,follows "
				"WHERE follows.follower=%s AND users.uid=follows.followee AND posts.uid=follows.followee AND posts.pid>%s ORDER BY posts.pid",(self.userid,self.fromid))
		return ("SELECT posts.pid,posts.uid,users.uname,posts.ptext FROM posts INNER JOIN users "
			"ON users.uid=posts.uid WHERE posts.pid>%s ORDER BY posts.pid" ,(self.fromid,))
	
	#returns a dict representation of the query result
		
	def getDict(self):
		result=self.execute()
		print type(result)
		if type(result) is post.Post:
			return {"count":1,
			   "posts":[result.getDict()]}
		elif type(result) is list:
			return {"count":len(result),
				"posts":[r.getDict() for r in result]}
		else:
			return self.emptyJSONResult 


