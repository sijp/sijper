import dbhandler

class AbstractAction(object):
	
	def execute(self):
		pass

def SqliteExecutor(executef):
	def sqlitewrapper(*args, **kwargs):
		db=dbhandler.getDB()
		cmd=executef(*args,**kwargs)
		c=db.cursor()
		#print "running %s,%s" % (cmd[0],str(cmd[1]))
		rs=dbhandler.execute(cmd)
		return rs
	return sqlitewrapper

