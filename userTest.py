import unittest

import user
import json 
class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.user = user.User((1,"shlomi"))
	
	def testUserData(self):
			assert self.user.getId()==1
			assert self.user.getName()=="shlomi"
	
	def testJSONData(self):
			jsonDict=json.loads(self.user.getJSON())
			assert jsonDict["uid"]==self.user.getId()
			assert jsonDict["uname"]==self.user.getName()

if __name__ == '__main__':
	    unittest.main()

