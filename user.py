class User:
	following=[]
	
	def __init__(self):
		pass
	
	def follow(self,u):
		self.following.append(u)
	
	def unfollow(self,u):
		try:
			self.following.remove(u)
			return True
		except ValueError:
			return False
	
	def getFollowingList(self):
		return self.following
