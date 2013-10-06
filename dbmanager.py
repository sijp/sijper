import sqlite3
from user import User

class DBManager():
	def connect(self,db='sijper.db'):
		self.conn=sqlite3.connect(db)
	
	def reset(self):
		c=self.conn.cursor()
		c.execute("CREATE TABLE users(uid INTEGER PRIMARY KEY AUTOINCREMENT, uname TEXT NOT NULL)")
		c.execute("CREATE TABLE posts(pid INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, ptext TEXT, FOREIGN KEY(uid) REFERENCES users(uid))")
		c.execute("CREATE TABLE follows(fid INTEGER PRIMARY KEY AUTOINCREMENT, follower INTEGER, followee INTEGER, FOREIGN KEY(follower) REFERENCES users(uid), FOREIGN KEY(followee) REFERENCES users(uid))")
		self.conn.commit()

	def disconnect(self):
		self.conn.close()
	
	def createUser(self,name):
		c=self.conn.cursor()
		c.execute("INSERT INTO users(uname) VALUES(?)",(name,))

		self.conn.commit()
		return self.getUserByName(name)

	def getUserById(self,uid):
		c=self.conn.cursor()
		c.execute("SELECT * FROM users where uid=?",(uid,))
		rs=c.fetchone()
		if rs==None:
			return None
		return User(rs)


	def getUserByName(self,name):
		c=self.conn.cursor()
		c.execute("SELECT * FROM users where uname=?",(name,))
		rs=c.fetchone()
		if rs==None:
			return None
		return User(rs)
		
	def follow(self,follower,followee):
		c=self.conn.cursor()
		c.execute("INSERT INTO follows(follower,followee) VALUES (?,?)",(follower,followee))
		self.conn.commit()
	
	def unfollow(self,follower,followee):
		c=self.conn.cursor()
		c.execute("DELETE FROM follows WHERE follower=? AND followee=?",(follower,followee))
		self.conn.commit()

	def getFollowingList(self,uid):
		c=self.conn.cursor()
		c.execute("SELECT followee FROM follows WHERE follower=?",(uid,))
		flist=[name for resultset in c.fetchall() for name in resultset] #flatten list
		return flist

