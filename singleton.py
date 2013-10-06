class Singleton(type):
	ins={}

	def __call__(cls,*args,**kwargs):
		print cls.ins
		if cls not in cls.ins:
			cls.ins[cls]=super(Singleton,cls).__call__(*args,**kwargs)
		return cls.ins[cls]
