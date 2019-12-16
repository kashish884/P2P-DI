
import os
import platform
import shlex
import time
import re
import socket
import threading

OS = platform.system()
HOST = socket.gethostbyname(socket.gethostname())
RFC_Server_Port = 40004
RFC_Fetching_List = [8130,8131]
FilePath = ''
cookieNumval = None
SERVER_NAME = '10.154.0.185'
SERVER_PORT = 65423


class Peer_Addition:  #To make an entry of the peer with below specified literals as its attributes

    def __init__(self, hostname, cookieNum, activeFlag, ttl, port, actvcnt, recentlyactv, next_entry=None):
        self.hostname = hostname
        self.cookieNum = cookieNum
        self.activeFlag = activeFlag
        self.TTL = int(ttl)
        self.list_port = int(port)
        self.ActvCnt = int(actvcnt)
        self.RecentlyActv = recentlyactv
        self.next_entry = next_entry

    def get_next(self):           #initialising getters and setters of all the attributes in class Peer_Addition
        return self.next_entry

    def get_hostname(self):
        return self.hostname

    def get_cookieNum(self):
        return self.cookieNum

    def get_activeFlag(self):
        return self.activeFlag

    def get_TTL(self):
        return self.TTL

    def get_list_port(self):
        return self.list_port

    def get_ActvCnt(self):
        return self.ActvCnt

    def get_RecentlyActv(self):
        return self.RecentlyActv

    def set_next(self, new_next):
        self.next_entry = new_next

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_list_port(self, port):
        self.list_port = port

    def set_cookieNum(self, cookieNumNo):
        self.cookieNum = cookieNumNo

    def set_activeFlag(self, activeFlag):
        self.activeFlag = activeFlag

    def set_TTL(self, ttl):
        self.TTL = ttl

    def set_ActvCnt(self):
        self.ActvCnt = actvcnt

    def set_RecentlyActv(self):
        self.RecentlyActv = recentlyactv


class Peer_Index():     #This object will be instantiated when a peer index gets updated or added or called to fetch a value(like port num)

    def __init__(self, head=None):
        self.head = head

    def get_head(self):
        return self.head

    def set_head(self, head):
        self.head = head

    def CreateEntry(self, hostname, cookieNum, activeFlag, ttl, port, actvcnt, recentlyactv):  #method to create an entry within a Peer_Index
        new_entry = Peer_Addition(hostname, cookieNum, activeFlag, ttl, port, actvcnt, recentlyactv)
        new_entry.set_next(self.head)
        self.head = new_entry

    def GetPort(self, hostname):  # Fetching the port number from the Peer Index
        current = self.head
        while current != None:
            if current.hostname == hostname:
                return current.get_list_port()
            current = current.get_next()
        print "ERROR! There is no port associated with %s\n" % (hostname)

    def Display(self):      		# To display the PI table
        current = self.head
        print "Peer-Index:--->"
        print "Hostname\tcookieNum\tActive Flag\tTTL\tListening Port\tRegistration count\tRecent Registration time\n"
        while current != None:
            print "%s\t%s\t%s\t%d\t%d\t\t%d\t\t%s" % (
            current.hostname, current.cookieNum, current.activeFlag, current.TTL, current.list_port, current.ActvCnt,
            current.RecentlyActv)
            current = current.next_entry


class RFC_Addition():    # Object to initialize RFC Entry

    def __init__(self, RFCno=0, RFCtitle='', hostname=socket.gethostbyname(socket.gethostname()), ttl=7200,
                 next_entry=None):
        self.RFCno = str(RFCno)
        self.RFCtitle = str(RFCtitle)
        self.hostname = str(hostname)
        self.TTL = int(ttl)
        self.next_entry = next_entry

    def get_next(self):
        return self.next_entry

    def get_RFCno(self):
        return self.RFCno

    def get_RFCtitle(self):
        return self.RFCtitle

    def get_hostname(self):
        return self.hostname

    def get_TTL(self):
        return self.TTL

    def set_next(self, new_next):
        self.next_entry = new_next

    def set_TTL(self, ttl):
        self.TTL = ttl


