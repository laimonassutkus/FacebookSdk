from typing import List, Optional
from app_facebook.message_objects.base_message_object import BaseMessageObject
from app_facebook.message_objects.buttons.quick_button import QuickButton
from app_facebook.message_objects.templates.base_template import BaseTemplate


class Reply(BaseMessageObject):
    def __init__(self, recipient_id: str, template: Optional[BaseTemplate] = None, quick_buttons: List[QuickButton] = [], text: Optional[str] = None):
        self.text = text
        self.recipient_id = recipient_id
        self.template = template
        self.quick_buttons = quick_buttons

    def to_json(self):
        recipient = {
            "id": self.recipient_id
        }

        if self.template:
            message = {
                "attachment": {
                    "type": "template",
                    "payload": self.template.to_json()
                }
            }
        elif self.text:
            message = {
                "text": self.text
            }
        else:
            raise ValueError('Could not create reply. Missing elements.')

        if self.quick_buttons:
            message['quick_replies'] = [button.to_json() for button in self.quick_buttons]

        return {
            'recipient': recipient,
            'message': message
        }
