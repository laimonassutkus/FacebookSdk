from typing import List
from app_facebook.message_objects.base_message_object import BaseMessageObject
from app_facebook.message_objects.buttons.base_button import BaseButton
from app_facebook.message_objects.elements.default_action import DefaultAction


class ElementDefinition(BaseMessageObject):
    def __init__(self, title: str, image_url: str, subtitle: str, action: DefaultAction, buttons: List[BaseButton] = []):
        self.buttons = buttons
        self.action = action
        self.subtitle = subtitle
        self.image_url = image_url
        self.title = title

    def to_json(self):
        json = {
            'title': self.title,
            'image_url': self.image_url,
            'subtitle': self.subtitle,
            'default_action': self.action.to_json()
        }

        if self.buttons:
            json['buttons'] = [button.to_json() for button in self.buttons]

        return json
