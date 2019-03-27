from random import randint
from linebot.models import (
    TextSendMessage, TemplateSendMessage, ConfirmTemplate, ButtonsTemplate, PostbackAction, MessageAction
)

response_start_another_challenge = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ConfirmTemplate(
        text='You didnt finish last challenge, resume or restart?',
        actions=[
            PostbackAction(
                label='Resume',
                text='Resume',
                data='challenge_resume' # Want to know me.
            ),
            PostbackAction(
                label='Restart',
                text='Restart',
                data='challenge_restart' # Want to know me.
            )
        ]
    )
)

response_start_firsttime_challenge = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ButtonsTemplate(
        text='Try to get 10 correct as fast as possible!',
        actions=[
            PostbackAction(
                label='Start',
                text='Start',
                data='challenge_start' # Want to know me.
            )
        ]
    )
)

response_when_correct = TextSendMessage(
	text='Correct!'
)

response_when_wrong = TextSendMessage(
	text='Wrong!'
)

response_challenge_done = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ButtonsTemplate(
        text='Well done, You finish the challenge ',
        actions=[
            PostbackAction(
                label='Start',
                text='Start',
                data='challenge_start' # Want to know me.
            )
        ]
    )
)

response_challenge_get_highest_score = TextSendMessage(
	text="Wow, it's the shortest time ever spent \uDBC0\uDC85"
)

def onChallengeDone(time,isBestScore):
    if isBestScore == True:
        return TextSendMessage(
        	text='Well done, You finish the challenge in {0} seconds!'.format(time),
        )
    else:
        return TemplateSendMessage(
            alt_text='Sorry, This message can show on mobile :)',
            template=ButtonsTemplate(
                text='Well done, You finish the challenge in {0} seconds!'.format(time),
                actions=[
                    MessageAction(
                        label='See Best Score',
                        text='See Best Score'
                    )
                ]
            )
        )

def genQuestion(questionNumber):
    a = randint(1,20)
    b = randint(1,5)
    c = randint(1,10)
    ans = 0
    operand1 = ''
    operand2 = ''

    formulaType = randint(0,3)
    if formulaType == 0:
        operand1 = '*'
        operand2 = '+'
        ans = a*b+c
    elif formulaType == 1:
        operand1 = '+'
        operand2 = '-'
        ans = a+b-c
    elif formulaType == 2:
        operand1 = '-'
        operand2 = '*'
        ans = a-b*c
    elif formulaType == 3:
        operand1 = '+'
        operand2 = '+'
        ans = a+b+c

    isEqual = randint(0,1)
    ## 0 = Equal, 1 = Not Equal
    if isEqual == 0:
        question = 'Q'+str(questionNumber)+'\n'+'{0}{1}{2}{3}{4}={5}'.format(a,operand1,b,operand2,c,ans)
        response = TemplateSendMessage(
            alt_text='Sorry, This message can show on mobile :)',
            template=ConfirmTemplate(
                text=question,
                actions=[
                    PostbackAction(
                        label='Yes!',
                        text='Yes!',
                        data='answer_Yes' # Want to know me.
                    ),
                    PostbackAction(
                        label='No',
                        text='No',
                        data='answer_No' # Dont wnt to know me.
                    )
                ]
            )
        )
        return [response,question,'answer_Yes']
    else:
        question = 'Q'+str(questionNumber)+'\n'+'{0}{1}{2}{3}{4}={5}'.format(a,operand1,b,operand2,c,(ans+randint(1,50)))
        response = TemplateSendMessage(
            alt_text='Sorry, This message can show on mobile :)',
            template=ConfirmTemplate(
                text=question,
                actions=[
                    PostbackAction(
                        label='Yes!',
                        text='Yes!',
                        data='answer_Yes' # Want to know me.
                    ),
                    PostbackAction(
                        label='No',
                        text='No',
                        data='answer_No' # Dont wnt to know me.
                    )
                ]
            )
        )
        return [response,question,'answer_No']

def onResume(question):
    return TemplateSendMessage(
        alt_text='Sorry, This message can show on mobile :)',
        template=ConfirmTemplate(
            text=str(question),
            actions=[
                PostbackAction(
                    label='Yes!',
                    text='Yes!',
                    data='answer_Yes' # Want to know me.
                ),
                PostbackAction(
                    label='No!',
                    text='No!',
                    data='answer_No' # Dont wnt to know me.
                )
            ]
        )
    )

def onSeeBestScoreClick(score):
    return TextSendMessage(
    	text='Your best score is {0}s!'.format(score)
    )
