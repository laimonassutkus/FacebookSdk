from app_facebook.message_objects.buttons.base_button import BaseButton


class UrlButton(BaseButton):
    def __init__(self, title: str, url: str):
        super().__init__(title=title)

        self.type = 'web_url'
        self.url = url

    def to_json(self):
        json = super().to_json()
        json['url'] = self.url
        return json
