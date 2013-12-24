import threading
import webbrowser
import http.server
#import SimpleHTTPServer

FILE = 'frontend.html'
PORT = 8080


class TestHandler(http.server.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.getheader('content-length'))        
        data_string = self.rfile.read(length)
        try:
            result = r"\(\sin^2\theta+\cos^2\theta=1\)"
        except:
            result = 'error'
        self.wfile.write(result)


def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()
def start_server(server_class=http.server.HTTPServer):
#def start_server():
    server_address = ('', PORT)
    httpd = server_class(server_address, TestHandler)
    httpd.serve_forever()
"""def start_server():
    #Start the server
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()"""

if __name__ == "__main__":
    open_browser()
    start_server()