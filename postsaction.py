import abstractaction
import user
import post

'''
PostMessage Action - used to post messages to the system
'''
class PostMessage(abstractaction.AbstractAction):
	'''
	recieves a user.User object and a msgtext for the post
	'''
	def __init__(self,user,msgtext):
		self.user=user
		self.msg=msgtext
	
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("INSERT INTO posts(uid,ptext) VALUES(%s,%s)",(self.user.getId(),self.msg))

class GetFeed(abstractaction.AbstractAction):
	def __init__(self,user=None):
		self.user=user

	@post.postformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		if self.user<>None:
			return ("SELECT posts.pid,posts.uid,users.uname,posts.ptext FROM posts,users,follows "
			"WHERE follows.follower=%s AND users.uid=follows.followee AND posts.uid=follows.followee",(self.user.getId(),))
		return ("SELECT posts.pid,users.uname,posts.uid,posts.ptext FROM posts,users " ,)

	def getJSON(self):
		result=self.execute()
		if type(result) is post.Post:
			d={"count":1}
			d["posts"]=[result.getJSON()]
			return json.dumps(d)
		elif type(result) is list:
			d={"count":len(result)}
			d["posts"]=[]
			for r in result:
				d["posts"].append(r.getJSON())
			return json.dumps(d)
		else:
			return self.emptyJSONResult 


