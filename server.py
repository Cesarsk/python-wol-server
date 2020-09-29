from http.server import BaseHTTPRequestHandler, HTTPServer
from wol import WakeOnLan
import os
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    #intercept GET request
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    #intercept POST request
    def do_POST(self):
        # wake on lan has to go here.
        host = "myPC"
        mydir = os.path.dirname(os.path.abspath(__file__))
        wol = WakeOnLan(host,mydir)
        conf = wol.loadConfig()
        if host == 'myPC':
            if not wol.wake(): 
                    print('Host not found. Check .ini file')
            else: 
                    print('Magic packet sent')
        else: 
            print("Check host variable.")