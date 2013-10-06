import abstractaction
import sqlite3
import user

class CreateUser(abstractaction.AbstractAction):

	def __init__(self,uname):
		self.uname=uname
	
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("INSERT INTO users(uname) VALUES(?)",(self.uname,))

class GetUser(abstractaction.AbstractAction):
	def __init__(self,uname=None):
		self.uname=uname

	@user.userformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		if self.uname==None:
			return ("SELECT uid,uname FROM users",)
		return ("SELECT uid,uname FROM users WHERE uname=?",(self.uname,))


class Follow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee
	
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("INSERT INTO follows(follower,followee) VALUES(?,?)",(self.follower,self.followee))

class Unfollow(abstractaction.AbstractAction):
	def __init__(self,follower,followee):
		self.follower=follower
		self.followee=followee

	@abstractaction.SqliteExecutor
	def execute(self):
		return ("DELETE FROM follows WHERE follower=? AND followee=?",(follower,followee))
	
class GetFollowing(abstractaction.AbstractAction):
	def __init__(self,u):
		print "type(u)=%s" %u
		if isinstance (u, user.User):
			self.uid=u.getId()
		elif isinstance (u, int):
			self.uid=u

	@user.userformatter
	@abstractaction.SqliteExecutor
	def execute(self):
		return ("SELECT users.uid,users.uname FROM users,follows WHERE follows.follower=? AND follows.followee=users.uid",(self.uid,))
	
