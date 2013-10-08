import user
'''
Basic Post object
'''
class Post:

	'''
	constructor - recieves a uid corresponding to this user
	'''
	def __init__(self,(postid,uid,uname,ptext)):
		self.pid=postid
		self.user=user.User((uid,uname))
		self.ptext=ptext
	'''
	returns the id of the post
	'''
	def getId(self):
		return self.pid
	
	'''
	returns the user associated with this post
	'''
	def getUser(self):
		return self.user

	'''
	get the message of this post
	'''
	def getMessage(self):
		return self.ptext
	
	'''
	get a JSON string representation of this Post
	'''
	def getJSON(self):
		d={"pid":self.pid,"user":self.user.getJSON(),"msg":self.ptext}
		return json.dumps(d)


'''
decorator for methods that returns (postid,uid,uname,ptext) tuples
usually from the database.
returns None if no tuples are returned by func
	a Post object if a single tuple is returned by fun
	a list of Post objects if more than 1 tuple is returned
'''
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
