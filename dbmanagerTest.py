import unittest
from dbmanager import DBManager

class DBManagerTestCase(unittest.TestCase):
	def setUp(self):
		self.dbm = DBManager()
		self.dbm.connect(":memory:")
		self.dbm.reset()

	def tearDown(self):
		self.dbm.disconnect()

	def testCreateUser(self):
		rs=self.dbm.getUserByName('shlomi')
		assert rs==None, "the user 'shlomi' wasn't inserted yet"
		rs=self.dbm.createUser('shlomi')
		assert rs<>None,"user creation had no effect"
		assert rs.getName()=='shlomi',"'shlomi is not in db after creation'" 
	
	def testFollow(self):
		u1=self.dbm.createUser('shlomi')
		u2=self.dbm.createUser('shlomi2')
		flist = self.dbm.getFollowingList(u1.uid)
		assert u2.uid not in flist, "new user is in the following table somehow"
		self.dbm.follow(u1.uid,u2.uid)
		flist = self.dbm.getFollowingList(u1.uid)
		assert u2.uid in flist, "user %d should be following user %d, but is not, flist: %s" %(u1.uid,u2.uid,flist)

	def testUnfollow(self):
		u1=self.dbm.createUser('shlomi')
		u2=self.dbm.createUser('shlomi2')
		self.dbm.follow(u1.uid,u2.uid)
		flist = self.dbm.getFollowingList(u1.uid)
		assert u2.uid in flist, "user %d should be following user %d, but is not, flist: %s" %(u1.uid,u2.uid,flist)
		self.dbm.unfollow(u1.uid,u2.uid)
		flist = self.dbm.getFollowingList(u1.uid)
		assert u2.uid not in flist, "user %d in still following user %d, flist: %s" % (u1.uid,u2.uid,flist)


if __name__ == '__main__':
	    unittest.main()

