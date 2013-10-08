import dbhandler

'''
Abstractions for supported actions
every supported HTTP action should be subclassed from this.
Then, in config.py those classes should be mapped in a dictionary.
'''
class AbstractAction(object):
	'''
	most basic json string that should be returned to clients' requests
	'''
	emptyJSONResult='{"count":0}'

	'''
	execute the action
	'''
	def execute(self):
		pass
	'''
	execute the action and return a json representation of the response
	'''
	def getJSON(self):
		self.execute()
		return self.emptyJSONResult 

'''
decorator for methods that return an sql string
returns the result tuples of the query
'''
def SqliteExecutor(executef):
	def sqlitewrapper(*args, **kwargs):
		db=dbhandler.getDB()
		cmd=executef(*args,**kwargs)
		c=db.cursor()
		#print "running %s,%s" % (cmd[0],str(cmd[1]))
		rs=dbhandler.execute(cmd)
		return rs
	return sqlitewrapper

