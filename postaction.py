import abstractaction
import sqlite3
import user
import post

class PostMessage(abstractaction.AbstractAction):

	def __init__(self,user,msgtext):
		self.user=user
		self.msg=msgtext
	
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("INSERT INTO posts(uid,ptext) VALUES(?,?)",(self.user.getId(),self.msg))

class GetFeed(abstractaction.AbstractAction):
	def __init__(self,user):
		self.user=user

	@user.postformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("SELECT posts.pid,users.uname,posts.uid,posts.ptext FROM posts,users,follows WHERE follows.follower=? AND users.uid=follows.followee AND posts.uid=follows.followee",(self.user.getId(),))

