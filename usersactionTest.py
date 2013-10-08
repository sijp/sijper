import unittest
import dbhandler
import usersaction

class CreateUserActionTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()

	def tearDown(self):
		dbhandler.cleanDB()
		dbhandler.closeDB()


	
	def testCreateUser(self):
		
		rs=dbhandler.execute(("SELECT * FROM users WHERE uname='shlomi'",))
		assert len(rs)==0, "User is in DB before action"
		cua=usersaction.CreateUser('shlomi')
		cua.execute()
		rs=dbhandler.execute(("SELECT * FROM users WHERE uname='shlomi'",))
		assert len(rs)>0, "Creation failed"
		result=rs[0]
		assert type(result[0]) is long, "uid is not integer. value: %s, type:%s" % result[0]
		assert result[1]=='shlomi', "uname is wrong. value: %s" % result[1]
class GetUserTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()

	def tearDown(self):
		dbhandler.cleanDB()
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
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()
		usersaction.CreateUser('u1').execute()
		usersaction.CreateUser('u2').execute()
		usersaction.CreateUser('u3').execute()

		self.u1=usersaction.GetUser('u1').execute()
		
		self.u2=usersaction.GetUser('u2').execute()
		self.u3=usersaction.GetUser('u3').execute()

	def tearDown(self):
		dbhandler.cleanDB()
		dbhandler.closeDB()
	
	def testFollow(self):

		cua=usersaction.Follow(self.u1.getId(),self.u2.getId())
		cua.execute()
		following=usersaction.GetFollowing(self.u1).execute()
		assert following<>None, "No Results!"
		assert following.getId()==self.u2.getId(), "%d is following the wrong guy: %d" % (self.u1.getId(),following.getId())

class GetFollowingTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()

		self.u=[]
		for x in range(1,10):
			usersaction.CreateUser('u'+str(x)).execute()
			self.u.append(usersaction.GetUser('u'+str(x)).execute())

	def tearDown(self):
		dbhandler.cleanDB()
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

