import SocketServer
import threading
import Queue
from SeverIp.info import host, port
from urllib2 import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()

numberOfThreads = 3
studentNumber = "12302255"


# BaseServer.shutdown()
# BaseServer.server_close()

# BaseServer.request_queue_size
# RequestHandler.finish()
# RequestHandler.handle()
# RequestHandler.setup() does aby initializations before handle

# threading.active_count()
# threading.current_thread()
# threading.local() create thread local info data=threading.local()
#                                            data.x=1

# readline() call in the second handler will call recv() multiple times until it encounters a newline character,
# while the single recv() call in the first handler will just return what has been sent

class ThreadedTCPHandler(SocketServer.BaseRequestHandler):

    # def setup(self):
        # cur_thread = threading.currentThread()
        # fifo.put(cur_thread)


    def handle(self):
        # fifo._get()
        requestString = self.request.recv(1024)

        if requestString == "KILL_SERVICE\n":
            self.request.sendall("Service Killed")
            print ("Service killed by Client\n")
            ThreadedTCPServer.serverAlive = False
            server.shutdown()
            server.server_close()
            exit()


        if requestString == "HELO BASE_TEST\n":
            requestString = ("HELO BASE_TEST\nIP:{}\nPort:{}\nStudentID:{}\n".format(my_ip, port, studentNumber))

        self.request.sendall(requestString)

    #def finish(self):
        #fifo.task_done()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 10
    serverAlive = True
    pass

if __name__ == "__main__":
    server = SocketServer.TCPServer((host, port), ThreadedTCPHandler)
    ip, serverPort = server.server_address  # find out what port we were given
    print(ip)
    print(serverPort)
    # fifo = Queue.Queue(maxsize=10)

    try:
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        while(ThreadedTCPServer.serverAlive==True):
            x=1

    except KeyboardInterrupt:
        print("Key board interrupt \nServer Shutting Down")
        server.shutdown()
        server.server_close()
        exit()