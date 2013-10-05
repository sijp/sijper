import unittest

from user import User

class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.user = User()
	
	def testFollow(self):
		user2=User()
		self.user.follow(user2)

		assert user2 in self.user.following
	
	def testUnfollow(self):
		user2=User()
		self.user.follow(user2)
		assert user2 in self.user.following
		self.user.unfollow(user2)
		assert user2 not in self.user.following


	def testUnfollowTwice(self):
		user2=User()
		self.user.follow(user2)
		assert user2 in self.user.following
		self.user.unfollow(user2)
		assert user2 not in self.user.following
		self.user.unfollow(user2)
		assert user2 not in self.user.following


	def testGetFollowingList(self):
		
		ulist= [User(),User(),User(),User()]

		for e1 in ulist:
			self.user.follow(e1)

		for e1 in ulist:
			assert e1 in self.user.getFollowingList()

if __name__ == '__main__':
	    unittest.main()

