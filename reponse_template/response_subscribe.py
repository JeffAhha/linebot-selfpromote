from linebot.models import (
    TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, StickerSendMessage
)

response_onSubscribeClick = TemplateSendMessage(
    alt_text='Wnat to subscribe?',
    template=ConfirmTemplate(
        text="I was a casual game developer before.\n\nI can recommand a casual game to you everyday!\n\nWant to subscribe?",
        actions=[
            PostbackAction(
                label='Yes!',
                text='Yes!',
                data='subscribe_accept' # Want to know me.
            ),
            PostbackAction(
                label='No~',
                text='No~',
                data='subscribe_refuse' # Dont wnt to know me.
            )
        ]
    )
)

response_onDesubscribeClick = TemplateSendMessage(
    alt_text='Want to desubscribe?',
    template=ConfirmTemplate(
        text="You already subscribe, you want to unsubscribe?",
        actions=[
            PostbackAction(
                label='Yes',
                text='Yes',
                data='desubscribe_accept' # Want to know me.
            ),
            PostbackAction(
                label='No',
                text='No',
                data='desubscribe_refuse' # Dont wnt to know me.
            )
        ]
    )
)

response_subscribe_refuse = TextSendMessage(
	text='OK, You can subscribe whenever you want \uDBC0\uDC8D'
)

response_subscribe_accept = TextSendMessage(
    text='OK,i will send information to you at 10am everyday.'
)

response_subscribe_accept2 = StickerSendMessage(
    package_id='1',
    sticker_id='117'
)

response_desubscribe_accept = TextSendMessage(
    text="You unsubscribe now~\nYou can subscribe again whenever you want!"
)

response_desubscribe_refuse = TextSendMessage(
    text="OK, I will keep sending game information to you everyday~"
)
