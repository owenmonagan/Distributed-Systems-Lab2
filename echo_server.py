import SocketServer
import threading
import sys
import os
import socket

numberOfThreads = 3
studentNumber = "8225096d25e2f49ea3efabe515fd9f58707934a0cb3a9494aea8d64ec363cd17"



if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


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



    def handle(self):

        client_connected=True
        while(client_connected==True):
            requestString = self.request.recv(1024)
            print("Client connected")

            if "KILL_SERVICE" in requestString:
                print ("Service killed by Client\n")
                client_connected=False
                ThreadedTCPServer.serverAlive = False


            elif "HELO" in requestString:
                print(requestString)
                lines=requestString.split()
                requestString = ("HELO {}\nIP:{}\nPort:{}\nStudentID:{}\n".format(lines[1], my_ip, p, studentNumber))
                self.request.sendall(requestString)
            else:
                print(requestString)





class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    request_queue_size = 10
    serverAlive = True
    allow_reuse_address = True
    pass

if __name__ == "__main__":
    my_ip = get_lan_ip()
    h, p = my_ip, int(sys.argv[1])
    print(my_ip)
    print(p)
    server = ThreadedTCPServer((h,p), ThreadedTCPHandler)


    try:
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        while(ThreadedTCPServer.serverAlive==True):
            x=1
        server.shutdown()
        server.server_close()
        exit()

    except KeyboardInterrupt:
        print("Key board interrupt \nServer Shutting Down")
        server.shutdown()
        server.server_close()
        exit()
