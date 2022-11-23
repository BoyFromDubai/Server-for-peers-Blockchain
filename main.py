import socket
import threading
import re

class Server():
    def __init__(self):
        self.header_size = 64
        self.msg_type_size = 64
        self.listening_ip = self.__get_local_ip()
        self.listening_port = 5000
        self.clients_port = 9999

        self.peers_request = 'peers_request'
        self.decoding_format = 'utf-8'
        self.disconnect_message = 'DISCONNECTED'

        self.server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.server.bind( (self.listening_ip, self.listening_port) )

        self.__start_listening()
    
    def __handle_client(self, conn, addr):
        print(f'[NEW CONNECTION] {addr}')
        client_ip, port = addr
        connected = True
        while connected:
            msg_length = conn.recv(self.header_size).decode(self.decoding_format)
            if msg_length:
                msg_length = int(msg_length)
                print(msg_length)
                msg_type = conn.recv(msg_length)
                print(msg_type)

                if msg_type.decode(self.decoding_format) == 'peers_request':
                    sendig_peers_thread = threading.Thread(target=self.__send_peers, args=(client_ip,))
                    sendig_peers_thread.start()

                if msg_type.decode(self.decoding_format) == self.disconnect_message:
                    connected = False

        conn.close()

    def __start_listening(self):
        
        self.server.listen()

        while True:
            (conn, addr) = self.server.accept()
            ip, port = addr
            with open('file.txt', 'a+') as f:
                f.seek(0)
                line = '1'
                ip_exists = False
                
                while line:
                    line = f.readline()
                    if line[:-1] == str(ip):
                        ip_exists = True
                    f.seek(len(line))
                
                if not ip_exists:
                    f.write(ip + '\n')
            thread = threading.Thread(target=self.__handle_client, args=(conn, addr))
            thread.start()

    def __get_local_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:

            # Use Google Public DNS server to determine own IP
            sock.connect(('8.8.8.8', 80))

            return sock.getsockname()[0]
        except socket.error:
            try:
                return socket.gethostbyname(socket.gethostname()) 
            except socket.gaierror:
                return '127.0.0.1'
        finally:
            sock.close()

    def __send_peers(self, ip):
        with open('file.txt', 'r') as f:
            peers = f.read()
            print(peers)
            msg = peers.encode(self.decoding_format)
            msg_len = str(len(msg)).encode(self.decoding_format)
            msg_len += b' ' * (self.header_size - len(msg_len))
            msg_type = 'peers_answer'.encode(self.decoding_format)
            msg_type += b' ' * (self.msg_type_size - len(msg_type))

            sending_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sending_socket.connect((ip, self.clients_port))
            sending_socket.send(msg_len)
            sending_socket.send(msg_type)
            sending_socket.send(msg)

if __name__ == '__main__':
    server = Server()

# if __name__ == '__main__':
#     PORT_NUMBER = 5000
#     SIZE = 1024
#     PORT_NUMBER_SEND_PEERS = 9999

#     request_phrase = 'peers'.encode()
#     hostName = gethostbyname( '192.168.0.140' )

#     server = socket( AF_INET, SOCK_DGRAM )
#     server.bind( (hostName, PORT_NUMBER) )

#     print ("Test server listening on port {0}\n".format(PORT_NUMBER))
    
#     while True:
#         (data, addr) = server.recvfrom(SIZE)
#         ip, port = addr
#         print(addr)
        
#         if data == request_phrase:
#             thread = threading.Thread(target=sendPeers, args=(ip, server,))
#             thread.start()
#         f = open('file.txt', 'w')
#         f.write(ip + '\n')
#         f.close()
        