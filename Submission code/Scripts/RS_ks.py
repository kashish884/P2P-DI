import threading
import os
import platform
import sys
import time
import datetime
import socket


OS = platform.system()
FilePath = ''
CP1 = ''

class RSaddition:    # Addition of Peer related details in the Registration server

    def __init__(self,hostname=None,list_port=0,cookie=0,actflag=1,ttl=7200, next_entry=None):
        self.hostname = str(hostname)
        self.list_port = int(list_port)
        self.cookie = str(cookie)
        if actflag == 1 :
           self.actflag = 'Active'
        else :
            self.actflag = 'Inactive'
        self.TTL = int(ttl)
        self.ActvCnt = 1
        self.RecentlyActv = time.ctime()
        self.next_entry = next_entry
        
    def get_next(self):            #initialising getters and setters for all the Peer index entry attributes.
        return self.next_entry

    def get_hostname(self):
        return self.hostname

    def get_cookie(self):
        return self.cookie

    def get_actflag(self):
        return self.actflag

    def get_TTL(self):
        return self.TTL

    def get_list_port(self):
        return self.list_port

    def get_ActvCnt(self):
        return self.ActvCnt

    def get_RecentlyActv(self):
        return self.RecentlyActv

    def set_next(self,new_next):
        self.next_entry = new_next

    def set_ttl(self,ttl):
        self.TTL = int(ttl)

    def set_flag(self,actflag):
        if actflag == 1 :
           self.actflag = 'Active'
        else :
            self.actflag = 'Inactive'

    def set_ActvCnt(self,ActvCnt):
        self.ActvCnt = ActvCnt

    def set_cookie(self,CookieNo):
        self.cookie = CookieNo



class PeerIndex():                   #Class to Create attributes within peertable as PeerIndex  

    def __init__(self,head=None):
        self.head=head

    def get_head(self):
        return self.get_head

    def CreateEntry(self,hostname,list_port,port):      #To add entry in peer-index and assign cookie 
        new_entry = RSaddition(hostname,list_port)
        new_entry.set_next(self.head)
        self.head = new_entry
        cookieNo = "%s:%s" %(hostname,port)
        new_entry.set_cookie(cookieNo)   
        return cookieNo
    
    def UpdateTTL(self,KAsock,addr):           #To set TTL of peer to 7200 sec upon recieving "KEEPALIVE" message 
        while True:
            message = KAsock.recv(2048)
            msg = str.split(message,"(%^&***)")
            if msg[0] == "KEEPALIVE":
                hostname = msg[3]
                current = self.head
                while current != None:
                    if current.get_hostname() == hostname:
                        current.set_ttl(7200)
                        break
                    current = current.get_next()
        KAsock.close()

    def Determine_Actvcnt(self,hostname):       #To calculate the registration count of peer
        current = self.head
        found = False
        while current and found is False:
            if current.get_hostname() == hostname:
                found = True
                current.set_ttl(7200)
                current.ActvCnt = current.ActvCnt + 1
                break
            else:
                current = current.get_next()
        if found is False:
            print "Peer not in list"

    def Leave_func(self,hostname):          #To set 'Inactive' flag and TTL to 0 sec when "LEAVE" message is recieved
        current = self.head
        found = False
        while current and found is False:
            if current.get_hostname() == hostname:
                found = True
                current.set_flag(0)
                current.set_ttl(0)
                break
            current = current.get_next()
        if found is False:
            print "Peer not in list"
        

    def Peer_Table_Send(self,hostname):         #To send across the whole Peer-Index 
        global OS
        current = self.head
        data = ''
        while current != None:
            if (current.get_hostname() != hostname):
                if (current.get_actflag() == 'Active'):
                    data = data+"(%^&***)"+str(current.get_hostname())+"(%^&***)"+str(current.get_cookie())+"(%^&***)"+str(current.get_actflag())+"(%^&***)"+str(current.get_TTL())+"(%^&***)"+str(current.get_list_port())+"(%^&***)"+str(current.get_ActvCnt())+"(%^&***)"+str(current.get_RecentlyActv())
            current = current.get_next()
        if data == '':
            header = "P2P-DI/1.0(%^&***)404(%^&***)ERROR(%^&***)Host:(%^&***)"+hostname+"(%^&***)OS:(%^&***)"+OS
            data = "(%^&***)No 'Active' peers in network"
            response = header + data
        else:
            header = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)"+hostname+"(%^&***)OS:(%^&***)"+OS
            response = header + data
        return response

    def peer_index_file_append(self):       #To get latest peer-index entry for writing to local file
        current = self.head
        response = str(current.get_hostname())+"\t"+str(current.get_cookie())+"\t"+str(current.get_actflag())+"\t\t"+str(current.get_TTL())+"\t"+str(current.get_list_port())+"\t"+str(current.get_ActvCnt())+"\t"+str(current.get_RecentlyActv())+"\n"
        return response


    def timer_function(self):                   #To decrement TTL of peers periodically
        while True :
            time.sleep(1)
            current = self.head
            if self.head != None :
                while current != None :
                    if(current.get_TTL() > 0):
                        TTL = current.get_TTL()-1
                        current.set_ttl(TTL)
                    if (current.get_TTL() == 0):
                        current.set_flag(0)
                    current = current.get_next()
   

    def display(self):
        current = self.head
        print "Hostname\tCookie\t\t\tActive Flag\t\tTTL\t\tListening_Port\tRegistration Count\tMost Recent Registration\n"
        while current:
            print "%s\t%s\t%s\t\t%d\t%d\t%d\t\t\t%s\n" %(current.get_hostname(), current.get_cookie(), current.get_actflag(), current.get_TTL(), current.get_list_port(), current.get_ActvCnt(), current.get_RecentlyActv())
            current = current.get_next()





