from user import User
from singleton import Singleton 
#from dbmanager import DBManager

class UserManager():
	__metaclass__=Singleton
	userList=[]

	def __init__(self):
		self.dbmanager = DBManager()
		
	

	
	
