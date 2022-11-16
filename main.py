from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import threading

def sendPeers(ip, server):
    with open('file.txt', 'r') as f:
        peers = f.read()

        server.connect((ip, 9999))
        server.send(peers.encode())

if __name__ == '__main__':
    PORT_NUMBER = 5000
    SIZE = 1024
    PORT_NUMBER_SEND_PEERS = 9999

    request_phrase = 'peers'.encode()
    hostName = gethostbyname( '192.168.0.123' )

    server = socket( AF_INET, SOCK_DGRAM )
    server.bind( (hostName, PORT_NUMBER) )

    print ("Test server listening on port {0}\n".format(PORT_NUMBER))
    
    while True:
        (data,addr) = server.recvfrom(SIZE)
        ip, port = addr
        print(addr)
        
        if data == request_phrase:
            thread = threading.Thread(target=sendPeers, args=(ip, server,))
            thread.start()
        f = open('file.txt', 'w')
        f.write(ip + '\n')
        f.close()
        