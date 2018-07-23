import urllib.request, urllib.parse, urllib.error
import json
import pymysql.cursors

def mysql_bicis(name,nameservice,nbikes,nstations,lat,lon):
    #fem connexió
    conn = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='bicing',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            print("%s,%s,%d,%d,%f,%f" % (name,nameservice,nbikes,nstations,lat,lon))
            sql = "INSERT INTO cities (name, serviceName, totalBikes, totalStations, latitude, longitude)"\
            " VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (name,nameservice,nbikes,nstations,lat,lon))

        conn.commit()

    except Exception as e:
        print (e)

    finally:
        conn.close()

    return True

llistaServeis=["bicing","bicimad","velib","santander-cycles","oslo-bysykkel","bikemi","villo","dublinbikes","wowcycle-reykjavik",\
"nextbike-malta"]

# recopilació dades diferents serveis de bici
for i in llistaServeis:
    url = "http://api.citybik.es/v2/networks/"+i

    origen_web = urllib.request.urlopen(url)
    js = origen_web.read().decode()
    wjdata = json.loads(js)

    city= wjdata['network']['location']['city']
    nameservice=wjdata['network']['id']

    try:
        latitude=float(wjdata['network']['location']['latitude'])
        longitude=float(wjdata['network']['location']['longitude'])
    except Exception as e:
        print (e)

    wjdata=wjdata['network']['stations']

    nBicis=0
    nStations=0
    for elm in wjdata:
        if (elm['empty_slots'] != None and elm['free_bikes'] != None):
            es=int(elm['empty_slots'])
            fb=int(elm['free_bikes'])
            nBicis+= int(es+fb)
        #nForaServei+= (elm['extra']['slots']-((elm['empty-slots'])+(elm['free_bikes'])))
        #nCirculant+= (elm['empty-slots'])
        nStations+= 1

    mysql_bicis(city,nameservice,nBicis,nStations,latitude,longitude)