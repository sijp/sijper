import unittest
import dbhandler
import usersaction
import sqlite3 

class CreateUserActionTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB(":memory:")

	def tearDown(self):
		dbhandler.closeDB()
	
	def testCreateUser(self):
		
		c=dbhandler.getDB().cursor()
		c.execute("SELECT * FROM users WHERE uname='shlomi'")
		assert c.fetchone()==None, "User is in DB before action"
		cua=usersaction.CreateUser('shlomi')
		cua.execute()
		c.execute("SELECT * FROM users WHERE uname='shlomi'")
		rs=c.fetchone()
		assert rs<>None, "No Results!"
		assert type(rs[0]) is int, "uid is not integer. value: %s" % rs[0]
		assert rs[1]=='shlomi', "uname is wrong. value: %s" % rs[1]


class GetUserTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB(":memory:")

	def tearDown(self):
		dbhandler.closeDB()

	def testGetUser(self):
		u=usersaction.GetUser('u1').execute()
		assert u==None, "users is not empty, but it should be"
		usersaction.CreateUser('u1').execute()
		u=usersaction.GetUser('u1').execute()
		assert u<>None, "users IS empty, but it should'NT be"
		assert u.getName()=='u1', "user's name is wrong: %s" % u.getName()
	
	def testGetAllUser(self):
		u=usersaction.GetUser().execute()
		assert u==None, "users is not empty, but it should be"
		usersaction.CreateUser('u1').execute()
		usersaction.CreateUser('u2').execute()
		u=usersaction.GetUser().execute()
		assert u<>None, "users IS empty, but it should'NT be"
		assert len(u)==2, "result set is not exactly 2, is actually: %d" % len(u)

class FollowActionTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB(":memory:")
		usersaction.CreateUser('u1').execute()
		usersaction.CreateUser('u2').execute()
		usersaction.CreateUser('u3').execute()

		self.u1=usersaction.GetUser('u1').execute()
		
		self.u2=usersaction.GetUser('u2').execute()
		self.u3=usersaction.GetUser('u3').execute()

	def tearDown(self):
		dbhandler.closeDB()
	
	def testFollow(self):
		c=dbhandler.getDB().cursor()

		cua=usersaction.Follow(self.u1.getId(),self.u2.getId())
		cua.execute()
		c.execute("SELECT follows.followee FROM follows,users WHERE follows.follower=users.uid AND users.uname='u1'")
		rs=c.fetchone()
		assert rs<>None, "No Results!"
		assert rs[0]==self.u2.getId(), "%d is following the wrong guy: %d" % (self.u1.getId(),rs[0])

class GetFollowingTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB(":memory:")
		self.u=[]
		for x in range(1,10):
			usersaction.CreateUser('u'+str(x)).execute()
			self.u.append(usersaction.GetUser('u'+str(x)).execute())

	def tearDown(self):
		dbhandler.closeDB()
	
	def testGetFollowing(self):
		for i in range(1,len(self.u),2):
			usersaction.Follow(self.u[0].getId(),self.u[i].getId()).execute()

		following=usersaction.GetFollowing(self.u[0]).execute()
		assert len(following)==len(self.u)/2 , "length of result is not %d" % (len(self.u)/2)
		
		for i in range(1,len(self.u),2):
			found=False
			for f in following:
				if f.getId()==self.u[i].getId() and f.getName()==self.u[i].getName():
					found=True
					break
			assert found, "user(uid=%d,uname=%s) not found" % (self.u[i].getId(), self.u[i].getName())
			found=False






if __name__ == '__main__':
	    unittest.main()

