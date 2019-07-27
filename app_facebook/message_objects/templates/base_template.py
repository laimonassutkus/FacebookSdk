from app_facebook.message_objects.base_message_object import BaseMessageObject


class BaseTemplate(BaseMessageObject):
    def __init__(self):
        self.template_type = None

    def to_json(self):
        assert self.template_type, 'Template type not specified.'

        return {
            'template_type': self.template_type
        }