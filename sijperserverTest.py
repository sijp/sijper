import unittest
import dbhandler
import sijperserver
import urllib
import urllib2
import json

class UserActionTestCase(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()
		self.serv=sijperserver.SijperServer("127.0.0.1",8080)
		self.url="http://127.0.0.1:8080"
		self.serv.start()

	def tearDown(self):
		print "teardown"
		self.serv.stop()
		dbhandler.cleanDB()
		dbhandler.closeDB()
	
	def testCreateUser(self):
		
		values={"action":"getuser", "uname":"shlomi"}
		data=urllib.urlencode(values)
		req=urllib2.Request(self.url,data)
		response=urllib2.urlopen(req)
		print response.info()
		#print "RESPONSE: "+ response.read()
		jsondata = json.loads(response.read())
		assert jsondata["count"]==0

		values={"action":"createuser", "uname":"shlomi"}
		data=urllib.urlencode(values)
		req=urllib2.Request(self.url,data)
		response=urllib2.urlopen(req)

		values={"action":"getuser", "uname":"shlomi"}
		data=urllib.urlencode(values)
		req=urllib2.Request(self.url,data)
		response=urllib2.urlopen(req)
		response.info()
		jsondata = json.loads(response.read())
		print jsondata
		assert jsondata["count"]==1


class FollowActionTest(unittest.TestCase):
	def setUp(self):
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()
		self.serv=sijperserver.SijperServer("127.0.0.1",8080)
		self.url="http://127.0.0.1:8080"
		self.serv.start()

		for i in xrange(1,10):
			values={"action":"createuser", "uname":"u%d"%i}
			data=urllib.urlencode(values)
			req=urllib2.Request(self.url,data)
			response=urllib2.urlopen(req)

	def tearDown(self):
		print "teardown"
		self.serv.stop()
		dbhandler.cleanDB()
		dbhandler.closeDB()

	def testOneFollowMany(self):
		for i in xrange(2,10):
			values={"action":"follow", "follower":"1","followee":"%d"%i}
			data=urllib.urlencode(values)
			req=urllib2.Request(self.url,data)
			response=urllib2.urlopen(req)
		
		values={"action":"getfollowing", "follower":1}
		data=urllib.urlencode(values)
		req=urllib2.Request(self.url,data)
		response=urllib2.urlopen(req)
		response.info()
		jsondata = json.loads(response.read())
		print jsondata
		assert jsondata["count"]==8




if __name__ == '__main__':
	    unittest.main()
