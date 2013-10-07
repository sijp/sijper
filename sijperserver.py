import threading
import socket
'''
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("127.0.0.1",8080))
sock.listen(5)
print "waiting for a connection..."
(clientsock,address) = sock.accept()
print "got something..."
sockFile=clientsock.makefile()
msg="nothing"
while len(msg)>0 and msg<>"\r\n":
	msg=sockFile.readline()
	print repr(msg)
sockFile.close
clientsock.shutdown(1)
clientsock.close()
sock.close()
'''
class SijperServer(threading.Thread):

	def __init__(self,addr,port):
		super(SijperServer,self).__init__()
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.bind((addr,port))
		self.sock.listen(5)
	
	'''
	start of ClientThread
	'''

	class ClientThread(threading.Thread):
		def __init__(self,clientsock,address):
			super(SijperServer.ClientThread,self).__init__()
			self.clientsock=clientsock
			self.address=address
		def run(self):
			sockFile=self.clientsock.makefile()
			try:
				while True:
					msg=sockFile.readline()
					if len(msg)==0 or msg=="\r\n":
						break
					self.processMsg(msg)
				
				if msg=="\r\n":
					data=sockFile.read(self.contentlength)
					parsedict={}
					for pair in data.split("&"):
						p=pair.split("=")
						parsedict[p[0]]=p[1]
					print parsedict
					sockFile.write("200 OK")
					sockFile.flush()
			finally:
				sockFile.close()
				self.clientsock.shutdown(1)
				self.clientsock.close()

		def processMsg(self,msg):
			if msg.startswith("Content-Length"):
				self.contentlength=int(msg[len("Content-Length: "):])


	'''
	end of ClientThread
	'''

	def stop(self):
		self.runFlag=False
		self.sock.shutdown(1)
		self.sock.close()

	def run(self):
		self.runFlag=True
		try:
			while self.runFlag:
				(clientsock,address) = self.sock.accept()
				ct=self.ClientThread(clientsock,address)
				ct.start()
		finally:
			self.sock.shutdown(1)
			self.sock.close()


sijp=SijperServer("127.0.0.1",8081)
sijp.start()
