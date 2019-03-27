from linebot.models import (
    StickerSendMessage, TextSendMessage, TextMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction, ButtonsTemplate
)

response_WTKM = TextSendMessage(
	text="I graduated from Nation Central University."
)

response_WTKM2 = TextSendMessage(
	text="After two years of graduating, I worked as a mobile game engineer and project managemer at Orangenose Studio."
)

response_WTKM3 = TextSendMessage(
	text="After completing my dream of making game, I enter GIEE of National Taiwan University to finish my master degree."
)

response_WTKM4 = TemplateSendMessage(alt_text="I'm currently looking for an intern oppertunity!",
    template=ButtonsTemplate(
        text="I'm currently looking for an intern oppertunity!",
        actions=[
            PostbackAction(
                label='Got It',
                text='Got It',
                data='aboutme_got_it'
            )
        ]
    )
)


response_DWTKM = StickerSendMessage(
    package_id='1',
    sticker_id='16'
)

response_DWTKM2 = TemplateSendMessage(
    alt_text="Pleeeeese, won't take up too much of your time",
    template=ButtonsTemplate(
        text="Pleeeeese, won't take up too much of your time",
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

response_navigate = TextSendMessage(
	text= "You can find more funny things in 'Menu' at the bottom of the page."
)
