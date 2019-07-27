from typing import Dict, Optional
from app_facebook.events.abstract_event import AbstractEvent
from app_facebook.message_objects.buttons.postback_button import PostbackButton
from app_facebook.message_objects.buttons.quick_button import QuickButton
from app_facebook.message_objects.elements.default_action import DefaultAction
from app_facebook.message_objects.elements.element import Element
from app_facebook.message_objects.elements.element_definition import ElementDefinition
from app_facebook.message_objects.elements.webview_height_ratio_enum import WebviewHeightRatioEnum
from app_facebook.message_objects.reply import Reply
from app_facebook.message_objects.templates.generic_template import GenericTemplate
from app_facebook.view import View


class DummyEvent(AbstractEvent):
    def __init__(self, expected_payload: Optional[Dict] = None):
        super().__init__()
        self.expected_payload = expected_payload

    EXPECTED_PAYLOAD_DICT = { 'test-key': 'test-value' }
    EXPECTED_JSON = {
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': [
                            {
                                'buttons': [
                                    {
                                        'payload': 'test_payload_button',
                                        'title': 'test_title_button',
                                        'type': 'postback'
                                    }
                                ],
                                'default_action': {
                                    'messenger_extensions': False,
                                    'type': 'web_url',
                                    'url': 'http://default_action.com',
                                    'webview_height_ratio': 'FULL'
                                },
                                'image_url': 'http://image.com',
                                'subtitle': 'test_subtitle_element_definition',
                                'title': 'test_title_element_definition'
                            }
                        ],
                    },
                },
                'quick_replies': [
                    {
                        'content_type': 'text',
                        'payload': 'test_payload_quick_button',
                        'title': 'test_title_quick_button',
                    }
                ]
            },
            'recipient': {
                'id': '123'
            }
        }

    def raise_view(self) -> View:
        assert self.payload().payload_dict == (self.expected_payload or self.EXPECTED_PAYLOAD_DICT)

        quick_button = QuickButton(
            title='test_title_quick_button',
            payload='test_payload_quick_button'
        )

        button = PostbackButton(
            title='test_title_button',
            payload='test_payload_button'
        )

        action = DefaultAction(
            url='http://default_action.com',
            webview_height_ratio=WebviewHeightRatioEnum.FULL
        )

        element_definition = ElementDefinition(
            title='test_title_element_definition',
            image_url='http://image.com',
            subtitle='test_subtitle_element_definition',
            action=action
        )

        element = Element(
            element_definition=element_definition,
            buttons=[button]
        )

        template = GenericTemplate(
            [element]
        )

        reply = Reply(
            recipient_id='123',
            template=template,
            quick_buttons=[quick_button],
        )

        return View(reply)
