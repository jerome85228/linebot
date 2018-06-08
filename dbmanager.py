import urllib.parse as urlparse
import os
import psycopg2

url = urlparse.urlparse(os.environ['DATABASE_URL'])
db = "dbname=%s user=%s password=%s host=%s port=%s" % (url.path[1:], url.username, url.password, url.hostname, url.port)
conn = psycopg2.connect(db)
cur = conn.cursor()


def DataInfo(con):
    query = "SELECT name,text,img,link,line from data where city = '"+con+"'"
    cur.execute(query)
    rows = cur.fetchall()
    textArray=[]
    for i in rows:
        for j in i:
            textArray.append(j)
            
    return textArray

     
def selectData(text):
    query = "SELECT "+text+" from data"
    cur.execute(query)
    rows = cur.fetchall()
    text=[]
    for i in rows:
        for j in i:
            text.append(j)            
    return text
    
print(selectData('city'))
print(DataInfo('雲林縣'))