import urllib.parse as urlparse
import os
import psycopg2

url = urlparse.urlparse(os.environ['DATABASE_URL'])
db = "dbname=%s user=%s password=%s host=%s port=%s" % (url.path[1:], url.username, url.password, url.hostname, url.port)
conn = psycopg2.connect(db)
cur = conn.cursor()


def DataInfo(con):
    query = "SELECT name,text,img,link,line from data where city = %s"
    cur.execute(query, (con,)) 
    rows = cur.fetchall()
    textArray=[]
    for (name,te,img,link,line) in rows:
        if (rows!= None):
            textArray.append(
                    CarouselColumn(
                        thumbnail_image_url = img,
                        title = name,
                        text = te,
                        actions=[
                            MessageTemplateAction(
                            label='了解'+name,
                            text='我想了解'+name,
                        ),
                        URITemplateAction(
                            label='官方網站',
                            uri = link
                        ),
                        URITemplateAction(
                            label='加入line',
                            uri = line
                        )
                        ]
                    ),                   
                    )
    return textArray

     
def selectData(text):
    query = "SELECT %s from data"
    cur.execute(query, (text,))
    rows = cur.fetchall()
    return rows