import SocketServer
import threading
import socket
import Queue
from random import randint

maxWorkerThreads= 2
studentNumber=1112221



class skelServer(SocketServer.BaseRequestHandler):
    #"""Request handler for my server"""
    def handle(self):
        fifo.put(self)
        #print(fifo.qsize())
        item=fifo.get()
        cur_thread = threading.current_thread()
        requestString= self.request.recv(1024)
        returnString=requestString
        #print(requestString)


        if requestString== "KILL_SERVICE\n":
            exit(0)

        elif requestString=="HELO BASE_TEST\n":
            returnString = ("HELO BASE_TEST\nIP:{}\nPort:{}\nStudentID:{}\n".format("134.226.32.10","3066",studentNumber))



        #print (self.client_address[0])
        # just send back the same data, but upper-cased
        #response = "{}: {}".format(cur_thread.name, resString.upper())
        #print (returnString)
        self.request.sendall(returnString)
        fifo.task_done()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print (response)
    finally:
        sock.close()



if __name__ == "__main__":
    #HOST, PORT = "localhost",5443
    HOST, PORT = "0.0.0.0", 3066

    #initialising queue 
    fifo=Queue.Queue()
    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), skelServer)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    for i in range(maxWorkerThreads):
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()




    fifo.join()


    #print ("Server loop running in thread:", server_thread.name)
    
    client(ip, port, "HELO text\n")
    client(ip, port, "HELO text\n")
    client(ip, port, "HELO text\n")
    client(ip, port, "HELO text\n")
    client(ip, port, "HELO text\n")

    val=True
    while(val==True):
        val==True
    #client(ip, port, "ANYTHING goes here\n")
    #client(ip, port, "KILL_SERVICE\n")

    
    #server.shutdown()
    #server.server_close()






