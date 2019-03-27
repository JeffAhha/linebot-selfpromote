import threading
import time
from reponse_template import response_challenge

import settings
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent,
    TextMessage, TextSendMessage, StickerSendMessage, TemplateSendMessage, ImageCarouselTemplate, CarouselTemplate,
    CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)

line_bot_api = LineBotApi(settings.line_channel_secret)
handler = WebhookHandler(settings.line_webhook_secret)


def main():
    line_bot_api.push_message(
        settings.line_debug_userid,
        TextSendMessage(
        	text='OK, You can subscribe whenever you want \uDBC0\uDC8D'
        ))

main()
