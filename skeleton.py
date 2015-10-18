import socketserver
import threading
import socket
import queue

maxWorkerThreads= 1



class skelServer(socketserver.BaseRequestHandler):
    """Request handler for my server"""
    def handle(self):
        fifo.put(self)
        print(fifo.qsize())
        item=fifo.get()
        cur_thread = threading.current_thread()
        resString= self.request.recv(1024).strip().decode("ascii")
        print(resString)


        if resString== "KILL_SERVICE":
            server.shutdown()
            server.server_close()

        elif resString=="HELO text":
            resString = ("{} Display server info:".format(self.client_address[0]))



        print (self.client_address[0])
        # just send back the same data, but upper-cased
        response = "{}: {}".format(cur_thread.name, resString.upper())
        print (response)
        self.request.sendall(response.encode("ascii"))
        fifo.task_done()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message.encode("ascii"))
        response = sock.recv(1024).decode("ascii")
        print ("Received: {}".format(response))
    finally:
        sock.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    #initialising queue 
    fifo=queue.Queue()
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


    print ("Server loop running in thread:", server_thread.name)
    i=0
    while i<1000:
        client(ip, port, "Hello World "+str(i))
        i+=1
    

    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")

    server.shutdown()
    server.server_close()






