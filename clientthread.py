import threading
import socket
import config
import dbhandler

class ClientThread(threading.Thread):
    ''' communicate with a single client
        recieves an HTTP 1.1 POST request
        process it
        and then sends an HTTP 1.1 POST response with the relevant JSON data

    '''

    def __init__(self,clientsock,address,server):
        '''init the client thread with socket clientsock, address and SijperServer server
        '''
        
        super(ClientThread,self).__init__()
        self.clientsock = clientsock
        self.address = address
        self.server = server
    
    def run(self):
        ''' reads the HTTP 1.1 headers and process every line
            then reads the data and process it
        '''
        
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
                    self.sendHeaders(sockFile,len(jsonResponse))
                    #finish header
                    sockFile.write(jsonResponse)
                    sockFile.flush()

        finally:
            sockFile.close()
            self.clientsock.shutdown(1)
            self.clientsock.close()

    def sendHeaders(self,sockFile,contentlength):
        ''' send http headers to client
        '''
        sockFile.write("HTTP/1.1 200 OK\r\n")
        sockFile.write("Content-Type: application/json;charset=UTF-8\r\n")
        sockFile.write("Content-Length: %d\r\n" % contentlength)
        sockFile.write("Content-Encoding: utf-8 \r\n")
        sockFile.write("Connection: keep-alive\r\n")
        sockFile.write("\r\n")
    
    def processHeader(self,msg):
            '''process header line.
               for now just waits until Content-Length is recieved 
                 
            '''
        if msg.startswith("Content-Length"):
            self.contentlength=int(msg[len("Content-Length: "):])

    def processData(self,data):
        ''' process the data of the request.
            data should be in HTTP POST parameter passing format. and must include
            an action parameter. `action`'s value will be looked up in
            `config.actionmodules` for the appropriate AbstractAction
            derived class that can process the action.
        
        '''
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

