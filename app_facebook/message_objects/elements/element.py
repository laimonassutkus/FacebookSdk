from typing import List
from app_facebook.message_objects.base_message_object import BaseMessageObject
from app_facebook.message_objects.buttons.base_button import BaseButton
from app_facebook.message_objects.elements.element_definition import ElementDefinition


class Element(BaseMessageObject):
    def __init__(self, element_definition: ElementDefinition, buttons: List[BaseButton]):
        self.buttons = buttons
        self.element_definition = element_definition

    def to_json(self):
        json = self.element_definition.to_json()

        if self.buttons:
            json['buttons'] = [button.to_json() for button in self.buttons]

        return json
