from linebot.models import (
    TextSendMessage, TextMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction, ButtonsTemplate
)

response_WTKM = TextSendMessage(
	text='He is a good boy!'
)

response_DWTKM = TemplateSendMessage(
    alt_text='Sorry, This message can show on mobile :)',
    template=ButtonsTemplate(
        text='Please take a look!\nHe is such a nnnnnnnnnice guy',
        actions=[
            PostbackAction(
                label='OK, fine.',
                text='OK, fine.',
                data='action=WTKM' # Want to know me.
            )
        ]
    )
)

response_alreadyKM = TextSendMessage(
	text="It's ok, I know you already know him <3"
)
