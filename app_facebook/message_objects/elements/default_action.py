from app_facebook.message_objects.base_message_object import BaseMessageObject
from app_facebook.message_objects.elements.webview_height_ratio_enum import WebviewHeightRatioEnum


class DefaultAction(BaseMessageObject):
    def __init__(
            self,
            url: str,
            webview_height_ratio: WebviewHeightRatioEnum,
            message_extensions: bool = False,
            action_type: str = 'web_url'
    ) -> None:
        """
        Constructor.
        """
        self.action_type = action_type
        self.message_extensions = message_extensions
        self.webview_height_ratio = webview_height_ratio
        self.url = url

    def to_json(self):
        return {
            "type": self.action_type,
            "url": self.url,
            "messenger_extensions": self.message_extensions,
            "webview_height_ratio": self.webview_height_ratio.value
        }
