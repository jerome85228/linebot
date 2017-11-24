import requests
import re
import configparser
from flask import Flask, request, abort
import mysql.connector
from mysql.connector import errorcode

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])


#connect db
cnx = mysql.connector.connect(user='lifecity', password='a123456789',
                              host='140.125.81.1',
                              database='對話',
                              charset="utf8")
cursor = cnx.cursor()



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

def find(i):   
    query = ('SELECT 關鍵字 FROM 對話.傳來 '
                'WHERE id傳來 = %s')
    cursor.execute(query, (i+1,))
    for row in cursor:
        return row[0]
print(find(1))

def reply(word):
    query = ('SELECT 回覆1, 回覆2, 回覆3, 回覆4, 回覆5 FROM 對話.傳來 '
                'WHERE 關鍵字 = %s')
    cursor.execute(query, (word,))
    row = cursor.fetchone()
    textArray=[]
    for i in range (5):
        if (row[i]!= None):
            textArray.append(TextSendMessage(text=row[i]))
    return textArray
print(reply('小循'))



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    print("event.source.user_id:", event.source.user_id)
	
    if event.message.text == "profile":
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='Status message: ' + profile.status_message
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
	
    if event.message.text == "據點查詢":
        buttons_template = TemplateSendMessage(
            alt_text='據點查詢 template',
            template=ButtonsTemplate(
                title='據點查詢',
                text='請選擇地區',
                thumbnail_image_url='https://i.imgur.com/u2dMEPE.jpg',
                actions=[
                    MessageTemplateAction(
                        label='北部[尚未有據點]',
                        text='北部地區'
                    ),
                    MessageTemplateAction(
                        label='中部',
                        text='中部地區'
                    ),
                    MessageTemplateAction(
                        label='南部[尚未有據點]',
                        text='南部地區'					
                    ),
                    MessageTemplateAction(
                        label='東部[尚未有據點]',
                        text='東部地區'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='這是目前台灣與循環經濟有關的地方喔!(๑´ㅂ`๑)' 
                    ),
					TextSendMessage(
                        text='點進去可以看到各區縣市( • ̀ω•́ )ﾉ' 
                    ),
                    buttons_template
                ]
            )
        return 0
		  		
    if event.message.text == "北部地區":
        carousel_template = TemplateSendMessage(
            alt_text='北部地區 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/dlIRYTP.jpg',
                        title='北部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='臺北市',
                                text='臺北市',
                            ),
                            MessageTemplateAction(
                                label='新北市',
                                text='新北市'
                            ),
                            MessageTemplateAction(
                                label='基隆市',
                                text='基隆市'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/dlIRYTP.jpg',
                        title='北部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='宜蘭市',
                                text='宜蘭市',
                            ),
                            MessageTemplateAction(
                                label='桃園市',
                                text='桃園市'
                            ),
							MessageTemplateAction(
                                label=' ',
                                text=' '
                            )
                        ]
                    ),
    			    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/dlIRYTP.jpg',
                        title='北部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='新竹市',
                                text='新竹市',
                            ),
                            MessageTemplateAction(
                                label='新竹縣',
                                text='新竹縣'
                            ),
							MessageTemplateAction(
                                label=' ',
                                text=' '
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='目前北部沒有任何相關的據點呦(๑•́ ₃ •̀๑)'
                    ),
					TextSendMessage(
                        text='可利用選單去察看別的地方呦(๑• ∀ •๑)σ' 
                    ),
                    carousel_template
                ]
        )
        return 0
		
    if event.message.text == "中部地區":
        carousel_template = TemplateSendMessage(
            alt_text='中部地區 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qLkJthI.jpg',
                        title='中部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='苗栗縣[尚未有據點]',
                                text='苗栗縣',
                            ),
                            MessageTemplateAction(
                                label='臺中市[尚未有據點]',
                                text='臺中市'
                            ),
                            MessageTemplateAction(
                                label='彰化縣[尚未有據點]',
                                text='彰化縣'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qLkJthI.jpg',
                        title='中部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='南投縣[尚未有據點]',
                                text='南投縣',
                            ),
					    	MessageTemplateAction(
                                label='雲林縣',
                                text='雲林縣',
                            ),
							MessageTemplateAction(
                                label=' ',
                                text=' '
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='目前雲林縣有資訊喔ヽ(́◕◞౪◟◕‵)ﾉ' 
                    ),
					TextSendMessage(
                        text='還不趕快點進去看ε٩(๑> ₃ <)۶з' 
                    ),
                    carousel_template
                ]
        )
        return 0
		
    if event.message.text == "南部地區":
        carousel_template = TemplateSendMessage(
            alt_text='南部地區 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/PBO9YmT.jpg',
                        title='南部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='嘉義市',
                                text='嘉義市',
                            ),
                            MessageTemplateAction(
                                label='嘉義縣',
                                text='嘉義縣'
                            ),
                            MessageTemplateAction(
                                label='臺南市',
                                text='臺南市'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/PBO9YmT.jpg',
                        title='南部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='高雄市',
                                text='高雄市',
                            ),
                            MessageTemplateAction(
                                label='屏東縣',
                                text='屏東縣'
                            ),
					    	MessageTemplateAction(
                                label='澎湖縣',
                                text='澎湖縣',
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='目前南部沒有任何相關的據點呦(๑•́ ₃ •̀๑)' 
                    ),
					TextSendMessage(
                        text='可利用選單去察看別的地方呦(๑• ∀ •๑)σ' 
                    ),
                    carousel_template
                ]
        )
        return 0
		
    if event.message.text == "東部地區":
        buttons_template = TemplateSendMessage(
            alt_text='東部地區 template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/XyFXwzp.jpg',
                title='東部據點查詢',
                text='請選擇縣市',
                actions=[
                    MessageTemplateAction(
                        label='花蓮縣',
                        text='花蓮縣',
                        ),
                    MessageTemplateAction(
                        label='臺東縣',
                        text='臺東縣'
                        )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='目前東部沒有任何相關的據點呦(๑•́ ₃ •̀๑)' 
                    ),
					TextSendMessage(
                        text='可利用選單去察看別的地方呦(๑• ∀ •๑)σ' 
                    ),
                    buttons_template
                ]
        )
        return 0
    
    if event.message.text == "雲林縣":	
        buttons_template = TemplateSendMessage(
            alt_text='雲林縣 template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/2unBCry.jpg',
                title='緻遠國際',
                text='香妍SHINING SECRET是全球首支主打沉香香氛系列、純淨天然、傳遞正能量的美妝保養品牌。',
                actions=[
                    MessageTemplateAction(
                        label='了解緻遠國際',
                        text='我想了解緻遠國際',
                    ),
                    URITemplateAction(
                        label='官方網站',
                        uri='https://www.zhiyuan.com.tw/ext/'
                    ),
                    URITemplateAction(
                        label='加入line',
                        uri='https://line.me/R/ti/p/%40exd6980d'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
 
    if event.message.text == "循環經濟":
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
        return 0
   
    if event.message.text == "送圖囉":
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
	
    if event.message.text == "小循說故事":
        confirm_template = TemplateSendMessage(
            alt_text='說故事 template',
            template=ConfirmTemplate(
                text='請選擇，要選左邊的呦<3',
                actions=[
                    MessageTemplateAction(
                        label='繼續說',
                        text='繼續說'
                    ),
                    MessageTemplateAction(
                        label='不想聽了',
                        text='閉嘴'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='好的好的~小循來說故事囉٩(๑•̀ω•́๑)۶'
                    ),
					TextSendMessage(
                        text='小循知道現在地球很老惹' 
                    ),
					TextSendMessage(
                        text='然而人們一直耗資源製造東西丟東西(つд⊂)' 
                    ),
					TextSendMessage(
                        text='所以地球生氣惹ヽ(#`Д´)ﾉ' 
                    ),
					confirm_template
                ]
        )
		
    if event.message.text == "繼續說":
        confirm_template = TemplateSendMessage(
            alt_text='說故事 template',
            template=ConfirmTemplate(
                text='請選擇，要選左邊的呦<3',
                actions=[
                    MessageTemplateAction(
                        label='繼續說',
                        text='繼續說2'
                    ),
                    MessageTemplateAction(
                        label='不想聽了',
                        text='閉嘴'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='地球氣候愈來愈可怕了'
                    ),
					TextSendMessage(
                        text='為了改善環境，循環經濟粗現了' 
                    ),
					TextSendMessage(
                        text='為您展示一下傳統的生產模式' 
                    ),
					ImageSendMessage(
    					original_content_url='https://i.imgur.com/1hMVlfd.jpg',
    					preview_image_url='https://i.imgur.com/1hMVlfd.jpg'
					),
					confirm_template
                ]
        )
		
    if event.message.text == "繼續說2":
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='再為您展示循環經濟的方式'
                    ),
					ImageSendMessage(
    					original_content_url='https://i.imgur.com/nA5BVgf.jpg',
    					preview_image_url='https://i.imgur.com/nA5BVgf.jpg'
					),
					TextSendMessage(
                        text='沒錯~傳統的就是丟棄丟棄在丟棄，而循環經濟就是可再利用，減少廢棄物' 
                    ),
					TextSendMessage(
                        text='所以循環經濟不僅僅環保、還可以減少消耗資源，大大的減低成本呢!' 
                    ),
					TextSendMessage(
                        text='是不是有理解了呢ヾ(*´∀ ˋ*)ﾉ' 
                    )
                ]
        )
		
    if event.message.text == "小循說原則":
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
		
    if event.message.text =="呼叫小循":
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
                        text='歡迎來到循跡點點ε٩(๑> ₃ <)۶з'
                    ),
					TextSendMessage(
                        text='我是小循機器人٩(๑•̀ω•́๑)۶' 
                    ),
					TextSendMessage(
                        text='有什麼我可以為您服務的呢ヾ(*´∀ ˋ*)ﾉ' 
                    ),
                    buttons_template
                ]
        )
        return 0
    

    for i in range (10): 
        if find(i) in event.message.text: 
            print (find(i))
            t = find(i)
            line_bot_api.reply_message(event.reply_token, reply(t))
	
		
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='小循不懂(๑•́ ₃ •̀๑)'))		
    
    
    cursor.close()
    cnx.close()
    
if __name__ == '__main__':
    app.run()
