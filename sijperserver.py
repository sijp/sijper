import threading
import socket
import config
import dbhandler
import clientthread

#A thread that will initiate a server socket that will listen to the given address and port
#once started, it will open a server socket and start accepting connections
#upon recieving such, it will create a new Thread (ClientThread) that will handle the actual communications

class SijperServer(threading.Thread):

	#init the server to addr and port
	def __init__(self,addr,port):
		super(SijperServer,self).__init__()
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.address=addr
		self.port=port
		self.sock.bind((addr,port))
		self.sock.listen(5)
		self.clients=[]	
	

	#stop the server and close the thread

	def stop(self):
		self.runFlag=False
		socket.socket(socket.AF_INET,socket.SOCK_STREAM).connect((self.address,self.port))
	
	
	#server thread accept loop
	def run(self):
		self.runFlag=True
		try:
			while self.runFlag:
				(clientsock,address) = self.sock.accept()
				if self.runFlag:
					ct=clientthread.ClientThread(clientsock,address,self)
					ct.start()
		finally:
			self.sock.shutdown(1)
			self.sock.close()

if __name__ == '__main__':
	dbhandler.openDB("sijper_test")
	dbhandler.setupDB()
	sijp=SijperServer("127.0.0.1",8080)
	sijp.start()
