#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import backend
import json
import cgi,cgitb


cgitb.enable() #for debugging

class testHTTPServer_RequestHanlder(BaseHTTPRequestHandler):
    # Page = open('index.html')
    # json_string = json.dumps(backend.getData())

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
        # page = self.create_page()
        # if self.path.endswith("/browse"):
        self.send_page('index2.html')
        # elif self.path.endswith("/cams"):
        # #     print("ina stranka")
        #     self.send_page('addCamForm.html')
        # elif self.path.endswith("/views"):
        #     self.send_page('addViewForm.html')



    def send_page(self,page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        # self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        file = open(page)
        self.wfile.write(bytes(file.read(),"utf8"))




    def do_POST(self):
        print(self.path)
        if self.path.endswith("/browse"):
            print(self.path)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # print(self.json_string)
            self.wfile.write(bytes(backend.getData(), "utf8"))
        #     self.send_response(200)
        elif "/detail/" in self.path:
            print("tu som " + self.path[8:])
            self.wfile.write(bytes(backend.getDetail(9), "utf8"))

        elif "/addCam" in self.path:
            print(self.path)
            # content_length = int(self.headers['Content-Length'])
            # print(self.rfile.read(content_length))
            # form = cgi.FieldStorage()
            #
            # username = form.getvalue("username")
            #
            # print(username)

        elif "/addView" in self.path:
            print(self.path)

        else:
            print(self.path)

            # self.wfile.write(bytes("posielam novy json","utf8"))
    #     self.wfile.write(bytes("<html><body><h1>POST Request Received!</h1></body></html>","utf8"))



def run():
    print('starting server...')
    server_address = ('127.0.0.1', 8081)

    httpd = HTTPServer(server_address,testHTTPServer_RequestHanlder)
    print('running server...')
    httpd.serve_forever()

run()