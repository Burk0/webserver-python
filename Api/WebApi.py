from utils import SystemoveVolanie
from Database import database

def browseApi(handler):
    print("hehe "+handler.path)
    db = database.Database
    if "" == handler.path[7:]:
        handler.send_response(200)
        handler.send_header('Content-Type', 'text/html')
        handler.end_headers()
        page = 'Web/index2.html'
        file = open(page)
        # print(WebApi.apina(self.path[7:]))
        handler.wfile.write(bytes(file.read(), "utf8"))
        # print("tutu som " + path)

    # elif handler.path.endswith("/initData"):
    elif handler.path[7:] == "/initData":
        print("tu som"  + handler.path)
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        # print(json_string)
        # return db.getInitData(db)
        handler.wfile.write(bytes(db.getInitData(db), "utf8"))

    elif  "/KameraDetail" in handler.path :
        print("som v detaile  " + handler.path)
        print(handler.path.split("/")[3])
        id = handler.path.split("/")[3]

        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        # print(json_string)
        # return db.getInitData(db)
        handler.wfile.write(bytes(db.getCamDetail(db,id), "utf8"))

        # print(db.getCamDetail(db,id))
        # return db.getCamDetail(db,id)
        # wfile.write(bytes(db.getCamDetail(db,id), "utf8"))

    elif "/ViewDetail" in handler.path:
        print("som v View detaile  " + handler.path)
        id = handler.path.split("/")[3]
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        # print(json_string)
        # return db.getInitData(db)
        handler.wfile.write(bytes(db.getViewDetail(db, id), "utf8"))

        # print(db.getCamDetail(db,id))
        # wfile.write(bytes(db.getViewDetail(db, id), "utf8"))
        # return db.getViewDetail(db, id)


    elif "/UsbCams" in handler.path:
        print("vracima vsetky USBcamery")
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        # print(db.getCamDetail(db,id))
        # wfile.write(bytes(SystemoveVolanie.getAllUsbCam(), "utf8"))
        # return SystemoveVolanie.getAllUsbCam()
        handler.wfile.write(bytes(SystemoveVolanie.getAllUsbCam(), "utf8"))



    elif "addCam" in handler.path:
        print("pridanie novej kamery")
        #TODO zavolanie db a pozretie nazvu takej kamery, ak existuje nevlozit a vratit false
        #TODO ak neexistuje tak insert a vratit true a poslat spat na stranku

        # print(db.getCamDetail(db,id))
        # wfile.write(bytes(db.getIfNameExists(db), "utf8"))
        return db.getIfNameExists(db)


    elif "addView" in handler.path:
        print("pridanie noveho nastavenia")
        # TODO zavolanie db a pozretie nazvu takej kamery, ak existuje nevlozist a vratit false
        # TODO ak neexistuje tak insert a vratit true a poslat spat na stranku
    # elif path.endswith("/cams"):
    # #     print("ina stranka")
    #     send_page('addCamForm.html')
    # elif path.endswith("/views"):
    #     send_page('addViewForm.html')

    elif (handler.path.count('/') == 4):
        print("sem som sa dostal")
        shotApi(handler,handler.path[7:],True)



def shotApi(handler,path,browse=False):
    print("shotApi " + path)
    db = database.Database
    row = db.selectShotFromTable(db,path)
    #nenasiel som snimku
    if(row is None):
        print("None")
        handler.send_response(200)

        handler.send_header('Content-type', 'text/html')
        message = "Zadana snimka neexsituje"
        # a poslem tu spravu o tom
        handler.wfile.write(bytes(message, "utf8"))
    else:
        cesta,pozn,snimka_id,snimka,zmaz = row
        #mam taku snimku a je v pohode
        if(pozn=="Ok"):
            print("poznamka je ok")
            handler.send_response(200)

            # Send headers
            handler.send_header('Content-type', 'image/jpeg')
            handler.end_headers()
            file = open(cesta + '/' + snimka, 'rb')
            # file=open('test.png','rb')
            # vratim mu ju
            handler.wfile.write(file.read())
            file.close()

        else:
            print("poznamka je zla")
            handler.send_response(200)

            handler.send_header('Content-type', 'text/html')
            # poslem mu srpavu ze snimka bola zla
            handler.wfile.write(bytes(pozn, "utf8"))

        if(browse is False and zmaz is None):
            print("zmazanie snimky")


