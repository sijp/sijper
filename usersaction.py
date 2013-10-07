import abstractaction
import sqlite3
import user

class CreateUser(abstractaction.AbstractAction):

	def __init__(self,uname):
		self.uname=uname
	
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("INSERT INTO users(uname) VALUES(%s)",(self.uname,))

class GetUser(abstractaction.AbstractAction):
	def __init__(self,uname=None):
		self.uname=uname

	@user.userformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		if self.uname==None:
			return ("SELECT uid,uname FROM users",)
		return ("SELECT uid,uname FROM users WHERE uname=%s",(self.uname,))


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
	
class GetFollowing(abstractaction.AbstractAction):
	def __init__(self,u):
		if isinstance (u, user.User):
			self.uid=u.getId()
		elif isinstance (u, int):
			self.uid=u

	@user.userformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("SELECT users.uid,users.uname FROM users INNER JOIN follows ON follows.followee=users.uid WHERE follows.follower=%s ",(self.uid,))
	
