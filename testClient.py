import socket
import sys

HOST, PORT = "localhost", 9001
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(b"HELO text\\n")

    # Receive data from the server and shut down
    received = sock.recv(1024).decode("ascii")
finally:
    sock.close()
print(received)
print ("Sent:     {}".format(data))
print ("Received: {}".format(received))