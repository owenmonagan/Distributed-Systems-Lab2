import socket
from SeverIp.info import host,port

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
    client(host, port, "HELO BASE_TEST\n")
    client(host, port, "HELO BASE_TEST\n")
    client(host, port, "HELO BASE_TEST\n")
    client(host, port, "HELO BASE_TEST\n")
    client(host, port, "KILL_SERVICE\n")