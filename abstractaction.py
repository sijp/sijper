import dbhandler

class AbstractAction(object):
	
	def execute(self):
		pass

def SqliteExecutor(executef):
	def sqlitewrapper(*args, **kwargs):
		db=dbhandler.getDB()
		cmd=executef(*args,**kwargs)
		c=db.cursor()
		if len(cmd)==2:
			print "running %s,%s" % (cmd[0],str(cmd[1]))
			c.execute(cmd[0],cmd[1])
		else:
			c.execute(cmd[0])
		rs=c.fetchall()
		db.commit()
		return rs
	return sqlitewrapper

