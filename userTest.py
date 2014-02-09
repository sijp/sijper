import unittest

import user
class UserTestCase(unittest.TestCase):
  def setUp(self):
    self.user = user.User((1,"shlomi"))
  
  def testUserData(self):
      assert self.user.getId()==1
      assert self.user.getName()=="shlomi"
  
  def testJSONData(self):
      jsonDict=self.user.getDict()
      assert jsonDict["uid"]==self.user.getId()
      assert jsonDict["uname"]==self.user.getName()

if __name__ == '__main__':
      unittest.main()

