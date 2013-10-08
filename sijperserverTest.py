import unittest
import dbhandler
import sijperserver
import urllib
import urllib2
import json

class HTTPTestCase(unittest.TestCase):
	def setUp(self):
		self.startServer()

	def tearDown(self):
		self.stopServer()
	
	def startServer(self):
		dbhandler.openDB("sijper_test")
		dbhandler.setupDB()
		self.serv=sijperserver.SijperServer("127.0.0.1",8080)
		self.url="http://127.0.0.1:8080"
		self.serv.start()

	def stopServer(self):
		self.serv.stop()
		dbhandler.cleanDB()
		dbhandler.closeDB()


	def sendPost(self,url,values):
		data=urllib.urlencode(values)
		req=urllib2.Request(url,data)
		return urllib2.urlopen(req)


class UserActionTestCase(HTTPTestCase):
				
	def testCreateUser(self):
		
		values={"action":"getuser", "uname":"shlomi"}
		response=self.sendPost(self.url,values)
		jsondata = json.loads(response.read())
		assert jsondata["count"]==0

		values={"action":"createuser", "uname":"shlomi"}
		response=self.sendPost(self.url,values)

		values={"action":"getuser", "uname":"shlomi"}
		response=self.sendPost(self.url,values)
		jsondata = json.loads(response.read())
		assert jsondata["count"]==1


class FollowActionTest(HTTPTestCase):
	def setUp(self):
		self.startServer()
		for i in xrange(1,10):
			values={"action":"createuser", "uname":"u%d"%i}
			self.sendPost(self.url,values)

	def testOneFollowMany(self):
		for i in xrange(2,10):
			values={"action":"follow", "follower":1,"followee":i}
			self.sendPost(self.url,values)
					
		values={"action":"getfollowing", "follower":1}
		response=self.sendPost(self.url,values)
		jsondata = json.loads(response.read())
		assert jsondata["count"]==8


class FeedsActionTest(HTTPTestCase):
	def setUp(self):
		self.startServer()
		for i in xrange(1,5):
			values={"action":"createuser","uname":"u%d"%1}
			self.sendPost(self.url,values)

		for i in xrange(2,5):
			values={"action":"follow","follower":1,"followee":i}
			self.sendPost(self.url,values)


	def testGetFeed(self):
		for i in xrange(2,5):
			values={"action":"postmessage","userid":i,"msgtext":"My ID is %d"%i}
			response=self.sendPost(self.url,values)
		values={"action":"getfeed","userid":1}
		response=self.sendPost(self.url,values)
		jsondata1=json.loads(response.read())
		assert jsondata1["count"]==3
		values={"action":"getglobalfeed"}
		response=self.sendPost(self.url,values)
		jsondata2=json.loads(response.read())
		assert jsondata2["count"]==3
	
	def testGetFeedTwice(self):
		for i in xrange(2,5):
			values={"action":"postmessage","userid":i,"msgtext":"My ID is %d"%i}
			response=self.sendPost(self.url,values)
		values={"action":"getfeed","userid":1}
		response=self.sendPost(self.url,values)
		jsondata1=json.loads(response.read())
		
		values={"action":"getfeed","userid":1}
		response=self.sendPost(self.url,values)
		jsondata2=json.loads(response.read())

		
		pids1=[p1["pid"] for p1 in jsondata1["posts"]]
		pids2=[p2["pid"] for p2 in jsondata2["posts"]]

		assert len(set(pids1)-set(pids2))==0,"2 subsequent feed requests don't match"



if __name__ == '__main__':
	    unittest.main()
