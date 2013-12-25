#SERVER IMPORTS
import threading
import webbrowser
import http.server
import socketserver
import sys
#CAS IMPORTS
sys.path.insert(0, 'Data/')
import textparser as cas

FILE = 'frontend.html'
PORT = 8080
def post_simplify(str):
    exp=cas.TextToCAS(str)
    result=exp.simplify("ThisIsForTheLatexCompiler",2)
    if type(result)==type(cas.TextToCAS("a")):
        result=[result.tolatex()]
    retval="SIMPL#"+exp.tolatex()
    for n in result:
        retval+=r"#\("+n+r"\)"
    return retval
def post_solve(str):
    
    return "SOLVE"
def byting(str):

    return bytes(str,"utf-8")
class TestHandler(http.server.SimpleHTTPRequestHandler):
    """The test example handler."""
    def do_POST(self):
        length = int(self.headers.get_all('Content-Length')[0])  
        data_string = self.rfile.read(length).decode('utf-8')
        print("RECEIVED STRING   :", data_string)

        if data_string[:10]=="#SAFEVAL1#":
            result=byting(post_simplify(data_string[10:]))
        elif data_string[:10]=="#SAFEVAL2#":
            result=byting(post_solve(data_string[10:]))
        else:
            result=byting("error")
        #except:
         #   result=byting("error")
        self.wfile.write(result)

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()
def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = http.server.HTTPServer(server_address, TestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
if __name__ == "__main__":
    open_browser()
    start_server()
