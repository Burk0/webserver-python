#!/usr/bin/env python

import datetime
import json

import psycopg2
from Model import view,snimka,kamera

connect_str = "dbname='Bc_new' user='postgres' host='localhost' " + \
              "password='admin1234'"


class Database(object):
#listKamier je list kamier, ktory patri triede, z toho dovodu aby som nemusel robit dopyt do db kvoli zoznamu vsetkych kamier


    def getInitData(self):


        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        list=[]
        self.listKamier=[]
        listNastaveni=[]

        try:
            cursor.execute("select s.*,v.view_meno,k.kamera_meno from snimka s JOIN view v on V.view_id = S.view_id JOIN kamera k ON k.kamera_id = v.kamera_id")
            # print("ok")
            rows = cursor.fetchall()
            # print(len(rows))
            for r in rows:
                # print(r[0])
                list.append(snimka.Snimka(r[0], r[1], r[3], r[6], r[7],r[8]))


            cursor.execute("select * from kamera")
            rows=cursor.fetchall()
            for r in rows:
                self.listKamier.append(kamera.Kamera(r[0], r[1], r[2]))


            cursor.execute("select v.view_id,v.view_meno,k.kamera_meno from view v join kamera k ON k.kamera_id = v.view_id")
            rows=cursor.fetchall()
            for r in rows:
                listNastaveni.append(view.View(r[0], r[1], r[2]))

            cursor.close()
        except Exception as e:
                    print("Uh oh, can't connect. Invalid dbname, user or password?")
                    print(e)

        # for r in list:
        #     print(str(list[0].id))
        # print(list)
        data = []
        data_imgs = []
        data_cams = []
        data_views = []
        # data.append('snimka:')
        for i in range(len(list)):
            data_imgs.append({'id':list[i].id,'nazov':list[i].nazov, 'poznamka':list[i].poznamka, 'Vytvorena':list[i].vytvorena,'kamera':list[i].meno_kamery,'nastavenie':list[i].meno_nastavenia})

        listKamier=self.listKamier
        # data.append('kamera:')
        for i in range(len(listKamier)):
            data_cams.append({'k_id': listKamier[i].id, 'k_nazov': listKamier[i].nazov, 'k_typ': listKamier[i].typ})


        # data.append('nastavenie:')
        for i in range(len(listNastaveni)):
            data_views.append({'n_id': listNastaveni[i].id, 'n_nazov': listNastaveni[i].nazov, 'n_kamera_meno': listNastaveni[i].kamera_meno})


        data.append({'snimky':data_imgs})
        data.append({'cams': data_cams})
        data.append({'views':data_views})


        # print(json.dumps(data, default=myconverter))

        return json.dumps(data,default=self.myconverter)


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
            # print(json.dumps(data))
            return json.dumps(data)
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

        data = []
        if (row is not None):
            data.append({'meno': row[0],'typ': row[1], 'prihlasovacie_meno':row[2],'prihlasovacie_heslo':row[3],'ip':row[4],'descriptor':row[5]})

        # print(json.dumps(data))
            return json.dumps(data)
        else:
            return None


    #ZIskanie detaily nastavenia
    def getViewDetail(self,id):
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        row = []
        try:
            cursor.execute(
                "select * from view where view_id ='"+str(id)+"'")
            # print("ok")
            row = cursor.fetchone()
        except Exception as e:
                    print("Uh oh, can't connect. Invalid dbname, user or password?")
                    print(e)
        # print(len(rows))
        data = []
        if(row is not None):
            data.append({'meno': row[1],'interval_medzi_fotkami': row[2], 'nova_fotka_pri_chybe':row[4],
                         'interval_mazania_fotky':row[6],'prz_motion_detektor':row[7],'cas_od':row[9],
                         'cas_do':row[10],'greyscale':row[11]})

            print(json.dumps(data, default=self.myconverter))
            return json.dumps(data, default=self.myconverter)
        else:
            return None

    #metoda ktora mi vrati vsetky kamery v systeme
    def getAllCams(self):
        data = []
        data.append({'return' : 0})
        return json.dumps(data)
        # for i in range(len(self.listKamier)):
        #     data.append({'id':self.listKamier[i].id,'meno':self.listKamier[i].nazov})
        # return json.dumps(data)



    #Converter casu
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
