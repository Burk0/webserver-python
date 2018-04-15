#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

from Database import database
from Api import WebApi
from urllib.request import urlretrieve
from utils import SystemoveVolanie


class testHTTPServer_RequestHanlder(BaseHTTPRequestHandler):

    def do_GET(self):
        # print("ZACIATOK" + self.path)
        # db = database.Database
        if "/browse" in self.path:
            WebApi.browseApi(self)

        elif self.path.count('/') == 3:
            WebApi.shotApi(self,self.path)

        elif "/help" in self.path:
            print("vraciam help")
            return
        elif "?" in self.path:
            WebApi.parseParameters(self,self.path)







        # page = self.create_page()
        # if self.path.endswith("/browse"):




    def do_POST(self):
        print("POST:"+self.path)
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
