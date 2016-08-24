from http.server import BaseHTTPRequestHandler, HTTPServer 
import logging
import xml.dom.minidom
import socketserver
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig(filename='serverLog.log',format='%(levelname)s: %(asctime)s : %(message)s',level=logging.DEBUG) 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("dummy_server")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class MyHandler(BaseHTTPRequestHandler):
    concurrentConnection = None
    totalConnection = None
    
    def do_GET(self):
        print("Received a GET request")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<d><b><t>Title</t></b>")
        self.wfile.write(b"<a><c>This is a test.</c>")
        self.wfile.write(b"<c>You accessed path: %s</c>" % bytes(self.path,'utf_8'))
        self.wfile.write(b"</a></d>")
        return

    def do_POST(self):
        MyHandler.concurrentConnection += 1
        MyHandler.totalConnection = self.totalConnection + 1
        print("Received a POST request")
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)
        # self.log_request()
        try:
            xml_string = xml.dom.minidom.parseString(post_body)
            pretty_xml_as_string = xml_string.toprettyxml()
            print(pretty_xml_as_string)
            requests_log.info(pretty_xml_as_string)
        except xml.parsers.expat.ExpatError:
            print(post_body)
            requests_log.info(post_body)
        print('concurrentConnection : ' +  str(MyHandler.concurrentConnection))
        print('totalConnection : ' + str(MyHandler.totalConnection) )
        self.send_response(200)#, "<xml>Write what you want here...</xml>")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<xml>Write what you want here...</xml>")
        MyHandler.concurrentConnection -= 1
        return

    # def log_request(self, code=None, size=None):
    #     print('Request')

    # def log_message(self, format, *args):
    #     print('Message')

# def handler(*args):
#    MyHandler( *args)

if __name__ == "__main__":
    try:
        concurrentConnection = 0
        totalConnection = 0
        port = 8889
        MyHandler.concurrentConnection = concurrentConnection
        MyHandler.totalConnection = totalConnection
        server = HTTPServer(('localhost', port), MyHandler)
        print('Started http server at port no. ' + str(port))
        print('Url is http://localhost:' + str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()
