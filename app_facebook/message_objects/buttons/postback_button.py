from app_facebook.message_objects.buttons.base_button import BaseButton


class PostbackButton(BaseButton):
    def __init__(self, title: str, payload: str):
        super().__init__(title=title)

        self.type = 'postback'
        self.payload = payload

    def to_json(self):
        json = super().to_json()
        json['payload'] = self.payload
        return json
