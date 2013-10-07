import abstractaction
import user
import post

class PostMessage(abstractaction.AbstractAction):

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

