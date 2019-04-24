import requests
import configparser
from flask import Flask, request, abort
import json
import urllib.parse as urlparse
import os
import psycopg2

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#db連線
url = urlparse.urlparse(os.environ['DATABASE_URL'])
db = "dbname=%s user=%s password=%s host=%s port=%s" % (url.path[1:], url.username, url.password, url.hostname, url.port)

conn = psycopg2.connect(db)
cur = conn.cursor()

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])

tw = {
    '北部': ['基隆市', '台北市', '新北市', '桃園縣', '新竹市', '新竹縣', '宜蘭縣'],
    '中部': ['苗栗縣', '台中市', '彰化縣', '南投縣', '雲林縣'],
    '南部': ['嘉義市', '嘉義縣', '台南市', '高雄市', '屏東縣', '澎湖縣'],
    '東部': ['台東縣', '花蓮縣'],
    '其他': ['金門縣', '連江縣']
}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

#查詢地區是否有廠商
def findArea(cityList):
    cityList = str(cityList).lstrip('[').rstrip(']')
    query = "SELECT city, count(*) from vendor where city in (" + cityList + ") group by city"
    cur.execute(query)
    result = cur.fetchall()

    return result

#讀取地區所擁有的廠商
def vendorInfo(city):
    query = "SELECT name, memo, img, link, line from vendor where city like '" + city + "%'"
    cur.execute(query)
    rows = cur.fetchall()

    textArray = []

    #旋轉木馬最多只能傳10個，如果超過要換另個寫法
    if (len(rows) > 1):
        for data in rows:
            textArray.append(
                CarouselColumn(
                    thumbnail_image_url = data[2],
                    title = data[0],
                    text = data[1],
                    actions = [
                        MessageTemplateAction(
                            label = '了解' + data[0],
                            text = '我想了解' + data[0]
                        ),
                        URITemplateAction(
                            label ='官方網站',
                            uri = data[3]
                        ),
                        URITemplateAction(
                            label ='加入line',
                            uri = data[4]
                        ),
                    ]
                ),
            )
            
        return TemplateSendMessage(alt_text = city, template = CarouselTemplate(columns = textArray))
    elif (len(rows) == 1):
        result = TemplateSendMessage(
            alt_text = city,
            template = ButtonsTemplate(
                thumbnail_image_url = rows[0][2],
                title = rows[0][0],
                text = rows[0][1],
                actions = [               
                    MessageTemplateAction(
                        label = '了解' + rows[0][0],
                        text = '我想了解' + rows[0][0]
                    ),
                    URITemplateAction(
                        label = '官方網站',
                        uri = rows[0][3]
                    ),
                    URITemplateAction(
                        label = '加入line',
                        uri = rows[0][4]
                    )        
                ]
            )
        )
        
        return result
    
    return TextMessage(text="此地方尚未有據點呦~")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):    
    print("使用者:"+event.source.user_id+" 傳來:"+event.message.text)

    #reply_message能回傳訊息最大數量為5，token只能使用一次
    fuck = event.message.text

    if fuck == "profile":
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text = 'Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text = 'Status message: ' + profile.status_message
                    ),
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))

    if "據點" in fuck:
        item = []
        for area in tw.keys():
            item.append(QuickReplyButton(action = MessageAction(label = area + '地區', text = area + '地區')),)

        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = '可以查看目前台灣與循環經濟有關的地方喔!(๑´ㅂ`๑)', quick_reply = QuickReply(items = item),
            )
        )

    for area in tw.keys():
        if area in fuck:
            cityCount = findArea(tw[area])
            
            item = []
            #如果縣市有廠商，則顯示
            for city in cityCount:
                if (city[1] > 0):
                    item.append(QuickReplyButton(action = MessageAction(label = city[0], text = city[0])),)
            
            #如果此地區無任何廠商，則顯示其他地區做為選項
            if (len(item) == 0):
                for areaOther in tw.keys():
                    if (areaOther != area):
                        item.append(QuickReplyButton(action = MessageAction(label = areaOther + '地區', text = areaOther + '地區')),)
                
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(
                            text='目前' + area +'沒有任何相關的據點呦(๑•́ ₃ •̀๑)'
                        ),
                        TextSendMessage(
                            text='可利用快速選項去查看別的地方呦(๑• ∀ •๑)σ', quick_reply = QuickReply(items = item),
                        ),
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [
                        TextSendMessage(
                            text='目前有顯示縣市有資訊喔ヽ(́◕◞౪◟◕‵)ﾉ' 
                        ),
                        TextSendMessage(
                            text='還不趕快點進去看ε٩(๑> ₃ <)۶з', quick_reply = QuickReply(items = item), 
                        ),
                    ]
                )

    
    modal = None
    
    #判斷是否有關鍵字是城市
    for area in tw.keys():
        for city in tw[area]:
            if city in fuck :
                modal = vendorInfo(city)

    #撈取城市相關廠商
    if (modal != None) :
        line_bot_api.reply_message(event.reply_token, modal)

    if "循環經濟" in fuck:
        buttons_template = TemplateSendMessage(
            alt_text='循環經濟 template',
            template=ButtonsTemplate(
                title='循環經濟理念',
                text='為您詳解何謂循環經濟',
                thumbnail_image_url='https://www.wealth.com.tw/files/d25b1c682936476f9a4f8942a9857e16.jpg',
                actions=[               
                    MessageTemplateAction(
                        label='一張圖看懂循環經濟',
                        text='送圖囉'
                    ),
                    MessageTemplateAction(
                        label='為什麼要有循環經濟?',
                        text='小循說故事'
                    ),
                    MessageTemplateAction(
                        label='循環經濟有啥原則?',
                        text='小循說原則'
                    )           
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='現在環境污染很嚴重咩 ( ´•̥×•̥` )'
                    ),
                    TextSendMessage(
                        text='所以才出現了循環經濟來幫助我們(๑• ∀ •๑)σ' 
                    ),
                    TextSendMessage(
                        text='可以點擊了解循環經濟到底是什麼呢ヽ(́◕◞౪◟◕‵)ﾉ' 
                    ),
                    buttons_template
                ]
        )
        
    if fuck == "送圖囉":
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='小循馬上為您送上一張看懂循環經濟'
                    ),
                    ImageSendMessage(
                        original_content_url='https://i.imgur.com/4nJJ1nv.jpg',
                        preview_image_url='https://i.imgur.com/4nJJ1nv.jpg'
                    ),
                    TextSendMessage(
                        text='從天下雜誌拿來哒ヽ(́◕◞౪◟◕‵)ﾉ' 
                    )
                ]
        )
    
    if fuck == "小循說故事":
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='好的好的~小循來說故事囉٩(๑•̀ω•́๑)۶'
                    ),
                    TextSendMessage(
                        text='小循知道現在地球很老惹\n然而人們一直耗資源製造東西丟東西(つд⊂)\n所以地球生氣惹ヽ(#`Д´)ﾉ' 
                    ),
                    TextSendMessage(
                        text='地球氣候愈來愈可怕了\n為了改善環境，循環經濟粗現了\n為您展示一下傳統的生產方式'
                    ),
                    ImageSendMessage(
                        original_content_url='https://i.imgur.com/1hMVlfd.jpg',
                        preview_image_url='https://i.imgur.com/1hMVlfd.jpg'
                    ),
                   TextSendMessage(
                        text='沒錯~傳統的就是生產後丟棄丟棄在丟棄\n每個階段都有廢棄物不斷產生',
                        quick_reply = QuickReply(items = 
                            [
                                QuickReplyButton(action = MessageAction(label = '繼續說', text = '[小循說故事]繼續說')),
                                QuickReplyButton(action = MessageAction(label = '不想聽了', text = '閉嘴')),
                            ]),
                    )
                ]
        )

    if fuck == "[小循說故事]繼續說":
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='再為您展示循環經濟的生產方式'
                    ),
                    ImageSendMessage(
                        original_content_url='https://i.imgur.com/nA5BVgf.jpg',
                        preview_image_url='https://i.imgur.com/nA5BVgf.jpg'
                    ),
                    TextSendMessage(
                        text='而循環經濟簡言而知就是所有東西可再利用\n完全大大減少廢棄物的產生' 
                    ),
                    TextSendMessage(
                        text='所以循環經濟不僅僅環保\n還可以減少消耗資源\n大大的減低成本呢!' 
                    ),
                    TextSendMessage(
                        text='是不是有理解了呢ヾ(*´∀ ˋ*)ﾉ',
                        quick_reply = QuickReply(items = 
                            [
                                QuickReplyButton(action = MessageAction(label = '沒有', text = '小循說故事')),
                                QuickReplyButton(action = MessageAction(label = '有', text = '閉嘴')),
                            ]),
                    )
                ]
        )
        
    if fuck == "小循說原則":
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='馬上為您奉上原則圖٩(๑•̀ω•́๑)۶'
                    ),
                    TextSendMessage(
                        text='從荷蘭來哒!' 
                    ),
                    ImageSendMessage(
                        original_content_url='https://i.imgur.com/Fs7pWmK.jpg',
                        preview_image_url='https://i.imgur.com/Fs7pWmK.jpg'
                    ),
                    TextSendMessage(
                        text='有興趣可以去訪問google大神呦( ´▽` )ﾉ' 
                    )
                ]
        )
        
    if fuck =="呼叫小循":
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='歡迎來到循跡點點',
                text='請選擇服務',
                thumbnail_image_url='https://i.imgur.com/NmV62Gs.jpg',
                actions=[
                    MessageTemplateAction(
                        label='關於循環經濟',
                        text='循環經濟'
                    ),
                    MessageTemplateAction(
                        label='哪裡有循環經濟的廠商呢',
                        text='據點查詢'
                    ),
                    URITemplateAction(
                        label='聯絡醜醜的負責人',
                        uri='https://www.facebook.com/profile.php?id=100000346362054'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='歡迎來到循跡點點ε٩(๑> ₃ <)۶з\n我是小循機器人٩(๑•̀ω•́๑)۶\n有什麼我可以為您服務的呢ヾ(*´∀ ˋ*)ﾉ'
                    ),
                    TextSendMessage(
                        text='請記得將Line大人更新到最新版本呦\n才不會錯過小循的高級功能'
                    ),
                    buttons_template
                ]
        )

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "小循不懂(〒︿〒)"))

    return 0

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    app.run()
