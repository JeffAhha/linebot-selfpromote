from linebot.models import (
    TextSendMessage, TextMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction, ButtonsTemplate
)

# response = TextSendMessage(
# 	text='Hi there, nice to meet you! \nThis bot is made by Jeff Chen~\n Would you like to know more about him? \uDBC0\uDC8D'
# )

def on_follow(display_name):
    return TemplateSendMessage(
        alt_text='Hi {0}, nice to meet you :)'.format(display_name),
        template=ConfirmTemplate(
            text='Hi {0}, nice to meet you! \n\nMy name is Jeff and this chatbot is made by me.\n\nWould you like to know more about me?'.format(display_name),
            actions=[
                PostbackAction(
                    label='Sure',
                    text='Sure',
                    data='action=WTKM' # Want to know me.
                ),
                PostbackAction(
                    label='No',
                    text='No',
                    data='action=DWTKM' # Dont wnt to know me.
                )
            ]
        )
    )
