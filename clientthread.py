import threading
import socket
import config
import dbhandler

#communicate with a single client
#recieves an HTTP 1.1 POST request
#process it
#and then sends an HTTP 1.1 POST response with the relevant JSON data

class ClientThread(threading.Thread):

	#init the client thread with socket clientsock, address and SijperServer server

	def __init__(self,clientsock,address,server):
		super(ClientThread,self).__init__()
		self.clientsock = clientsock
		self.address = address
		self.server = server
	
	
	#reads the HTTP 1.1 headers and process every line
	#then reads the data and process it
	
	
	def run(self):
		sockFile=self.clientsock.makefile()
		try:
			while True:
				msg=sockFile.readline()
				if len(msg)==0 or msg=="\r\n":
					break
				self.processHeader(msg)
			
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
			sockFile.close()
			self.clientsock.shutdown(1)
			self.clientsock.close()


	#process header line.
	#for now just waits until Content-Length is recieved 

	def processHeader(self,msg):
		if msg.startswith("Content-Length"):
			self.contentlength=int(msg[len("Content-Length: "):])

	#process the data of the request.
	#data should be in HTTP POST parameter passing format. and must include an action parameter.
	#`action`'s value will be looked up in `config.actionmodules` for the appropriate AbstractAction
	#derived class that can process the action.

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
			actObj=config.actionmodules[action](**paramdict)
			return actObj.getJSON()
		
		self.server.stop()
		return None

