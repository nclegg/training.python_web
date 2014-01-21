import socket
import sys

def response_ok():
    parts = ['HTTP/1.1 200 OK',
             'Content-Type: text/plain',
             '',
             'this is a pretty minimal response']
    return '\r\n'.join(parts)

def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'

def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>log_buffer, "making a server on {0}:{1}".format(*address)
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>log_buffer, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
#            try:
#                print >>log_buffer, 'connection - {0}:{1}'.format(*addr)
#                while True:
#                    data = conn.recv(16)
#                    print >>log_buffer, 'received "{0}"'.format(data)
#                    if data:
#                        msg = 'sending data back to client'
#                        print >>log_buffer, msg
#                        conn.sendall(data)
#                    else:
#                        msg = 'no more data from {0}:{1}'.format(*addr)
#                        print >>log_buffer, msg
#                        break
#            finally:
#                conn.close()

            try:
                print >>log_buffer, 'connection - {0}{1}'.format(*addr)
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                parse_request(request)
                print >>log_buffer, 'sending response'
                response = response_ok()
                conn.sendall(response)
            finally:
                conn.close()
            
    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
