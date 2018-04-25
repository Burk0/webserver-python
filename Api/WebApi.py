import json
from _ast import UAdd

from Model import JsonModel
from utils import Utils
from Database import database
import urllib
from io import BytesIO

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
        handler.send_header('Access-Control-Allow-Origin', '*')

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
        handler.send_header('Access-Control-Allow-Origin', '*')
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
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.end_headers()
        # print(db.getCamDetail(db,id))
        # wfile.write(bytes(SystemoveVolanie.getAllUsbCam(), "utf8"))
        # return SystemoveVolanie.getAllUsbCam()
        handler.wfile.write(bytes(Utils.getAllUsbCam(), "utf8"))



    elif "AddCam" in handler.path:
        print("pridanie novej kamery")
        #TODO zavolanie db a pozretie nazvu takej kamery, ak existuje nevlozit a vratit false
        #TODO ak neexistuje tak insert a vratit true a poslat spat na stranku
        params = urllib.parse.parse_qs(handler.path[15:])
        print("params",params.get("actualId"))
        # print(db.getCamDetail(db,id))
        # wfile.write(bytes(db.getIfNameExists(db), "utf8"))
        # return db.getIfNameExists(db)


    elif "AddView" in handler.path:
        print("pridanie noveho nastavenia")
        # TODO zavolanie db a pozretie nazvu takej kamery, ak existuje nevlozist a vratit false
        # TODO ak neexistuje tak insert a vratit true a poslat spat na stranku
        print(urllib.parse.parse_qs(handler.path[15:]))
    # elif path.endswith("/cams"):
    # #     print("ina stranka")
    #     send_page('addCamForm.html')
    # elif path.endswith("/views"):
    #     send_page('addViewForm.html')

    elif (handler.path.count('/') == 4):
        print("sem som sa dostal")
        shotApi(handler,handler.path[7:],True)

    elif "/testCam" in handler.path:
        print("TestCam")

        params = urllib.parse.parse_qs(handler.path[16:])
        usbdesc = params.get("usbList").pop(0)
        file = Utils.getTestCam(usbdesc)
        handler.send_response(200)
        if file is not None:
            print("_____________________")
            handler.send_header('Content-type', 'image/jpeg')
            handler.send_header('Access-Control-Allow-Origin', '*')
            handler.end_headers()
            handler.wfile.write(file.read())
            file.close()
        else :
            handler.send_header('Content-type', 'text/html')
            handler.send_header('Access-Control-Allow-Origin', '*')
            handler.end_headers()
            handler.wfile.write(bytes("chyba", "utf8"))
        # print(db.getCamDetail(db,id))
        # wfile.write(bytes(SystemoveVolanie.getAllUsbCam(), "utf8"))
        # return SystemoveVolanie.getAllUsbCam()
        # file = open("/home/buranskyd/BC/moja prva USB kamera/moj motion4/22-04-18" + '/' + "22042018_181424.png", 'rb')
        # file=open('test.png','rb')
        # vratim mu ju


        # file.close()




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
        cesta,pozn,snimka_id,snimka = row
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


def parseParameters(handler):



    db = database.Database
    params = urllib.parse.parse_qs(handler.path[2:])
    akcia = ""
    first = False
    last = False
    dateFrom = ""
    dateTo = ""
    urlList = False
    # print(params)

    if params.get("first") is not None :
        first = True
    if params.get("last") is not None :
        last = True
    if params.get("dateFrom") is not None :
        dateFrom = params.get("dateFrom").pop(0)
    if params.get("dateTo") is not None :
        dateTo = params.get("dateTo").pop(0)
    if params.get("urlList") is not None :
        urlList = True
    if params.get("action") is not None :
        akcia = params.get("action").pop(0)
    if akcia == "getCam":
        print("getCamaaaa")
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.end_headers()

        handler.wfile.write(bytes(db.getCam(db,urlList), "utf8"))
    elif akcia == "getView":
        if params.get("camera"):
            kamera =params.get("camera").pop(0)

            handler.send_response(200)
            handler.send_header('Content-Type', 'application/json')
            handler.send_header('Access-Control-Allow-Origin', '*')
            handler.end_headers()

            handler.wfile.write(bytes(db.getView(db,urlList,kamera), "utf8"))

    elif akcia == "getShots":
        if params.get("camera"):
            kamera =params.get("camera").pop(0)
            if params.get("view"):
                nastavenie = params.get("view").pop(0)

                handler.send_response(200)
                handler.send_header('Content-Type', 'application/json')
                handler.send_header('Access-Control-Allow-Origin', '*')
                handler.end_headers()

                handler.wfile.write(bytes(db.getShots(db,kamera,nastavenie,urlList,first,last,dateFrom,dateTo), "utf8"))


    elif akcia == "getShot":
        if params.get("camera"):
            kamera = params.get("camera").pop(0)
            if params.get("view"):
                nastavenie = params.get("view").pop(0)
                if params.get("date"):
                    date = params.get("date").pop(0)
                    print(date)
                    ret = db.getShot(db, kamera, nastavenie, date)
                    if ret is None:
                        handler.send_response(200)
                        handler.send_header('Content-Type', 'application/json')
                        data = []
                        data.append({'error': 'nenasla sa ziadna snimka'})
                        odata = JsonModel.JsonModel(data)
                        print("vypis", json.dumps({"zoznam": odata}))
                        return json.dumps({"zoznam": odata})
                        # a poslem tu spravu o tom
                        handler.wfile.write(bytes(message, "utf8"))

                    else:
                        cesta,snimka = ret
                        handler.send_response(200)
                        handler.send_header('Content-type', 'image/jpeg')
                        handler.end_headers()
                        file = open(cesta+'/'+snimka, 'rb')
                        # file=open('test.png','rb')
                        # vratim mu ju
                        handler.wfile.write(file.read())
                        file.close()

                    # handler.send_response(200)
                    # handler.send_header('Content-type', 'image/jpeg')
                    # handler.send_header('Access-Control-Allow-Origin', '*')
                    # handler.end_headers()
                    #
                    # handler.wfile.write(
                    #     bytes(db.getShot(db, kamera, nastavenie,date), "utf8"))







    print(akcia)
    print(urlList)




    # handler.wfile.write(bytes(db.getViewDetail(db, id), "utf8"))