class RFC_Index():     #Object to create, update and search for an attribute within RFC_Index

    def __init__(self, head=None):
        self.head = head

    def get_head(self):
        return self.head

    def CreateEntry(self, RFCno, RFCtitle, hostname, ttl):
        new_entry = RFC_Addition(RFCno, RFCtitle, hostname, ttl)
        new_entry.set_next(self.head)
        self.head = new_entry

    def LocalRFC_Search(self, RFCno):  # B4 Initializing a contact with the RS for Active peer index doing self check for available RFC's
        global HOST
        current = self.head
        while current != None:
            if current.hostname == HOST:
                if current.RFCno == str(RFCno):
                    print "RFC %d is already present on the local system\n" % (RFCno)
                    return True
            current = current.next_entry
        print "Contacting RS server for obtaining RFC %d......\n" % (RFCno)
        return False

    def Check_DuplicateEntry(self, RFCno, hostname):  # To Check for duplicate entry before appending peer RFC Index to local Index
        current = self.head
        while current != None:
            if current.RFCno == str(RFCno) and current.hostname == hostname:
                return True
            else:
                current = current.next_entry
        return False

    def SearchRFC_Index(self, RFCno):  # To search the merged RFC-Index for the required RFC
        current = self.head
        status = False
        print "Searching Merged RFC-Index....\n"
        while current != None:
            if current.hostname != HOST:
                if current.RFCno == str(RFCno):
                    status = True
                    return (status, current.hostname)
            current = current.next_entry
        print " RFC %d is not found !\n" % (RFCno)
        return (status, None)

    def UpdateRFC_List(self):  # Update RFC Index local file list
        current = self.head
        entry = str(current.get_RFCno()) + "\t" + str(current.get_RFCtitle()) + "\t" + str(
            current.get_hostname()) + "\t" + str(current.get_TTL()) + "\n"
        return entry

    def display(self):
        current = self.head
        print "RFC-Index\n"
        while current != None:
            print "%s\t%s\t%s\t%d" % (current.RFCno, current.RFCtitle, current.hostname, current.TTL)
            current = current.next_entry

    def GenerateIndex_Response(self):  # To send across the whole RFC-Index
        global HOST
        global OS
        current = self.head
        message = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)" + HOST + "(%^&***)OS:(%^&***)" + OS
        print "P2P-DI/1.0 200 OK Host:" + HOST + "OS:" + OS
        while current != None:
            data = str(current.get_RFCno()) + '(%^&***)' + str(current.get_RFCtitle()) + '(%^&***)' + str(
                current.get_hostname()) + '(%^&***)' + str(current.get_TTL())
            message = message + "(%^&***)" + data
            print "...\n"
            current = current.next_entry
        return message


def Get_LocalFile_List():  # To obtain list of RFCs already present on localhost
    global FilePath
    files = []
    count = 0
    for file in os.listdir(FilePath):
        if file.startswith("8"):
            count += 1
            files.append(os.path.splitext(file)[0])
    return (files, count)


def Get_FileTitle():  # To obtain RFC titles of local RFCs
    global FilePath
    title = []
    start = 0
    end = 0
    for file in os.listdir(FilePath):
        if file.startswith("8"):
            f = open(file, "r")
            content = f.read()
            f.close()
            contents = str(content)
            c = re.split('(\W+)',contents)   #RE package is used to split the strings into individual part and then fetched to get the title of the RFC
            elem = 0
            count = 0
            for elem in c:
                if elem == "2017":
                    start = count
                    break
                count += 1
            elem = 0
            count = 0
            for elem in c:
                if elem == "Abstract":
                    end = count
                    break
                count += 1
            hd = ''
            for elem in range(start + 1, end):
                hd = hd + " " + c[elem]
            title.append(hd)
    return title


def ServerMain(socket, addr, object):   #Function implementing RFC Server functionalities like sending RFC index to RS 
    global FilePath
    global HOST
    global OS
    msg = socket.recv(1024)
    message = str.split(msg, "(%^&***)")
    if message[0] == 'GET':
        if message[1] == 'RFC-INDEX':
            print "Sending RFC-INDEX to %s.....\n" % (str(addr))
            response = object.GenerateIndex_Response()
            socket.send(response)
            print "Finished sending RFC-Index to %s\n" % (str(addr))
        elif message[1] == 'RFC':
            os.chdir(FilePath)  # Changes CWD to 'CWD\IP_Project'
            print "Sending RFC %s to %s......\n" % (message[2], str(addr))
            response = "P2P-DI/1.0(%^&***)200(%^&***)OK(%^&***)Host:(%^&***)" + HOST + "(%^&***)OS:(%^&***)" + OS
            print "P2P-DI/1.0 200 OK Host:" + HOST + "OS:" + OS
            filename = str(message[2]) + ".txt"
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    filedata = f.read()
                    response = response + "(%^&***)" + filedata
                    socket.send(response)
                print "Finished sending RFC %s to %s\n" % (message[2], str(addr))
    socket.close()


def ServerModule(object):   #Function implementing RFC Server socket attributes 
    global HOST
    global RFC_Server_Port
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, RFC_Server_Port))

    server_socket.listen(25)
    print "Starting server.....\n"
    while True:
        client_socket, addr = server_socket.accept()
        print "Connection from: " + str(addr)
        MainThread = threading.Thread(target=ServerMain, args=(client_socket, addr, object,))
        MainThread.start()


