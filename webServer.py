#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import backend
import cgi

class testHTTPServer_RequestHanlder(BaseHTTPRequestHandler):
    Page = open('index.html')
    # Page = '''\
    # <html>
    # <body>
    # <table>
    # <tr>  <td>Header</td>         <td>Value</td>          </tr>
    # <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
    # <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
    # <tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
    # <tr>  <td>Command</td>        <td>{command}</td>      </tr>
    # <tr>  <td>Path</td>           <td>{path}</td>         </tr>
    # </table>
    # </body>
    # </html>
    # '''
    # def do_GET(self):
    #     self.send_response(200)
    #
    #     self.send_header('Content-type','text/html')
    #     self.end_headers()
    #     self.wfile.write(bytes('{"status" : "ready"}',"utf8"))
    #
    #     message = "Hello world"
    #     file = open('index.html')
    #     self.wfile.write(bytes(file.read(),"utf8"))
    #     file.close()

    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path,
            'list': backend.getData(),
            'lenght' : len(backend.getData())
        }
        page = self.Page.read().format(**values)
        return page

    def send_page(self,page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(bytes(page,"utf8"))


    def do_POST(self):
        self.send_response(200)
        # self.send_response(301)
        # self.send_header('Location','/snimka')
        # self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        print ("lal:" +form.getvalue("foo"))
        self.wfile.write(bytes("<html><body><h1>POST Request Received!</h1></body></html>","utf8"))



def run():
    print('starting server...')
    server_address = ('127.0.0.1', 8081)

    httpd = HTTPServer(server_address,testHTTPServer_RequestHanlder)
    print('running server...')
    httpd.serve_forever()

run()