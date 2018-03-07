#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

from Database import database
import Web


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
        print(self.path)
        # page = self.create_page()
        # if self.path.endswith("/browse"):
        if "/" in self.path:
            self.send_page('Web/index2.html')

        if self.path.endswith("/initData.json"):
            print("tu som"  + self.path)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # print(self.json_string)
            db = database.Database
            self.wfile.write(bytes(db.getInitData(db), "utf8"))
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
        # if self.path.endswith("/browse"):
        #     print(self.path)
        #     self.send_response(200)
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     # print(self.json_string)
        #     db = database.Database;
        #     self.wfile.write(bytes(db.getInitData(db), "utf8"))
        #     # database.getImageDetail(2)
        #     # print(db.getInitData(db))
        #     # print(db.getAllCams(db))
        # #     self.send_response(200)
        # elif "/detail/" in self.path:
        #     print("tu som " + self.path[8:])
        #     self.wfile.write(bytes(database.getDetail(9), "utf8"))
        #
        # elif "/addCam" in self.path:
        #     print(self.path)
        #     # content_length = int(self.headers['Content-Length'])
        #     # print(self.rfile.read(content_length))
        #     # form = cgi.FieldStorage()
        #     #
        #     # username = form.getvalue("username")
        #     #
        #     # print(username)
        #
        # elif "/addView" in self.path:
        #     print(self.path)
        #
        # else:
        #     print(self.path)

            # self.wfile.write(bytes("posielam novy json","utf8"))
    #     self.wfile.write(bytes("<html><body><h1>POST Request Received!</h1></body></html>","utf8"))



def run():
    print('starting server...')
    server_address = ('127.0.0.1', 8081)

    httpd = HTTPServer(server_address,testHTTPServer_RequestHanlder)
    print('running server...')
    httpd.serve_forever()
