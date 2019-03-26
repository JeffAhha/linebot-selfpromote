from linebot.models import (
    TextSendMessage, TextMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction, ButtonsTemplate
)

# response = TextSendMessage(
# 	text='Hi there, nice to meet you! \nThis bot is made by Jeff Chen~\n Would you like to know more about him? \uDBC0\uDC8D'
# )

response = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ConfirmTemplate(
        text='Hi there, nice to meet you! \nThis bot is made by Jeff Chen~\nWould you like to know more about him?',
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
