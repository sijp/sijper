import unittest
import dbhandler
import postsaction
import usersaction
import sqlite3 

class PostMessageTestCase(unittest.TestCase):
    def setUp(self):
        dbhandler.openDB("sijper_test")
        dbhandler.setupDB()

    def tearDown(self):
        dbhandler.cleanDB()
        dbhandler.closeDB()

    def testPostMessage(self):
        usersaction.CreateUser("u1").execute()
        u=usersaction.GetUser("u1").execute()

        postsaction.PostMessage(u.getId(),"Hello World").execute()
        posts=postsaction.GetFeed().execute()
        assert posts<>None, "post wasn't posted"


if __name__ == '__main__':
    unittest.main()

