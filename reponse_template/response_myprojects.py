from linebot.models import (
    TextSendMessage, TemplateSendMessage, ImageCarouselTemplate, CarouselTemplate,
    CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction, URIAction, ImageCarouselColumn
)

response_porjects_carousel = TemplateSendMessage(
    alt_text='Sorry, this message can show on mobile :)',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://lh3.googleusercontent.com/nAp1i1NgfPxbreIQnlZTwVi2cqzbE25IQtTlq7Jmjk7SuGRWgerp2rsI274Ggtpzhvo',
                title="I'm Ping Pong King :)",
                text='Do some finger exercise and release the stress of the day!',
                actions=[
                    URIAction(
                        label='Try Out! (Android)',
                        uri="http://orangenose.page.link/pingpongkingbtn01?fbclid=IwAR2mbrp-vzUgS9vj9cbLJwSPY1xJ3SIm-IUUrzQClyRKiexwmqsC1IVIhfs"
                    ),
                    URIAction(
                        label='Try Out! (IOS)',
                        uri="http://orangenose.page.link/pingpongkingbtn01?fbclid=IwAR2mbrp-vzUgS9vj9cbLJwSPY1xJ3SIm-IUUrzQClyRKiexwmqsC1IVIhfs"
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://3.bp.blogspot.com/-ruZzgX3ootA/W3U3VnAXfyI/AAAAAAAAAWI/jVX8SvzcmXgO92Z5P9VGLszOr3hHc0FpACLcBGAs/s1600/com.orangenose.trick.jpg',
                title='Triky Test 2',
                text="87% people can't solve it.\nCan you solve it?",
                actions=[
                    URIAction(
                        label='Try Out! (Android)',
                        uri='https://goo.gl/VwTCRh'
                    ),
                    URIAction(
                        label='Try Out! (IOS)',
                        uri='https://goo.gl/kGt8V5'
                    )
                ]
            )
        ],
        image_size='contain'
    )
)

response_introduce = TextSendMessage(
	text='Those are the projects I have participated in, hope you enjoy it.'
)
