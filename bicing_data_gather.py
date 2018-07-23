# -*- coding: utf-8 -*-
#import requests
import time
import urllib.request, urllib.parse, urllib.error
import json
import pymysql.cursors
import re
from datetime import datetime as dt, timedelta as td

def escriu_a_mysql(v2):
    #fem connexió
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='bicing',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            timeStp=v2['timestamp']

            timeStp=re.sub(r'(T)(.*)(\..*)',r' \2',timeStp)
                
            timeStp=dt.strptime(timeStp, "%Y-%m-%d %H:%M:%S")+td(hours=1)
            continue
            
            slots=(v2["empty_slots"]+v2["free_bikes"])

            #Inserir dades a la BD
            sql = "INSERT INTO bicing_tmp (uid, slots, empty_slots, bikes, status, timestamp) \
            VALUES (%s, %s, %s, %s, %s, %s)" 
            #executem SQL amb valors del camp "bicing"
            cursor.execute(sql, (v2["extra"]["uid"], slots, v2["empty_slots"], v2["free_bikes"], v2["extra"]["status"], timeStp))

        connection.commit()

    except Exception as e:
        print (e)

    finally:
        connection.close()

    return True

#def check(lstr,str_j):
#    if (lstr==str_j) or not internet_on():
#      time.sleep(60)

#App
def internet_on():
    try:
        urllib.request.urlopen('http://216.58.211.238', timeout=1)
        return True
    except urllib.request.URLError as err: 
        print(err)
        return False

#BICING
url= "http://api.citybik.es/v2/networks/bicing"

last_str_json = ""
cont=0
while True:
    origen_web = urllib.request.urlopen(url)
    # obtenim el darrer json de la web
    str_json = origen_web.read().decode()

    # si l'anterior json llegit és igual a l'acabat de llegir, voldrà dir que ja és a la BDD
    # esperem un minut i reiniciem el loop
    #check(last_str_json,str_json)
    if last_str_json==str_json:
        time.sleep(150)
        continue

    cont+=1
    print (cont)
    #print(cont + str(dt.now()))

    # actualizem "last_str_json" per al proper loop
    last_str_json = str_json
    
    #iniciem desat a base de dades
    try:
        current_dataset = json.loads(str_json)
        current_dataset=current_dataset['network']['stations']
    except Exception as e:
        current_dataset = None
        print(e)

    #si la comprobació es correcte, passar a l'acció
    if current_dataset != None:
        for element in current_dataset:

            escriu_a_mysql(element)