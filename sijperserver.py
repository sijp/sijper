import threading
import socket
import config
import dbhandler
'''
start of ClientThread
'''

class ClientThread(threading.Thread):
	def __init__(self,clientsock,address,server):
		super(ClientThread,self).__init__()
		self.clientsock=clientsock
		self.address=address
		self.server=server
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
				jsonResponse=self.processData(data)
				if jsonResponse<>None:
					#write header
					sockFile.write("HTTP/1.1 200 OK\r\n")
					sockFile.write("Content-Length:%d" % len(jsonResponse) )
					sockFile.write("\r\n\r\n")
					#finish header
					sockFile.write(jsonResponse)
					sockFile.flush()

		finally:
			print "done with client"
			sockFile.close()
			self.clientsock.shutdown(1)
			self.clientsock.close()

	def processMsg(self,msg):
		if msg.startswith("Content-Length"):
			self.contentlength=int(msg[len("Content-Length: "):])

	def processData(self,data):
		paramdict={}
		action=""
		for pair in data.split("&"):
			p=pair.split("=")
			if p[0]=="action":
				action=p[1]
			else:
				paramdict[p[0]]=p[1]
		if action<>"quit":
			print "action=%s" %action
			actObj=config.actionmodules[action](**paramdict)
			return actObj.getJSON()
		
		self.server.stop()
		return None



'''
end of ClientThread
'''


class SijperServer(threading.Thread):


	def __init__(self,addr,port):
		super(SijperServer,self).__init__()
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.address=addr
		self.port=port
		self.sock.bind((addr,port))
		self.sock.listen(5)
		self.clients=[]	
	
	def stop(self):
		self.runFlag=False
		socket.socket(socket.AF_INET,socket.SOCK_STREAM).connect((self.address,self.port))

	def register(self,client):
		self.clients.append(client)
	def unregister(self,client):
		pass	


	def run(self):
		self.runFlag=True
		try:
			while self.runFlag:
				(clientsock,address) = self.sock.accept()
				if self.runFlag:
					ct=ClientThread(clientsock,address,self)
					ct.start()
		finally:
			self.sock.shutdown(1)
			self.sock.close()
			print "server is down"

if __name__ == '__main__':
	dbhandler.openDB("sijper_test")
	dbhandler.setupDB()
	sijp=SijperServer("127.0.0.1",8080)
	sijp.start()
