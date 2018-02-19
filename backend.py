#!/usr/bin/env python

import psycopg2
import snimka,kamera,view
import json
import datetime

def getData():
#     rows = [(298669, 'Disaster to Submarine Boat A.1 ', 74, 4, 1990, 'XVAJIbdRSKG385l8ZcTU2W0FIYp0FV27f50RPMlgUwbEwJV0xj9ROZEhBXDG0bocjCPTOSO8R9eqSjnjmtWGaRCIKzos02B9TTQt'),
# (298670, 'Disaster Town ', 156, 5, 1972, 'k6lsjiFpVxPfOJoe03YBdG3Pbfo4JYhy2Y9KlGeOn1bPklHCH6FjNHSW3sQULfbpbvfLgfQ0fmFMLHMdhFchRMWcZhGo7cgE0zrd'),
# (298671, 'Disaster Video ', 88, 3, 1996, '281QUgOkkaQVyqzePPK8XPSEp62Vj3u9j2BbDlFKDZcRXMOCRqTF0Y7rWSmkyY0hLZhXuDBHezyLVevvY92tVBMTfa2Dwi2NRu7G'),
# (298672, 'Disaster Wars: Earthquake vs. Tsunami ', 49, 3, 1946, 'GrSnhrFXg3j6sr7njztqCatafbjeScd5mwBEmbGkAXiDD0tPitFv42bpChqsgpjNYga1SVcrWmdPAiwfas027cf2gtPttMFnitLF'),
# (298673, 'Disaster Zone: Volcano in New York ', 94, 2, 1920, 'kdaDLFta8Lcu6Oh0glxiQOgzsrIGaypiubUCkgpxEsCntMlfMPfkeIBjnHaJu7OXCtF3csZgpDS58HopSYCweEd7V5CMwFG5Y97h'),
# (298674, 'Disaster! ', 100, 3, 1934, 'CjM7L510R7yoDVesSOtGdl1NrSGZUC7SLeOyvhOyquTrrHV5Krdh3qazVJXOfW2BqDAg75DgLeMPYJxquUV8LylzpBu7usOZgbMG'),
# (298675, 'Disaster! ', 110, 1, 1925, 'QFESULmUEDWSrHtsi0v1OfLMEXMOG59KxOKV68nULCR9b57oV8Ia3BJBqpjAOe3aE6TIbkoO5mOPJYLEJtTI6YyjEJZMeQvTt9LL'),
# (298676, 'Disaster! A Major Motion Picture Ride... Starring You! ', 195, 5, 1972, 'K8tdOTLmVbn1Exd8ffSiUoCInO5Y6ig0ZVDSNhDRVzBvFpoJ0naIwhvDP50m7sqpmzmGUOZOrMOBW08AXpdmFApobITLBIcW0vJ6'),
# (298677, 'Disaster: Day of Crisis ', 180, 5, 1941, 'B6bzAHw40XBJDZW7QsX9WCwpJKMObMv1Kbm95GMonmLjAKGn3CHEcN3IOXvrxq5en4UsHFQXfXjeXUGwukGz1ascoBfZxK8JNQD7'),
# (298678, 'Disaster: Death on Display ', 27, 1, 1920, 'iTU4TXYHLKUmT6iHZ88w9EeFYTStzM4MoAwtSCrdD15TENwyEPwVfiNPSazlVt5pyaawjGWThkYpGXVUTBI7GFmKM9Vme2s8I169'),
# (298679, 'Disaster: Twenty Twelve ', 182, 4, 1972, 'YIdXEJwEHzVto7wUYpjAg7spP9kyXvONJNVt1aQiBuRvdfpTXKhYdYV7IN5GzUHKD1uFOWZ3s62SHYcJUlwKn5YYWDQha4HaOqNK'),
# (298680, 'Disasterpiece ', 96, 5, 1995, '4HFMdt5tg8JPnMuDeZ7ZWWKkZP6YUiOGWG2hrCaD1aXfLppN0JEWQBrjmzMoLqzzStS6izcNKuT4MjPDkwq6palKt3DCYKz0in2o'),
# (298681, 'Disasterpieces ', 73, 4, 1941, '8RAm321fxiiiRIu7qwPWwcAevwZtu5WvDkQZNRcHbs74wzjoc8fMGD57ASviTlQdSSqtm0KLz7kgtOf7389caIcu96k8UbefLqDI'),
# (298682, 'Disasters of the Century ', 78, 1, 1956, 'TIdiYR0S2CUUi0NXjLg1PSWG7NCGX56bCMNkFTaGMPbM1Dd4dWAPWpNvCogNqV8lguPGdtQJHDqm3sNOnylM2Qp6sidZCOjJgeCv'),
# (298683, 'Disastro ', 86, 3, 1928, 'WSvJBMmdRnCVx2eRlvvFuYfs5H62MQimMMVyz1UHSo1pufkVjSHM9dNEwgw5WZIZ10uUyTWRitepSalXyyjWVhWa1NlNrpQkPg57'),
# (298684, 'DisAstro ', 53, 2, 1941, 'IZHeHm3Wm4qCLA6IY88eTzGJjYRQn0FljbY2eMqsIuCGYC8p58B3Sax03laqnEXs301R0iOoNBlSzcb0YriHMvKPDfQpjiDMPQ3w'),
# (298685, 'Disastro di Reggio e Messina ', 15, 5, 1999, 'RZ9pmE5NVPD5YlXDhIvwhrk8VlmNeGui77nDcwtuXOovma8E8VhoT0veHLTwVZO2Epxz3K8F2WBrC5zoXWUVTAVx4AEhXZNTIW11'),
# (298686, 'Disastro ferroviario a Montecchio ', 151, 2, 1973, '9MLezpOUhTkhWlIch2Q8RcEccH1wVTobMY1Sn6mYIFvsc00PeJZ78Mtt7rEQ3z1EZwfBjkMitjh9IvowENbsXflDiZN7knVUz,lBY'),
# (298687, 'Disastro ferroviario a Montecelio ', 121, 5, 1949, 'smMB1x1xGu6EgxDK6mKzJLHC7NH7aHkL2ZSwta1SadyefUwdangvhWSX6J9PRV4ndHgSDCDWfFXWaZ4ag0g2wtVTwOeSQF4iN4n7'),
# (298688, 'Disastrous Flirtation ', 86, 5, 1944, 'h24i3ArEvsyXOyyVSmryMRgnVGdwUYl5BT6lV3Zikb6gnpTe99nZ1i5rbrHBM7eRqVfl8jfdlQWn6fRJikSJc0ZFHn6UH1g1QKF3')]
    connect_str = "dbname='Bc_new' user='postgres' host='localhost' " + \
              "password='admin1234'"

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    list=[]
    listKamier=[]
    listNastaveni=[]

    try:
        cursor.execute("select * from snimka")
        # print("ok")
        rows = cursor.fetchall()
        # print(len(rows))
        for r in rows:
            # print(r[0])
            list.append(snimka.Snimka(r[0],r[1],r[3],r[6]))


        cursor.execute("select * from kamera")
        rows=cursor.fetchall()
        for r in rows:
            listKamier.append(kamera.Kamera(r[0],r[1],r[2]))


        cursor.execute("select v.view_id,v.view_meno,k.kamera_meno from view v join kamera k ON k.kamera_id = v.view_id")
        rows=cursor.fetchall()
        for r in rows:
            listNastaveni.append(view.View(r[0],r[1],r[2]))

        cursor.close()
    except Exception as e:
                print("Uh oh, can't connect. Invalid dbname, user or password?")
                print(e)

    # for r in list:
    #     print(str(list[0].id))
    # print(list)
    data = []
    # data.append('snimka:')
    for i in range(len(list)):
        data.append({'s_id':list[i].id,'s_nazov':list[i].nazov, 's_poznamka':list[i].poznamka, 's_Vytvorena':list[i].vytvorena})


    # data.append('kamera:')
    for i in range(len(listKamier)):
        data.append({'k_id': listKamier[i].id, 'k_nazov': listKamier[i].nazov, 'k_typ': listKamier[i].typ})


    # data.append('nastavenie:')
    for i in range(len(listNastaveni)):
        data.append({'n_id': listNastaveni[i].id, 'n_nazov': listNastaveni[i].nazov, 'n_kamera_meno': listNastaveni[i].kamera_meno})


    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    print(json.dumps(data, default=myconverter))

    return json.dumps(data,default=myconverter)


def getDetail(id):
    data = []
    data.append({'id': 8})

    return json.dumps(data)

# getData()