def Generate_KeepAlive():  #Function to implement KeepAlive message constantly after every 10 secs
    global SERVER_NAME
    global SERVER_PORT
    global HOST
    global OS
    global cookieNumval
    KAsock = socket.socket()
    KAsock.connect((SERVER_NAME, SERVER_PORT))

    while True:
        time.sleep(20)
        message = "KEEPALIVE(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)cookieNum:(%^&***)" + str(
            cookieNumval) + "(%^&***)OS:(%^&***)" + OS
        print "KEEPALIVE P2P-DI/1.0 Host:" + HOST + "cookieNum:" + str(cookieNumval) + "OS:" + OS
        print "\nKEEP ALIVE!!!!\n"
        KAsock.send(message)
    KAsock.close()


def Leave_Func():    #Function to implement leave functionality for peer from the Registration Server
    global SERVER_NAME
    global SERVER_PORT
    global HOST
    global OS
    global cookieNumval
    s = socket.socket()
    s.connect((SERVER_NAME, SERVER_PORT))
    message = "LEAVE(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)cookieNum:(%^&***)" + str(
        cookieNumval) + "(%^&***)OS:(%^&***)" + OS
    print "LEAVE P2P-DI/1.0 Host:" + HOST + "cookieNum:" + str(cookieNumval) + "OS:" + OS
    s.send(message)
    rep = s.recv(1024)
    reply = str.split(rep, "(%^&***)")
    if reply[1] == "200" and reply[2] == "OK":
        print "Leaving the P2P network"
    return message


