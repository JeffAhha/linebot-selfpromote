from linebot.models import (
    TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction
)

response_onSubscribeClick = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ConfirmTemplate(
        text="Subscribe to get more game information?\nI will recommand you a casual game everyday!",
        actions=[
            PostbackAction(
                label='Yes',
                text='Yes!',
                data='subscribe_accept' # Want to know me.
            ),
            PostbackAction(
                label='No',
                text='No~',
                data='subscribe_refuse' # Dont wnt to know me.
            )
        ]
    )
)

response_onDesubscribeClick = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ConfirmTemplate(
        text="Subscribe to get more game information?\nI will recommand you a casual game everyday!",
        actions=[
            PostbackAction(
                label='Yes',
                text='Yes!',
                data='desubscribe_accept' # Want to know me.
            ),
            PostbackAction(
                label='No',
                text='No~',
                data='desubscribe_refuse' # Dont wnt to know me.
            )
        ]
    )
)

response_subscribe_refuse = TextSendMessage(
	text='OK, You can subscribe whenever you want~ \uDBC0\uDC8D'
)

response_subscribe_accept = TextSendMessage(
    text='This is todays'
)

response_desubscribe_accept = TextSendMessage(
    text="You're desubscribe now~\nYou can subscribe again when ever you want!"
)

response_desubscribe_refuse = TextSendMessage(
    text="OK, I will keep sending game information to you everyday~"
)