def ServerMain(connectionSocket,addr):       # To initiate socket details of the RS server
    global CP1
    global FilePath
    msg = connectionSocket.recv(2048)
    msg1 = str.split(msg,"(%^&***)")
 
    if msg1[0] == "REGISTER":
        if msg1[4] != "Cookie:":

            hostname = msg1[3]
            list_port = msg1[5]
            peeraddr = connectionSocket.getpeername()
            Cookie = CP1.CreateEntry(hostname,list_port,peeraddr[1])
            reply = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Cookie:(%^&***)"+Cookie+"(%^&***)Host:(%^&***)"+hostname+"(%^&***)OS:(%^&***)"+OS
            print("Registering the Client P2P-DI/1.0(%^&***)200(%^&***)OK ")
            print("Cookie:"+Cookie)
            print("Hostname:" + hostname)
            print("OS:" + OS)
            connectionSocket.send(reply)
            CP1.display()
            index = CP1.peer_index_file_append()
            os.chdir(FilePath)
            f = open("Peer_Index.txt", "a+")
            try:
                f.write(index)
            finally:
                f.close()
            connectionSocket.close()
        elif msg1[4] == "Cookie":
            hostname = msg1[3]
            CP1.Determine_Actvcnt()
            reply = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Cookie:(%^&***)"+Cookie+"(%^&***)Host:(%^&***)"+hostname+"(%^&***)OS:(%^&***)"+OS
            connectionSocket.send(reply)
            connectionSocket.close()
        
    if msg1[0] == "LEAVE" :
        print("Setting Peer %s to 'Inactive'...\n") %(str(addr))
        hostname = msg1[3] 
        CP1.Leave_func(hostname)
        reply = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)"+hostname+"\nOS:(%^&***)"+OS
        connectionSocket.send(reply)
        CP1.display()
        connectionSocket.close()
        
    if msg1[1] == "PEER-INDEX" :
        print("SENDING PEER - INDEX  P2P-DI/1.0 200 OK")
        #print("Host:" + hostname)
        #print("OS:" + OS)
        hostname = msg1[4]
        peer_table = CP1.Peer_Table_Send(hostname)
        connectionSocket.send(peer_table)
        connectionSocket.close()


    
def main():
    global CP1
    global FilePath
    CP1= PeerIndex()
    t = threading.Thread(target=CP1.timer_function, args=())
    t.start()

    wd = os.getcwd()
    if OS == "Windows":
            directory = wd+"\IP_Project\Server"
    else:
        directory = wd+"/IP_Project/Server"
    if not os.path.exists(directory):
        os.makedirs(directory)
    FilePath = directory
    os.chdir(FilePath)
    f = open("Peer_Index.txt","w+")
    f.write("\nHOSTNAME\tCOOKIE\t\t\tACTIVE FLAG\tTTL\tLISTENING PORT\tREGISTRATION COUNT\tMOST RECENT REGISTRATION\n")
    f.close()
    
    ServerSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    ServerSocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    ServerSocket.bind( ( '', 65423 ) )

    ServerSocket.listen(1)
    while True:
            connectionSocket,addr = ServerSocket.accept()
            print "on Connection from: " + str(addr) + "\n"
            MainThread = threading.Thread(target=ServerMain,args=(connectionSocket,addr))
            KeepAliveThread = threading.Thread(target=CP1.UpdateTTL,args=(connectionSocket,addr))
            KeepAliveThread.daemon = True
            MainThread.start()
            KeepAliveThread.start()
        

            






if __name__ == '__main__':
    main()
