import socket
import sys


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP) 


    # allow imediate socket re-use http://docs.python.org/2/library/socket.html
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # log that we are building a server
    print >>log_buffer, "making a server on {0}:{1}".format(*address)
    
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>log_buffer, 'waiting for a connection'

            conn, addr = sock.accept()

            try:
                print >>log_buffer, 'connection - {0}:{1}'.format(*addr)

                while True:
                    data = conn.recv(16)
                    print >>log_buffer, 'received "{0}"'.format(data)
           
                    if not data:
                        break
                    conn.sendall(data)

            finally:
                conn.close()
                print >>log_buffer, 'closing socket'
            
    except KeyboardInterrupt:
        sock.close()
        print >>log_buffer, 'connection closed'


if __name__ == '__main__':
    server()
    sys.exit(0)
