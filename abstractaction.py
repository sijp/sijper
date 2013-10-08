import dbhandler

class AbstractAction(object):
	
	emptyJSONResult='{"count":0}'

	def execute(self):
		pass
	def getJSON(self):
		self.execute()
		return self.emptyJSONResult 

def SqliteExecutor(executef):
	def sqlitewrapper(*args, **kwargs):
		db=dbhandler.getDB()
		cmd=executef(*args,**kwargs)
		c=db.cursor()
		#print "running %s,%s" % (cmd[0],str(cmd[1]))
		rs=dbhandler.execute(cmd)
		return rs
	return sqlitewrapper

