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
'''
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    if text == 'profile':
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
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'imagemap':
        pass
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))
'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    
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
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
		
    if event.message.text =="1":
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='fuck'
                ),
                TextSendMessage(
                    text='you'
                )
            ]
        )
        
		
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
        line_bot_api.reply_message(event.reply_token, carousel_template)
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
        line_bot_api.reply_message(event.reply_token, carousel_template)
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
        line_bot_api.reply_message(event.reply_token, carousel_template)
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
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
    if event.message.text == "雲林縣":	
        buttons_template = TemplateSendMessage(
            alt_text='雲林縣 template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/2unBCry.jpg',
                title='香研',
                text='香妍SHINING SECRET是全球首支主打沉香香氛系列、純淨天然、傳遞正能量的美妝保養品牌。',
                actions=[
                    MessageTemplateAction(
                        label='了解香研',
                        text='我想了解香研',
                    ),
                    URITemplateAction(
                        label='官網',
                        uri='https://www.zhiyuan.com.tw/ext/'
                    ),
                    URITemplateAction(
                        label='加入line',
                        uri='https://line.me/R/ti/p/%40uur2008z'
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
                    URITemplateAction(
                        label='影片介紹循環經濟',
                        uri='https://www.youtube.com/watch?v=LI4J4xXEuw4'
                    ),
                    MessageTemplateAction(
                        label='什麼是循環經濟?',
                        text='循環經濟是什麼?'
                    ),
                    MessageTemplateAction(
                        label='為何要循環經濟?',
                        text='為何要循環經濟?'
                    )				
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
		
    if event.message.text == "需要服務":
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
		
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不好意思，尚未開啟此服務，請利用選單選擇其他功能呦'))		

    
if __name__ == '__main__':
    app.run()
