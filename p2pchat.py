#simple p2p chat application

#import need modules
import socket
import threading
import sys
import time
from random import randint

#create server class 
class Server:
    #create list of connections
    connections = []
    #create list of peers
    peers = []
    #run server side of chat
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #reuse server socket server
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)
        print("server running....")

        #connects server side of chat
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            #notify of new peers connecting
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1], "connected"))
            #update peer list with new connection
            self.sendPeers()

    #constructor and run function    
    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connections in self.connections:
                connection.send(bytes(data))
            if not data:
                print(str(a[0]) + ':' + str(a[1], "disconnected"))
                self.connections.remove(c)
                #notify of peer disconnection
                self.peers.remove(a[0])
                c.close()
                #update peer list of peer diconnection
                self.sendPeers()
                break
    #create send peers method        
    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","
        #send new peers list to all peers
        for connection in self.connections:
            connectiion.send(b'\x11' + bytes(p, "utf-8"))
        
#create client class     
class Client:
    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(""),'utf-8'))

    #runs client side of chat and connects 
    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #reuse client socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 10000))
        #pass to sendMsg function above
        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()
        
        #receive loop
        while True:
            data = sock.recv(1024)
            if not data:
                break
            #store peer list and update constantly
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))
                
    #create updatePeers function used above
    def updatePeers(self, peerData):
        #convert bytes to string
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]
        
#create p2p class to be accessed by client class and any outside class
class p2p:
    peers = ['127.0.0.1']

#turns client into server incase of server disconnection
while True:
    try:
        print("Trying to connect....")
        time.sleep(randint(1, 5))
        #loop through peers
        for peer in p2p.peers:
            try:
                client = Client(peer)
            #ctr + C to exit program
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            #created loop to prevent all systems from trying to become sever. Now only 1 in 20 chance
            if randint(1,20) == 1:
                #make client the server when no server connected
                try:
                    server = Server()
                #ctr + C to exit program
                except KeyboardInterrupt:
                    sys.exit(0)
                #print statement upon a connection not being established
                except:
                    print("Counldn't start the server...")
    
    #ctr + C to exit program
    except KeyboardInterrupt:
        sys.exit(0)
    

    





