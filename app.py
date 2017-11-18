import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

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
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']
	
	
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
   
    if event.message.text == "據點查詢":
        buttons_template = TemplateSendMessage(
            alt_text='據點查詢 template',
            template=ButtonsTemplate(
                title='據點查詢',
                text='請選擇地區',
                thumbnail_image_url='https://www2.moeaboe.gov.tw/oil102/oil1022010/map/images/taiwan.png',
                actions=[
                    MessageTemplateAction(
                        label='北部',
                        text='北部地區'
                    ),
                    MessageTemplateAction(
                        label='中部',
                        text='中部地區'
                    ),
                    MessageTemplateAction(
                        label='南部',
                        text='南部地區'					
                    ),
                    MessageTemplateAction(
                        label='東部',
                        text='東部地區'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "北部地區":
        carousel_template = TemplateSendMessage(
            alt_text='北部地區 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Northern_Taiwan_official_determined.svg/330px-Northern_Taiwan_official_determined.svg.png',
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
                        thumbnail_image_url='https://b1.rimg.tw/secretes/a4d6735a.jpg',
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
                        thumbnail_image_url='https://b1.rimg.tw/secretes/a4d6735a.jpg',
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
        line_bot_api.reply_message(event.reply_token, carousel_template)
        return 0
    if event.message.text == "中部地區":
        carousel_template = TemplateSendMessage(
            alt_text='中部地區 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Central_Taiwan_official_determined.svg/375px-Central_Taiwan_official_determined.svg.png',
                        title='中部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='苗栗縣',
                                text='苗栗縣',
                            ),
                            MessageTemplateAction(
                                label='臺中市',
                                text='臺中市'
                            ),
                            MessageTemplateAction(
                                label='彰化縣',
                                text='彰化縣'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://b1.rimg.tw/secretes/a4d6735a.jpg',
                        title='中部據點查詢',
                        text='請選擇縣市',
                        actions=[
                            MessageTemplateAction(
                                label='南投縣',
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
        line_bot_api.reply_message(event.reply_token, carousel_template)
        return 0
    if event.message.text == "南部地區":
        carousel_template = TemplateSendMessage(
            alt_text='南部地區 template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Southern_Taiwan_official_determined.svg/330px-Southern_Taiwan_official_determined.svg.png',
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
                        thumbnail_image_url='https://b1.rimg.tw/secretes/a4d6735a.jpg',
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
        line_bot_api.reply_message(event.reply_token, carousel_template)
        return 0
    if event.message.text == "東部地區":
        buttons_template = TemplateSendMessage(
            alt_text='東部地區 template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Eastern_Taiwan_official_determined.svg/330px-Eastern_Taiwan_official_determined.svg.png',
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
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
    if event.message.text == "雲林縣":	
        image_carousel_template = TemplateSendMessage(
            alt_text='雲林縣 template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/2unBCry.jpg',
                        action=PostbackTemplateAction(
                            label='詳細了解',
                            text='我想了解香研',
                            #data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://example.com/item2.jpg',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        ) 
        line_bot_api.reply_message(event.reply_token, image_carousel_template)
        return 0
 
    if event.message.text == "循環經濟":
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='歡迎來到循跡點點',
                text='請選擇服務',
                thumbnail_image_url='https://www.wealth.com.tw/files/d25b1c682936476f9a4f8942a9857e16.jpg',
                actions=[               
                    URITemplateAction(
                        label='關於循環經濟',
                        uri='https://www.youtube.com/watch?v=LI4J4xXEuw4'
                    ),
                    MessageTemplateAction(
                        label='據點查詢',
                        text='據點查詢'
                    ),
                    URITemplateAction(
                        label='聯絡負責人',
                        uri='https://www.facebook.com/profile.php?id=100000346362054'
                    )							
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不好意思，尚未此服務，請利用選單選擇其他功能呦'))	

    
if __name__ == '__main__':
    app.run()
