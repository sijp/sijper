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
class SijperServer:

	def __init__(self,addr,port):
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.bind((addr,port))
		sock.listen(5)
	
	class ClientThread(threading.Thread):
		def __init__(self,clientsock,address):
			self.clientsock=clientsock
			self.address=address
		def run(self):
			sockfile=clientsock.makefile()
			while True:
				msg=sockFile.readline()
				if len(msg)==0 or msg=="\r\n":
					break 
			sockFile.close()
			self.clientsock.shutdown(1)
			self.clientsock.close()
	def stop(self):
		self.runFlag=False

	def start(self):
		self.runFlag=True
		while self.runFlag:
			(clientsock,address) = self.sock.accept()
			ct=ClientThread(clientsock,address)
			ct.start()

