#! python3
# Defining a server for sending and receiving messages
# through network, applying 2 child-thread
import socket, sys, threading,time


PORT = 64164
HOST = '192.168.0.64'#socket.gethostname()

class ThreadClient(threading.Thread):
    """heritance of a thread-object to communicate with the client"""
    def __init__(self, conn, thname):
        threading.Thread.__init__(self, name=thname)
        self.conn = conn
    
    def run(self):
        global glob_ready
        #Communication with client
        name= self.getName()        # All threads have an ID
        while True:
            start=self.conn.recv(1).decode('UTF-8')
            if start!=chr(0):
                print("start:",start)
            else:
                msgClient=''
                while True:
                    curr=self.conn.recv(1).decode('UTF-8')
                    if curr==chr(0):break
                    msgClient+=curr
            try:
                print(msgClient)
                #msgClient=msgClient.decode('UTF-8')
            except Exception as e:
                print(e)
                print(msgClient)
            if msgClient=='#fin#' or msgClient=="":
                break
            if msgClient=='online.get':
                x=True
                locking.acquire()
                for client in conn_Cli:
                    if client!=name:
                        sendmsg(conn_Cli[name],bytes("SERVER>>> "+client+' online.', 'utf-8'))
                        x=False
                        time.sleep(0.5)
                if x: sendmsg(conn_Cli[name],bytes("SERVER>>> Currently you are the only one online", 'utf-8'))
                locking.release()
                continue
            if msgClient.startswith("#pic#"):
                glob_ready=False
                message= msgClient+"#pic#"+name
                print(message)
                locking.acquire()
                for client in conn_Cli:
                    if client!=name:
                        sendmsg(conn_Cli[client],bytes(message, 'utf-8'))
                img=b''
                a=0
                length=int(msgClient.split("#pic#")[1])
                #sendmsg(conn_Cli[name],bytes("#prog#"+str(len(str(length))), 'utf-8'))
                time.sleep(0.15)
                while a<length: 
                    msgImg=self.conn.recv(4096)
                    img+=msgImg
                    a+=len(msgImg)
                    for client in conn_Cli:
                        if client!=name:
                            conn_Cli[client].send(msgImg)
                    #sendmsg(conn_Cli[name],bytes("#prog#"+str(a),'utf-8'))
                locking.release()
                glob_ready=True
                continue
            # if msgClient.startswith("#LEN#"):
            #     locking.acquire()
            #     length=int(msgClient.split("#LEN#")[1])
            #     sendmsg(conn_Cli[name],bytes("#OK#"+"#END#",'utf-8'))
            #     msgClient=self.conn.recv(length).decode('utf-8')
            #     locking.release()
            if msgClient.startswith("#GAME#"):
                locking.acquire()
                for client in conn_Cli:
                    if client!=name:
                        sendmsg(conn_Cli[client],bytes(msgClient,'utf-8'))
                locking.release()
                continue
            message="%s> %s" % (name, msgClient)
            print(message)
            locking.acquire()
            for client in conn_Cli:
                if client!=name:
                    sendmsg(conn_Cli[client],bytes(message, 'utf-8'))
            locking.release()


        # Closing the connection 
        self.conn.close()           # Server side connection close
        locking.acquire()
        for client in conn_Cli:
            if client!=name:
                sendmsg(conn_Cli[client],bytes("SERVER>>> %s Lekapcsolódott."%name, 'utf-8'))
        locking.release()
        del conn_Cli[name]          # deleting reg from dictionary
        print("A kliens %s lekapcsolódott"%name)
        #End of thread


def sendmsg(conn,msg):
    conn.send(bytes(chr(0), 'utf-8'))
    conn.send(msg)
    conn.send(bytes(chr(0), 'utf-8'))

# Initializing server - creating socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("A socketet nem sikerült összekapcsolni a válaszott címmel.")
    time.sleep(2)
    sys.exit()
print("A server kész, várakozás a kérésekre...")
mySocket.listen()

# Managing connecting clients
conn_Cli={}
locking=threading.Lock()
glob_ready=True
while True:
    try:
        connec, addr = mySocket.accept()
        # Received a connection, initializing new thread
        name=connec.recv(1024).decode('UTF-8')
        if name in conn_Cli:
            name=name+'({0})'.format(addr[1])
        th= ThreadClient(connec,name)
        while not glob_ready:
            continue
        th.start()
        # Registering the connection
        it= th.getName()
        conn_Cli[it]=connec
        print("Kliens %s felkapcsolódott, IP cím %s, port %s." \
                                % (it, addr[0], addr[1]))
        connec.send(bytes(name, 'utf-8'))
        sendmsg(connec,bytes("SERVER>>> Successful connection, welcome, %s"%it, 'utf-8'))
        time.sleep(0.3)
        locking.acquire()
        for client in conn_Cli:
            if client!=name:
                sendmsg(conn_Cli[client], bytes("SERVER>>> Client %s connected to the server, IP cím %s, port %s." \
                                % (it, addr[0], addr[1]), 'utf-8'))
                sendmsg(conn_Cli[client],bytes("#PLAYER#%s"%name, 'utf-8'))
                sendmsg(connec,bytes("#PLAYER#%s"%client, 'utf-8'))
        locking.release()
    except Exception as e:
        print(e)
