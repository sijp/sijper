import user
# Basic Post class

class Post:

	#constructor - recieves a uid corresponding to this user
	def __init__(self,(postid,uid,uname,ptext)):
		self.pid=postid
		self.user=user.User((uid,uname))
		self.ptext=ptext
	
	def getId(self):
		return self.pid
	
	def getUser(self):
		return self.user

	def getMessage(self):
		return self.ptext


def postformatter(func):
	def postWrapper(*args,**kwargs):
		rs=func(*args,**kwargs)
		if len(rs)==0:
			return None
		if len(rs)==1:
			return Post(rs[0])
		ret=[]
		for r in rs:
			ret.append(Post(r))
		return ret
	return postWrapper
