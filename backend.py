#!/usr/bin/env python

import psycopg2

def getData():
    connect_str = "dbname='dbs_projekt' user='postgres' host='localhost' " + \
              "password='admin1234'"

    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    try:
        cursor.execute("select * from movies limit 10")
        print("ok")
        rows = cursor.fetchall()
        print(len(rows))
        for r in rows:
            print(r[0])

    except Exception as e:
                print("Uh oh, can't connect. Invalid dbname, user or password?")
                print(e)

    return rows

# getData()