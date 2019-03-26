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
        profile = line_bot_api.get_profile(user_id)
        user_ref = user_collection.document(user_id)
        doc = user_ref.get().to_dict()

        if text == 'I want to know more about Jeff':
            line_bot_api.reply_message(
                event.reply_token,
                response_aboutme.response_WTKM)
            line_bot_api.push_message(
                user_id,
                response_aboutme.response_WTKM2)
            line_bot_api.push_message(
                user_id,
                response_aboutme.response_WTKM3)
            line_bot_api.push_message(
                user_id,
                response_aboutme.response_WTKM4)
        elif text == "Any project made by Jeff?" or text == 'project' or text == 'Project':
            line_bot_api.reply_message(
                event.reply_token,
                response_myprojects.response_porjects_carousel)
            line_bot_api.push_message(
                user_id,
                response_myprojects.response_introduce)
        elif text == 'Take 10 Questions Challenge!!' or text == 'challenge' or text == 'Challenge':
            if doc['isPlayingGame'] == True:
                line_bot_api.reply_message(
                    event.reply_token,
                    response_challenge.response_start_another_challenge)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    response_challenge.response_start_firsttime_challenge)
        elif text == 'Subscribe' or text == 'subscribe':
            if doc['isSubscribe'] == True:
                line_bot_api.reply_message(
                    event.reply_token,
                    response_subscribe.response_onDesubscribeClick)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    response_subscribe.response_onSubscribeClick)
        elif text == 'Hi' or text == 'hi':
            line_bot_api.reply_message(
                event.reply_token,
                response_onfollow.on_follow(profile.display_name))

    except Exception as e:
        send_to_debug_account(str(e))

@handler.add(FollowEvent)
def handle_Follow(event):
    try:
        user_id = event.source.user_id
        profile = line_bot_api.get_profile(user_id)
        user_ref = user_collection.document(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            response_onfollow.on_follow(profile.display_name))
        user_ref.set({
            'isSubscribe':False,
            'gameHighestScore':100000,
            'isPlayingGame':False,
            'isKnowMe':False,
            'gameCurrentQuestionNumber':1,
            'gameQuestion':'',
            'gameAnswer':'',
            'gameStartTime':'',
            'gameEndTime':'',
        })
    except Exception as e:
        send_to_debug_account(str(e))

