import socketserver

class skelServer(socketserver.BaseRequestHandler):
    """Request handler for my server"""
    def handle(self):
        self.clientInfo= self.request.recv(1024).strip()
        print ("{} wrote:".format(self.client_address[0]))
        print (self.clientInfo.decode("ascii"))
        # just send back the same data, but upper-cased
        self.request.sendall(self.clientInfo.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), skelServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
