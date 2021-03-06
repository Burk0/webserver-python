#!/usr/bin/env python

import datetime
import json

import psycopg2
from Model import view, snimka, kamera, JsonData,JsonModel

connect_str = "dbname='BC_new' user='postgres' host='localhost' " + \
              "password='admin1234'"


class Database(object):
#listKamier je list kamier, ktory patri triede, z toho dovodu aby som nemusel robit dopyt do db kvoli zoznamu vsetkych kamier

    # def initDataFile(self):
    #     data_imgs = []
    #     data_cams = []
    #     data_views = []
    #     data_imgs.append(
    #         {'id': '2', 'nazov': 'nazov', 'poznamka':'pozn', 'Vytvorena': '12:03:2012',
    #          'kamera': 'kamera1', 'nastavenie': 'nastavenie'})
    #
    #     data_cams.append({'k_id': '3', 'k_nazov': 'kamera_nazov', 'k_typ': 'USB'})
    #
    #     data_views.append({'n_id': '4', 'n_nazov': 'nazov',
    #                            'n_kamera_meno': 'kamera1'})
    #
    #     oData = JsonData.JsonData(data_cams, data_views, data_imgs)
    #     print(json.dumps(oData.__dict__, default=self.myconverter))
    #     return json.dumps(oData.__dict__, default=self.myconverter)




    def getInitData(self):


        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        list=[]
        self.listKamier=[]
        listNastaveni=[]

        try:
            cursor.execute("select s.*,v.view_meno,k.kamera_meno from snimka s JOIN nastavenie v on V.view_id = S.view_id JOIN kamera k ON k.kamera_id = v.kamera_id")
            # print("ok")
            rows = cursor.fetchall()
            # print(len(rows))
            for r in rows:
                # print(r[0])
                list.append(snimka.Snimka(r[0], r[1], r[3], r[6], r[9],r[8],r[5]))


            cursor.execute("select * from kamera")
            rows=cursor.fetchall()
            for r in rows:
                self.listKamier.append(kamera.Kamera(r[0], r[1], r[2]))


            cursor.execute("select v.view_id,v.view_meno,k.kamera_meno from nastavenie v left join kamera k ON k.kamera_id = v.kamera_id")
            rows=cursor.fetchall()
            for r in rows:
                listNastaveni.append(view.View(r[0], r[1], r[2]))

            cursor.close()
            data_imgs = []
            data_cams = []
            data_views = []
            # data.append('snimka:')
            for i in range(len(list)):
                data_imgs.append({'id': list[i].id, 'nazov': list[i].nazov, 'poznamka': list[i].poznamka,
                                  'Vytvorena': list[i].vytvorena, 'kamera': list[i].meno_kamery,
                                  'nastavenie': list[i].meno_nastavenia,'previewUrl':list[i].url})

            listKamier = self.listKamier
            # data.append('kamera:')
            for i in range(len(listKamier)):
                data_cams.append({'k_id': listKamier[i].id, 'k_nazov': listKamier[i].nazov, 'k_typ': listKamier[i].typ})

            # data.append('nastavenie:')
            for i in range(len(listNastaveni)):
                data_views.append({'n_id': listNastaveni[i].id, 'n_nazov': listNastaveni[i].nazov,
                                   'n_kamera_meno': listNastaveni[i].kamera_meno})

            # data.__add__({'snimky':data_imgs})
            # data.append({'snimky':data_imgs})
            # data.append({'cams': data_cams})
            # data.append({'views':data_views})

            oData = JsonData.JsonData(data_cams, data_views, data_imgs)

            # sdata = str(data)
            # print(json.dumps(oData.__dict__,default=self.myconverter))
            return json.dumps(oData.__dict__, default=self.myconverter)
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
            return None

        # for r in list:
        #     print(str(list[0].id))
        # print(list)



    #Ziskanie detailu snimky z kamery
    #param id
    def getImageDetail(self,id):
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        data = []
        row = []
        try:
            cursor.execute(
                "select nazov,rozlisenie,cesta from snimka where snimka_id ='"+str(id)+"'")
            # print("ok")
            row = cursor.fetchone()


        except Exception as e:
                    print("Uh oh, can't connect. Invalid dbname, user or password?")
                    print(e)

        if(row is not None):
            data.append({'meno': row[0], 'rozlisenie': row[1], 'cesta': row[2]})
            odata = JsonModel.JsonModel(data)
            # print(json.dumps(data))
            return json.dumps(odata.__dict__)
        else:
            return None


    #ZIskanie detaily camery
    def getCamDetail(self,id):
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        try:
            cursor.execute(
                "select kamera_meno,kamera_typ,acc_meno,acc_heslo,ip,kamera_usb_desc from kamera where kamera_id ='"+str(id)+"'")
            # print("ok")
            row = cursor.fetchone()
        except Exception as e:
                    print("Uh oh, can't connect. Invalid dbname, user or password?")
                    print(e)

        if (row is not None):
            # data.append({'nazov': row[0],'typ': row[1], 'prihlasovacie_meno':row[2],'prihlasovacie_heslo':row[3],'ip':row[4],'descriptor':row[5]})

            # odata = JsonModel.JsonModel(data)
            # print(json.dumps(data))
            return json.dumps({'nazov': row[0],'typ': row[1], 'prihlasovacie_meno':row[2],'prihlasovacie_heslo':row[3],'ip':row[4],'descriptor':row[5]})
        else:
            return None


    #ZIskanie detaily nastavenia
    def getViewDetail(self,id):
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        try:
            cursor.execute(
                "select * from nastavenie where view_id ='"+str(id)+"'")
            # print("ok")
            row = cursor.fetchone()
        except Exception as e:
                    print("Uh oh, can't connect. Invalid dbname, user or password?")
                    print(e)
        # print(len(rows))
        if(row is not None):
            return json.dumps({'meno': row[1],'interval_medzi_fotkami': row[2], 'nova_fotka_pri_chybe':row[4],
                         'interval_mazania_fotky':row[6],'prz_motion_detektor':row[7],'cas_od':row[9],
                         'cas_do':row[10],'greyscale':row[11]}, default=self.myconverter)
        else:
            return None

    #metoda ktora mi vrati vsetky kamery v systeme
    def getIfNameExists(self):
        data = []
        data.append({'return' : 'true'})
        odata = JsonModel.JsonModel(data)
        print(json.dumps(data))
        return json.dumps(odata.__dict__, default=self.myconverter)


    def getAllCams(self):
        data=[]
        for i in range(len(self.listKamier)):
            data.append({'id':self.listKamier[i].id,'meno':self.listKamier[i].nazov})
        odata = JsonModel.JsonModel(data)
        return json.dumps(odata.__dict__, default=self.myconverter)


    #Converter casu
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()



    def selectShotFromTable(self,url):
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        try:
            cursor.execute(
                "select cesta,poznamka,snimka_id,nazov from snimka s JOIN nastavenie v ON s.view_id = v.view_id where url ='" + url+ "'")
            # print("ok")
            row = cursor.fetchone()
            cursor.close()
            return row
        except Exception as e:
                    print("selectShotFromTable:")
                    print(e)
                    cursor.close()


    def getCam(self,urlList):

        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        if urlList:
            querry = "select url from kamera k join nastavenie n on k.kamera_id= n.kamera_id join snimka s ON s.view_id =n.view_id where url !='null'"
        else:
            querry = "select kamera_meno from kamera"
        try:
            cursor.execute(
                querry)
            # print("ok")
            row = cursor.fetchall()
            cursor.close()

            odata = JsonModel.JsonModel(row)
            print("vypis", json.dumps({"zoznam": odata}, default=self.myconverter))
            return json.dumps({"zoznam": odata}, default=self.myconverter)
        except Exception as e:
            print("selectShotFromTable:")
            print(e)
            cursor.close()


    def getView(self,urlList,kamera):
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        if urlList:
            querry = "select url from kamera k join nastavenie n on k.kamera_id= n.kamera_id join snimka s ON s.view_id =n.view_id where url !='null' and " \
                     "k.kamera_meno = '"+str(kamera)+"'"
        else:
            querry = "select view_meno from kamera k join nastavenie n on k.kamera_id= n.kamera_id where kamera_meno = '"+str(kamera)+"'"
        try:
            cursor.execute(
                querry)
            # print("ok")
            row = cursor.fetchall()
            cursor.close()
            odata = JsonModel.JsonModel(row)
            print("vypis", json.dumps({"zoznam": odata}, default=self.myconverter))
            return json.dumps({"zoznam": odata}, default=self.myconverter)
        except Exception as e:
            print("selectShotFromTable:")
            print(e)
            cursor.close()



    def getShots(self,kamera,nastavenie,urlList,first,last,dateFrom,dateTo):

        print("====",dateTo)
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        where = ""
        limit = ""
        if first:
            limit = "order by vytvorena limit 1"
        elif last :
            limit = "order by vytvorena DESC limit 1"

        if dateFrom :
            print("tutu")
            if  dateTo:
                where = " and vytvorena >='" +str(dateFrom) + "' and vytvorena <='"+str(dateTo)+ "'"
            else:
                where = " and vytvorena >='" + str(dateFrom) + "'"
        elif  dateTo:
            where = " and vytvorena <='"+str(dateTo)+ "'"
        if urlList:
            querry = "select url from kamera k join nastavenie n on k.kamera_id= n.kamera_id join snimka s ON s.view_id =n.view_id where url !='null' and " \
                     "k.kamera_meno = '" + str(kamera) + "' and n.view_meno='"+str(nastavenie)+ "'"
        else:
            querry = "select s.nazov from kamera k join nastavenie n on k.kamera_id= n.kamera_id join snimka s ON s.view_id =n.view_id where url !='null' and " \
                     "k.kamera_meno = '" + str(kamera) + "' and n.view_meno='"+str(nastavenie)+ "'"
        try:
            cursor.execute(
                querry + where + limit)
            # print("ok")
            row = cursor.fetchall()
            cursor.close()
            odata = JsonModel.JsonModel(row)
            print("vypis", json.dumps({"zoznam": odata}, default=self.myconverter))
            return json.dumps({"zoznam": odata}, default=self.myconverter)
        except Exception as e:
            print("database.getShots:")
            print(e)
            cursor.close()



    def getShot(self,kamera, nastavenie,date):
        print("date: ",date)
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        # row = []

        try:
            cursor.execute("select cesta,nazov from snimka where url != 'null' ORDER BY abs(extract(epoch from (vytvorena - timestamp '"+str(date)+"'))) limit 1")
            # print("ok")
            row = cursor.fetchone()
            cursor.close()
            print("vypis", row)
            return row

        except Exception as e:
            print("getView:")
            print(e)
            cursor.close()


