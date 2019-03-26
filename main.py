# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

##########################################
### Import Dependencies
##########################################
from datetime import datetime
from flask import Flask, request, abort
import settings
from reponse_template import response_myprojects, response_onfollow, response_aboutme, response_subscribe, response_challenge
import firebase_admin
from firebase_admin import firestore
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


##########################################
### Initialize
##########################################

firebase_admin.initialize_app()
user_collection = firestore.client().collection('userData')

line_bot_api = LineBotApi(settings.line_channel_secret)
handler = WebhookHandler(settings.line_webhook_secret)
debug_user_id = settings.line_debug_userid

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        text = event.message.text
        user_id = event.source.user_id
        user_ref = user_collection.document(user_id)
        doc = user_ref.get().to_dict()

        if text == 'About Jeff':
            line_bot_api.reply_message(
                event.reply_token,
                response_aboutme.response_WTKM)
        elif text == "Jeff's project":
            line_bot_api.reply_message(
                event.reply_token,
                response_myprojects.response_porjects_carousel)
            line_bot_api.push_message(
                user_id,
                response_myprojects.response_introduce)
        elif text == 'Take 10 Questions challenge!':
            if doc['isPlayingGame'] == True:
                line_bot_api.reply_message(
                    event.reply_token,
                    response_challenge.response_start_another_challenge)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    response_challenge.response_start_firsttime_challenge)
        elif text == 'Subscribe!':
            if doc['subscribe'] == True:
                line_bot_api.reply_message(
                event.reply_token,
                response_subscribe.response_onDesubscribeClick)
            else:
                line_bot_api.reply_message(
                event.reply_token,
                response_subscribe.response_onSubscribeClick)
            ####todo
            print(event)
    except Exception as e:
        send_to_debug_account(str(e))

@handler.add(FollowEvent)
def handle_Follow(event):
    try:
        user_ref = user_collection.document(event.source.user_id)
        user_ref.set({
            'subscribe':False,
            'gameHighestScore':100000,
            'isPlayingGame':False,
            'isKnowMe':False,
            'gameCurrentQuestionNumber':1,
            'gameQuestion':'',
            'gameAnswer':'',
            'gameStartTime':'',
            'gameEndTime':'',
        })
        # send_to_debug_account(str(user_ref.get().to_dict()['gameStartTime']))
        line_bot_api.reply_message(
            event.reply_token,
            response_onfollow.response)
    except Exception as e:
        send_to_debug_account(str(e))

@handler.add(PostbackEvent)
def handle_Postback(event):
    try:
        data = event.postback.data
        user_id = event.source.user_id
        user_ref = user_collection.document(user_id)
        doc = user_ref.get().to_dict()

        if data == 'action=WTKM':
            line_bot_api.reply_message(
                event.reply_token,
                response_aboutme.response_WTKM)
        elif data =='action=DWTKM':
            line_bot_api.reply_message(
                event.reply_token,
                response_aboutme.response_DWTKM)
        elif data =='subscribe_accept':
            ###todo
            print(event)
        elif data =='subscribe_refuse':
            ###todo
            print(event)
        elif data =='desubscribe_accept':
            ###todo
            print(event)
        elif data =='desubscribe_refuse':
            ###todo
            print(event)
        elif data == 'challenge_start':
            question = response_challenge.genQuestion(doc['gameCurrentQuestionNumber'])
            line_bot_api.reply_message(
                event.reply_token,
                question[0])
            user_ref.update({
                'gameStartTime':firestore.SERVER_TIMESTAMP,
                'gameQuestion':question[1],
                'gameAnswer':question[2],
                'gameCurrentQuestionNumber':1,
                'isPlayingGame':True
                })
        elif doc['isPlayingGame'] and (data == 'answer_Yes' or data == 'answer_No'):
            if doc['gameAnswer'] == data:
                if doc['gameCurrentQuestionNumber'] == 2:
                    user_ref.update({'gameEndTime':firestore.SERVER_TIMESTAMP})
                    doc = user_ref.get().to_dict()
                    time_start = datetime.strptime(str(doc['gameStartTime']),"%Y-%m-%d %H:%M:%S.%f%z")
                    time_end = datetime.strptime(str(doc['gameEndTime']),"%Y-%m-%d %H:%M:%S.%f%z")
                    totalTime = (time_end-time_start).seconds
                    if totalTime < doc['gameHighestScore']:
                        line_bot_api.reply_message(
                            event.reply_token,
                            response_challenge.onChallengeDone(totalTime,True))
                        line_bot_api.push_message(
                            user_id,
                            response_challenge.response_challenge_get_highest_score)
                        user_ref.update({
                            'gameHighestScore':totalTime
                        })
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            response_challenge.onChallengeDone(totalTime,False))

                    user_ref.update({
                        'isPlayingGame':False,
                    })
                else:
                    question = response_challenge.genQuestion(doc['gameCurrentQuestionNumber']+1)
                    line_bot_api.reply_message(
                        event.reply_token,
                        response_challenge.response_when_correct)
                    line_bot_api.push_message(user_id,question[0])
                    user_ref.update({
                        'gameQuestion':question[1],
                        'gameAnswer':question[2],
                        'gameCurrentQuestionNumber':doc['gameCurrentQuestionNumber']+1
                        })
            else:
                question = response_challenge.genQuestion(doc['gameCurrentQuestionNumber'])
                line_bot_api.reply_message(
                    event.reply_token,
                    response_challenge.response_when_wrong)
                line_bot_api.push_message(user_id,question[0])
                user_ref.update({
                    'gameQuestion':question[1],
                    'gameAnswer':question[2]
                    })
    except Exception as e:
        send_to_debug_account(str(e))

@handler.default()
def default(event):
    print(event)

def send_to_debug_account(text):
    line_bot_api.push_message(debug_user_id,
        TextSendMessage(
            text="Text : "+text
        ))

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=3000)