def main():
    global SERVER_NAME
    global SERVER_PORT
    global HOST
    global RFC_Server_Port
    global OS
    global RFC_Fetching_List
    global FilePath
    global cookieNumval

    wd = os.getcwd()
    if OS == "Windows":
        directory = wd + "\IP_Project\Client"
    else:
        directory = wd + "/IP_Project"
    if not os.path.exists(directory):
        os.makedirs(directory)

    FilePath = directory
    os.chdir(FilePath)

    RFCtable = RFC_Index()
    Peertable = Peer_Index()

    f1 = open("RFC_Index.txt", "w+")
    f1.write("\nRFC NUMBER\tRFC TITLE\tHOSTNAME\tTTL\n")
    f1.close()

    s = socket.socket()
    s.connect((SERVER_NAME, SERVER_PORT))
    if os.path.isfile("cookieNum.txt"):
        with open("cookieNum.txt", "r") as f:
            cookieNumval = f.read()
    else:
        cookieNumval = None

    if cookieNumval != None:
        message = "REGISTER(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)cookieNum:(%^&***)" + str(
            cookieNumval) + "(%^&***)Port:(%^&***)" + str(RFC_Server_Port) + "(%^&***)OS:(%^&***)" + OS
        print "REGISTER P2P-DI/1.0 Host:" + HOST + "cookieNum:" + str(cookieNumval) + "Port:" + str(RFC_Server_Port) + "OS:" + OS
    else:
        message = "REGISTER(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)Port:(%^&***)" + str(
            RFC_Server_Port) + "(%^&***)OS:(%^&***)" + OS
    s.send(message)
    rep = s.recv(1024)
    reply = str.split(rep, "(%^&***)")
    if reply[1] == "200" and reply[2] == "OK":
        print "Peer %s registered with RS\n" % (str(s.getsockname()))
        cookieNumval = str(reply[4])
        s.close()
        f = open("cookieNum.txt", "w+")
        f.write(cookieNumval)
        f.close()
    Keep_AliveThread = threading.Thread(target=Generate_KeepAlive, args=())
    Keep_AliveThread.daemon = True
    Keep_AliveThread.start()

    (localfiles, count) = Get_LocalFile_List()
    if not localfiles:
        print "No RFCs on localhost\n"
    else:
        print 'RFCs on local system:\n'
        for i in localfiles:
            print i
        title = Get_FileTitle()
        print "Updating local RFCs to RFC-Index..\n"
        for idx in range(0, count):
            RFCtable.CreateEntry(localfiles[idx], title[idx], HOST, 7200)
            entry = RFCtable.UpdateRFC_List()
            os.chdir(FilePath)
            f = open("RFC_Index.txt", "a+")
            try:
                f.write(entry)
            finally:
                f.close()
    MainThread = threading.Thread(target=ServerModule, args=(RFCtable,))
    MainThread.start()
    time.sleep(20)
    start_time_cumulative = time.time()
    RFCtable.display()
    for RFCno in RFC_Fetching_List:
        status = RFCtable.LocalRFC_Search(RFCno)
        if status == False:
            start_time_each = time.time()
            s = socket.socket()
            s.connect((SERVER_NAME, SERVER_PORT))
            message = "GET(%^&***)PEER-INDEX(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)cookieNum:(%^&***)" + str(
                cookieNumval) + "(%^&***)OS:(%^&***)" + OS
            print "GET PEER-INDEX P2P-DI/1.0 Host:" + HOST + "cookieNum:" + str(cookieNumval) + "OS:" + OS
            print "Requesting Peer-Index from RS....\n"
            s.send(message)
            rep = s.recv(4096)
            reply = str.split(rep, "(%^&***)")
            if reply[1] == "200" and reply[2] == "OK":
                Peertable.set_head(None)  # To CHECK!!
                idx = 7
                while (idx < len(reply)):
                    Peertable.CreateEntry(reply[idx], reply[idx + 1], reply[idx + 2], reply[idx + 3], reply[idx + 4],
                                          reply[idx + 5], reply[idx + 6])
                    idx = idx + 7
                    print "...\n"
                print "Peer-Index successfully downloaded on %s\n" % (str(s.getsockname()))
            elif reply[1] == "404" and reply[2] == "ERROR":
                print "ERROR: %s!\n" % (str(reply[7]))
                Peertable.Display()
            s.close()

            current = Peertable.get_head()
            while current != None:
                if current.hostname != HOST:
                    peername = current.get_hostname()
                    peerport = current.get_list_port()
                    s = socket.socket()
                    s.connect((peername, peerport))
                    message = "GET(%^&***)RFC-INDEX(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)OS:(%^&***)" + OS
                    print "GET RFC-INDEX P2P-DI/1.0 Host:" + HOST + "OS:" + OS
                    print "Requesting RFC-Index from Peer %s:%s....\n" % (peername, str(peerport))
                    s.send(message)
                    rep = s.recv(4096)
                    reply = str.split(rep, "(%^&***)")
                    if reply[1] == "200" and reply[2] == "OK":
                        idx = 7
                        while (idx < len(reply)):
                            res = RFCtable.Check_DuplicateEntry(reply[idx], reply[idx + 2])
                            if res == False:
                                RFCtable.CreateEntry(reply[idx], reply[idx + 1], reply[idx + 2], reply[idx + 3])
                                entry = RFCtable.UpdateRFC_List()
                                os.chdir(FilePath)
                                f = open("RFC_Index.txt", "a+")
                                try:
                                    f.write(entry)
                                finally:
                                    f.close()
                            idx = idx + 4
                            print "...\n"
                        print "RFC-Index successfully downloaded on %s\n" % (str(s.getsockname()))
                    else:
                        print "ERROR while downloading RFC-Index from peer %s:%s\n" % (peername, str(peerport))
                    s.close()

                    (status, peername) = RFCtable.SearchRFC_Index(RFCno)
                    if status == True:
                        peerport = Peertable.GetPort(peername)
                        s = socket.socket()
                        s.connect((peername, peerport))
                        message = "GET(%^&***)RFC(%^&***)" + str(
                            RFCno) + "(%^&***)P2P-DI/1.0(%^&***)Host:(%^&***)" + HOST + "(%^&***)OS:(%^&***)" + OS
                        print "GET RFC" + str(RFCno) + "P2P-DI/1.0 Host:" + HOST + "OS:" + OS
                        print "Requesting RFC %d from peer %s:%s..\n" % (RFCno, peername, str(peerport))
                        s.send(message)
                        rep = s.recv(204800)
                        reply = str.split(rep, "(%^&***)")
                        if reply[1] == "200" and reply[2] == "OK":
                            idx = 7
                            filename = str(RFCno) + ".txt"
                            f = open(filename, "w+")
                            f.write(reply[7])
                            f.close()
                            end_time_each = time.time()
                            print "RFC %d successfully downloaded!\n" % (RFCno)
                            final_time_each = end_time_each - start_time_each
                            f = open("Timer.txt", "a+")
                            try:
                                f.write(
                                    "\nThe time taken for obtaining RFC " + str(RFCno) + ": " + str(final_time_each))
                            finally:
                                f.close()
                            s.close()
                            break
                        s.close()
                current = current.get_next()
            if current == None:
                print "RFC %d is not present with any peer\n" % (RFCno)

    end_time_cumulative = time.time()
    final_time_cumulative = end_time_cumulative - start_time_cumulative
    f = open("Timer.txt", "a+")
    try:
        f.write("\nThe cumulative time taken for obtaining all required RFCs: " + str(final_time_cumulative))
    finally:
        f.close()
    print "\nCompleted searching for all required RFCs\n"
    while True:
        userinput = raw_input("Leave or stay??\n")
        if userinput == "leave":
            LeaveSock = Leave_Func()
            break
        elif userinput == "stay":
            print "Waiting before closing server....\n"
            time.sleep(60)

    Keep_AliveThread.join()
    MainThread.join(10)
    LeaveSock.close()


if __name__ == '__main__':
    main()

