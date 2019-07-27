from typing import Optional
from app_facebook.message_objects.buttons.base_button import BaseButton


class QuickButton(BaseButton):
    def __init__(self, title: str, payload: str, image_url: Optional[str] = None):
        super().__init__(title)

        self.image_url = image_url
        self.payload = payload
        self.content_type = 'text'
        self.type = 'quick'

    def to_json(self):
        json = super().to_json()

        # Facebook API does not accept this parameter
        if json.get('type'):
            del json['type']

        json['content_type'] = self.content_type
        json['payload'] = self.payload

        if self.image_url:
            json['image_url'] = self.image_url

        return json
