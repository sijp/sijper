import unittest

from usermanager import UserManager

class UserManagerTestCase(unittest.TestCase):
	def setUp(self):
		self.usermanager = UserManager()
	
	def testSingleton(self):
		usermanager2=UserManager()
	
		assert usermanager2==self.usermanager
	
	def testSingleton2(self):
		usermanager2=UserManager()
		usermanager2.userList.append(1)
		assert 1 in self.usermanager.userList
		assert 2 not in self.usermanager.userList

if __name__ == '__main__':
	    unittest.main()

