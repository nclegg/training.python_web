import socket
import sys
import os 
import mimetypes



def response_ok(body, mimetype):
    """returns the HTTP resource and mime-type"""
    response = [ "HTTP/1.1 200 OK",
                 "Content-Type: %s"  % mimetype,
                 "",
                 body
               ]
    return "\r\n".join(response)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)

def response_not_found():
    """returns a 404 Not Found response"""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri


def resolve_uri(uri):
    home_dir = "webroot"

    # adjust domain root index
    uri = home_dir if uri == '/' else home_dir + uri

    if not os.path.exists(uri):
        raise ValueError("File not found")

    body = ""
    mimetype = ""

    if os.path.isdir(uri):
        mimetype = "text/plain"
        body = '\n'.join(os.listdir(uri))
    elif os.path.isfile(uri):
        mimetype = mimetypes.guess_type(uri)[0]
        body = open(uri, 'rb').read()
    return body, mimetype


def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break
                try:
                    uri = parse_request(request)
                    print >>sys.stderr, uri,  '****uri'
                    body, mimetype = resolve_uri(uri)
                    response = response_ok(body, mimetype)
                except NotImplementedError:
                    response = response_method_not_allowed()
                except ValueError:
                    response = response_not_found()

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()
            
    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
