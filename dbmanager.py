import urllib.parse as urlparse
import os
import psycopg2

'''url = urlparse.urlparse(os.environ['DATABASE_URL'])
db = "dbname=%s user=%s password=%s host=%s port=%s" % (url.path[1:], url.username, url.password, url.hostname, url.port)
'''
db = "dbname=ddl3cfrqk7kmdq user=yerzjcmqnuvauv password=91aaea5b60b59e59c9be939e937ebb9f14ad0618c30ba98e10500490c9bb213b host=ec2-54-204-2-26.compute-1.amazonaws.com port=5432"
conn = psycopg2.connect(db)
cur = conn.cursor()


def DataInfo(con):
    query = "SELECT name,text,img,link,line from data where city = '"+con+"'"
    cur.execute(query)
    rows = cur.fetchall()
    text = []
    for i in rows:
        text.append(list(i))
    textArray = []
    if (len(text) < 5):
        for i in range(len(text)):
            textArray.append(
                    'CarouselColumn('+
                        'thumbnail_image_url = '+text[i][2]+','+
                        'title = '+text[i][0]+','
                        'text = '+text[i][1]+','
                        'actions=['+
                            'MessageTemplateAction('+
                            "label='了解'+"+text[i][0]+','+
                            "text='我想了解'+"+text[i][0]+
                        '),'+
                        'URITemplateAction('+
                            "label='官方網站',"+
                            'uri = '+text[i][3]+
                        '),'+
                        'URITemplateAction('+
                            "label='加入line',"+
                            'uri = '+text[i][4]+
                        ')'+
                        ']'+
                   '), '               
                    )
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