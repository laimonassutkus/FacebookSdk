from typing import Optional
from app_facebook.message_objects.base_message_object import BaseMessageObject


class BaseButton(BaseMessageObject):
    def __init__(self, title: Optional[str] = None):
        self.type = None
        self.title = title

    def to_json(self):
        assert self.type, 'Button type can not be empty'

        json = { 'type': self.type }

        if self.title:
            json['title'] = self.title

        return json
