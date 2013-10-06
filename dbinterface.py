from singleton import Singleton

class DBInterface:
	__metaclass__=Singleton
	def connect(self,db='sijper.db'):
		pass
			
	def reset(self):
		pass

	def disconnect(self):
		pass	
	def createUser(self,name):
		pass

	def getUserById(self,uid):
		pass
	
	def getUserByName(self,name):
		pass
		
	def follow(self,follower,followee):
		pass
	
	def unfollow(self,follower,followee):
		pass

	def getFollowingList(self,uid):
		pass

