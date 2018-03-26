#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

from Database import database
from utils import SystemoveVolanie


class testHTTPServer_RequestHanlder(BaseHTTPRequestHandler):

    def do_GET(self):
        print("ZACIATOK" + self.path)
        db = database.Database
        # page = self.create_page()
        # if self.path.endswith("/browse"):
        if "/" == self.path:
            # print("tutu som " + self.path)
            self.send_page('Web/index2.html')

        elif self.path.endswith("/initData"):
            print("tu som"  + self.path)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # print(self.json_string)

            self.wfile.write(bytes(db.getInitData(db), "utf8"))

        elif  "/KameraDetail" in self.path :
            print("som v detaile  " + self.path)
            print(self.path.split("/")[2])
            id = self.path.split("/")[2]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            print(db.getCamDetail(db,id))
            self.wfile.write(bytes(db.getCamDetail(db,id), "utf8"))

        elif "/ViewDetail" in self.path:
            print("som v View detaile  " + self.path)
            id = self.path.split("/")[2]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # print(db.getCamDetail(db,id))
            self.wfile.write(bytes(db.getViewDetail(db, id), "utf8"))


        elif "/UsbCams" in self.path:
            print("vracima vsetky USBcamery")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # print(db.getCamDetail(db,id))
            self.wfile.write(bytes(SystemoveVolanie.getAllUsbCam(), "utf8"))



        elif "addCam" in self.path:
            print("pridanie novej kamery")
            #TODO zavolanie db a pozretie nazvu takej kamery, ak existuje nevlozist a vratit false
            #TODO ak neexistuje tak insert a vratit true a poslat spat na stranku


        elif "addView" in self.path:
            print("pridanie noveho nastavenia")
            # TODO zavolanie db a pozretie nazvu takej kamery, ak existuje nevlozist a vratit false
            # TODO ak neexistuje tak insert a vratit true a poslat spat na stranku
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
