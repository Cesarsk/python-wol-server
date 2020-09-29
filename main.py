import logging
from server import S
from http.server import HTTPServer

# define port here
def run(server_class=HTTPServer, handler_class=S, port=7070):
    
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = ""
    try: 
        httpd = server_class(server_address, handler_class)
    except: 
        print("kill process with command: netstat -vanp tcp | grep ",port)
        print("kill process with command: sudo lsof -i tcp:",port)
    
    logging.info('Starting httpd...\n')
    try: 
        httpd.serve_forever()
    except KeyboardInterrupt: 
        pass
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    run()