@handler.add(PostbackEvent)
def handle_Postback(event):
    data = event.postback.data
    user_id = event.source.user_id
    user_ref = user_collection.document(user_id)
    doc = user_ref.get().to_dict()

    if data == 'action=WTKM':
        line_bot_api.reply_message(
            event.reply_token,
            response_aboutme.response_WTKM)
        line_bot_api.push_message(
            user_id,
            response_aboutme.response_WTKM2)
        line_bot_api.push_message(
            user_id,
            response_aboutme.response_WTKM3)
        line_bot_api.push_message(
            user_id,
            response_aboutme.response_WTKM4)
    elif data =='action=DWTKM':
        line_bot_api.reply_message(
            event.reply_token,
            response_aboutme.response_DWTKM
        )
        line_bot_api.push_message(
            user_id,
            response_aboutme.response_DWTKM2)
    elif data =='subscribe_accept':
        line_bot_api.reply_message(
            event.reply_token,
            response_subscribe.response_subscribe_accept)
        line_bot_api.push_message(
            user_id,
            response_subscribe.response_subscribe_accept2)
        user_ref.update({'isSubscribe':True})
    elif data =='subscribe_refuse':
        line_bot_api.reply_message(
            event.reply_token,
            response_subscribe.response_subscribe_refuse)
    elif data =='desubscribe_accept':
        line_bot_api.reply_message(
            event.reply_token,
            response_subscribe.response_desubscribe_accept)
        user_ref.update({'isSubscribe':False})
    elif data =='desubscribe_refuse':
        line_bot_api.reply_message(
            event.reply_token,
            response_subscribe.response_desubscribe_refuse)
    elif data =='challenge_start':
        question = response_challenge.genQuestion(1)
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
    elif data =='challenge_resume' and doc['isPlayingGame'] == True:
        line_bot_api.reply_message(
            event.reply_token,
            response_challenge.onResume(doc['gameQuestion']))
    elif data =='challenge_restart' and doc['isPlayingGame'] == True:
        line_bot_api.reply_message(
            event.reply_token,
            response_challenge.response_start_firsttime_challenge)
    elif doc['isPlayingGame'] and (data == 'answer_Yes' or data == 'answer_No'):
        if doc['gameAnswer'] == data:
            if doc['gameCurrentQuestionNumber'] == 10:
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
                    user_ref.update({'gameHighestScore':totalTime})
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        response_challenge.onChallengeDone(totalTime,False))

                user_ref.update({'isPlayingGame':False})
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
    elif data == 'aboutme_got_it':
        line_bot_api.reply_message(
            event.reply_token,
            response_aboutme.response_navigate)
    # try:
    #     data = event.postback.data
    #     user_id = event.source.user_id
    #     user_ref = user_collection.document(user_id)
    #     doc = user_ref.get().to_dict()
    #
    #     if data == 'action=WTKM':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_aboutme.response_WTKM)
    #         line_bot_api.push_message(
    #             user_id,
    #             response_aboutme.response_WTKM2)
    #         line_bot_api.push_message(
    #             user_id,
    #             response_aboutme.response_WTKM3)
    #         line_bot_api.push_message(
    #             user_id,
    #             response_aboutme.response_WTKM4)
    #     elif data =='action=DWTKM':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_aboutme.response_DWTKM
    #         )
    #         line_bot_api.push_message(
    #             user_id,
    #             response_aboutme.response_DWTKM2)
    #     elif data =='subscribe_accept':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_subscribe.response_subscribe_accept)
    #         line_bot_api.push_message(
    #             user_id,
    #             response_subscribe.response_subscribe_accept2)
    #         user_ref.update({'isSubscribe':True})
    #     elif data =='subscribe_refuse':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_subscribe.response_subscribe_refuse)
    #     elif data =='desubscribe_accept':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_subscribe.response_desubscribe_accept)
    #         user_ref.update({'isSubscribe':False})
    #     elif data =='desubscribe_refuse':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_subscribe.response_desubscribe_refuse)
    #     elif data =='challenge_start':
    #         question = response_challenge.genQuestion(1)
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             question[0])
    #         user_ref.update({
    #             'gameStartTime':firestore.SERVER_TIMESTAMP,
    #             'gameQuestion':question[1],
    #             'gameAnswer':question[2],
    #             'gameCurrentQuestionNumber':1,
    #             'isPlayingGame':True
    #             })
    #     elif data =='challenge_resume' and doc['isPlayingGame'] == True:
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_challenge.onResume(doc['gameCurrentQuestionNumber'],doc['gameQuestion']))
    #     elif data =='challenge_restart' and doc['isPlayingGame'] == True:
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_challenge.response_start_firsttime_challenge)
    #     elif doc['isPlayingGame'] and (data == 'answer_Yes' or data == 'answer_No'):
    #         if doc['gameAnswer'] == data:
    #             if doc['gameCurrentQuestionNumber'] == 10:
    #                 user_ref.update({'gameEndTime':firestore.SERVER_TIMESTAMP})
    #                 doc = user_ref.get().to_dict()
    #                 time_start = datetime.strptime(str(doc['gameStartTime']),"%Y-%m-%d %H:%M:%S.%f%z")
    #                 time_end = datetime.strptime(str(doc['gameEndTime']),"%Y-%m-%d %H:%M:%S.%f%z")
    #                 totalTime = (time_end-time_start).seconds
    #                 if totalTime < doc['gameHighestScore']:
    #                     line_bot_api.reply_message(
    #                         event.reply_token,
    #                         response_challenge.onChallengeDone(totalTime,True))
    #                     line_bot_api.push_message(
    #                         user_id,
    #                         response_challenge.response_challenge_get_highest_score)
    #                     user_ref.update({'gameHighestScore':totalTime})
    #                 else:
    #                     line_bot_api.reply_message(
    #                         event.reply_token,
    #                         response_challenge.onChallengeDone(totalTime,False))
    #
    #                 user_ref.update({'isPlayingGame':False})
    #             else:
    #                 question = response_challenge.genQuestion(doc['gameCurrentQuestionNumber']+1)
    #                 line_bot_api.reply_message(
    #                     event.reply_token,
    #                     response_challenge.response_when_correct)
    #                 line_bot_api.push_message(user_id,question[0])
    #                 user_ref.update({
    #                     'gameQuestion':question[1],
    #                     'gameAnswer':question[2],
    #                     'gameCurrentQuestionNumber':doc['gameCurrentQuestionNumber']+1
    #                     })
    #         else:
    #             question = response_challenge.genQuestion(doc['gameCurrentQuestionNumber'])
    #             line_bot_api.reply_message(
    #                 event.reply_token,
    #                 response_challenge.response_when_wrong)
    #             line_bot_api.push_message(user_id,question[0])
    #             user_ref.update({
    #                 'gameQuestion':question[1],
    #                 'gameAnswer':question[2]
    #                 })
    #     elif data == 'aboutme_got_it':
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             response_aboutme.response_navigate)
    # except Exception as e:
    #     send_to_debug_account(str(e))

@handler.default()
def default(event):
    print(event)

def send_to_debug_account(text):
    line_bot_api.push_message(debug_user_id,
        TextSendMessage(
            text="Text : "+text))

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=3000)
